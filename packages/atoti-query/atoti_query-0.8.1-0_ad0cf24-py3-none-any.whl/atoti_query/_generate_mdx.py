from collections.abc import Collection, Iterable, Mapping, Sequence
from typing import Literal, Optional

from atoti_core import (
    BASE_SCENARIO_NAME,
    ComparisonCondition,
    Constant,
    HierarchyCoordinates,
    HierarchyIsinCondition,
    IsinCondition,
    LevelCoordinates,
    MeasureCoordinates,
    QueryFilter,
    decombine_condition,
)

from ._discovery import IndexedDiscoveryCube, IndexedDiscoveryHierarchy
from ._hierarchy_filter import HierarchyFilter


def _escape(name: str, /) -> str:
    return name.replace("]", "]]")


def _generate_set(
    members: Collection[str], /, *, single_element_short_syntax: bool = True
) -> str:
    if single_element_short_syntax and len(members) == 1:
        return next(iter(members))

    return f"""{{{", ".join(members)}}}"""


def _generate_columns_set(measures_coordinates: Iterable[MeasureCoordinates], /) -> str:
    return _generate_set(
        [
            f"[Measures].[{_escape(measure_coordinates.measure_name)}]"
            for measure_coordinates in measures_coordinates
        ],
        # Atoti UI 5 does not support it.
        # See https://support.activeviam.com/jira/browse/UI-5036.
        single_element_short_syntax=False,
    )


def _keep_only_deepest_levels(
    levels_coordinates: Iterable[LevelCoordinates],
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> dict[LevelCoordinates, int]:
    hierarchy_to_max_level_depth: dict[HierarchyCoordinates, int] = {}

    for level_coordinates in levels_coordinates:
        hierarchy_coordinates = level_coordinates.hierarchy_coordinates
        current_max_level_depth = hierarchy_to_max_level_depth.get(
            hierarchy_coordinates, -1
        )
        regular_level_names = [
            level["name"]
            for level in cube["dimensions"][hierarchy_coordinates.dimension_name][
                "hierarchies"
            ][hierarchy_coordinates.hierarchy_name]["levels"].values()
        ]
        level_depth = regular_level_names.index(level_coordinates.level_name)

        if level_depth > current_max_level_depth:
            hierarchy_to_max_level_depth[hierarchy_coordinates] = level_depth

    return {
        LevelCoordinates(
            hierarchy_coordinates.dimension_name,
            hierarchy_coordinates.hierarchy_name,
            list(
                cube["dimensions"][hierarchy_coordinates.dimension_name]["hierarchies"][
                    hierarchy_coordinates.hierarchy_name
                ]["levels"]
            )[depth],
        ): depth
        for hierarchy_coordinates, depth in hierarchy_to_max_level_depth.items()
    }


def _get_first_level(hierarchy: IndexedDiscoveryHierarchy, /) -> str:
    return next(iter(hierarchy["levels"])) if hierarchy["slicing"] else "ALL"


def _generate_hierarchy_unique_name(
    hierarchy_coordinates: HierarchyCoordinates,
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_first_level: bool = False,
) -> str:
    parts = [hierarchy_coordinates.dimension_name, hierarchy_coordinates.hierarchy_name]

    if include_first_level:
        hierarchy = cube["dimensions"][hierarchy_coordinates.dimension_name][
            "hierarchies"
        ][hierarchy_coordinates.hierarchy_name]
        parts.append(_get_first_level(hierarchy))

    return ".".join(f"[{_escape(part)}]" for part in parts)


def _generate_level_set(
    level_coordinates: LevelCoordinates,
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_totals: bool,
    level_depth: int,
) -> str:
    hierarchy = cube["dimensions"][level_coordinates.dimension_name]["hierarchies"][
        level_coordinates.hierarchy_name
    ]
    return (
        f"{_generate_hierarchy_unique_name(level_coordinates.hierarchy_coordinates, cube=cube)}.[{_escape(level_coordinates.level_name)}].Members"
        if hierarchy["slicing"] or not include_totals
        else f"Hierarchize(Descendants({{{_generate_hierarchy_unique_name(level_coordinates.hierarchy_coordinates, cube=cube, include_first_level=True)}.[AllMember]}}, {level_depth}, SELF_AND_BEFORE))"
    )


def _generate_rows_set(
    levels_coordinates: Mapping[LevelCoordinates, int],
    /,
    *,
    cube: IndexedDiscoveryCube,
    include_totals: bool,
) -> str:
    if len(levels_coordinates) == 1:
        level_coordinates, level_depth = next(iter(levels_coordinates.items()))
        return _generate_level_set(
            level_coordinates,
            cube=cube,
            include_totals=include_totals,
            level_depth=level_depth,
        )

    return f"""Crossjoin({", ".join(
        [
            _generate_level_set(level_coordinates, cube=cube,include_totals=include_totals, level_depth=level_depth)
            for level_coordinates, level_depth in levels_coordinates.items()
        ]
    )})"""


def _ensure_condition_on_shallowest_level(
    level_coordinates: LevelCoordinates,
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> None:
    if (
        next(
            level["name"]
            for level in cube["dimensions"][level_coordinates.dimension_name][
                "hierarchies"
            ][level_coordinates.hierarchy_name]["levels"].values()
            if level["type"] != "ALL"
        )
        != level_coordinates.level_name
    ):
        raise (
            ValueError(
                f"Only conditions based on the shallowest level of a hierarchy are supported but level {level_coordinates} was given."
            )
        )


def _generate_hierarchy_coordinates_to_filter(
    *,
    comparison_conditions: Iterable[
        ComparisonCondition[LevelCoordinates, Literal["eq", "ne"], Constant]
    ],
    cube: IndexedDiscoveryCube,
    hierarchy_isin_conditions: Iterable[HierarchyIsinCondition],
    isin_conditions: Iterable[IsinCondition[LevelCoordinates, Constant]],
) -> dict[HierarchyCoordinates, HierarchyFilter]:
    hierarchy_coordinates_to_filter: dict[HierarchyCoordinates, HierarchyFilter] = {}

    def add_hierarchy_filter(
        hierarchy_filter: HierarchyFilter,
        /,
        *,
        hierarchy_coordinates: HierarchyCoordinates,
    ) -> None:
        existing_filter = hierarchy_coordinates_to_filter.get(hierarchy_coordinates)

        hierarchy_coordinates_to_filter[hierarchy_coordinates] = (
            existing_filter & hierarchy_filter if existing_filter else hierarchy_filter
        )

    for comparison_condition in comparison_conditions:
        _ensure_condition_on_shallowest_level(comparison_condition.subject, cube=cube)

        add_hierarchy_filter(
            HierarchyFilter(
                exclusion=comparison_condition.operator == "ne",
                member_paths=[(comparison_condition.target,)],
            ),
            hierarchy_coordinates=comparison_condition.subject.hierarchy_coordinates,
        )

    for isin_condition in isin_conditions:
        _ensure_condition_on_shallowest_level(isin_condition.subject, cube=cube)

        add_hierarchy_filter(
            HierarchyFilter(
                member_paths=[(member,) for member in isin_condition.elements],
            ),
            hierarchy_coordinates=isin_condition.subject.hierarchy_coordinates,
        )

    for hierarchy_isin_condition in hierarchy_isin_conditions:
        add_hierarchy_filter(
            HierarchyFilter(
                member_paths=hierarchy_isin_condition.member_paths,
            ),
            hierarchy_coordinates=hierarchy_isin_condition.subject,
        )

    return hierarchy_coordinates_to_filter


def _generate_member_unique_name(
    member_path: Iterable[Constant],
    /,
    *,
    cube: IndexedDiscoveryCube,
    hierarchy_coordinates: HierarchyCoordinates,
) -> str:
    hierarchy = cube["dimensions"][hierarchy_coordinates.dimension_name]["hierarchies"][
        hierarchy_coordinates.hierarchy_name
    ]
    parts = [
        _generate_hierarchy_unique_name(
            hierarchy_coordinates, cube=cube, include_first_level=True
        )
    ]

    if not hierarchy["slicing"]:
        parts.append("[AllMember]")

    for member in member_path:
        value = member.value
        if not isinstance(value, str):
            raise (
                TypeError(
                    f"Only conditions against strings are supported but `{hierarchy_coordinates}` was compared against `{value}` of type `{type(value)}`."
                )
            )

        parts.append(f"[{_escape(value)}]")

    return ".".join(parts)


def _generate_filter(
    hierarchy_filter: HierarchyFilter,
    /,
    *,
    cube: IndexedDiscoveryCube,
    hierarchy_coordinates: HierarchyCoordinates,
) -> str:
    filter_set = _generate_set(
        [
            _generate_member_unique_name(
                member_path, cube=cube, hierarchy_coordinates=hierarchy_coordinates
            )
            for member_path in hierarchy_filter.member_paths
        ]
    )

    return (
        f"Except({_generate_hierarchy_unique_name(hierarchy_coordinates, cube=cube)}.Members,{filter_set})"
        if hierarchy_filter.exclusion
        else filter_set
    )


def _generate_filters(
    hierarchy_coordinates_to_filter: Mapping[HierarchyCoordinates, HierarchyFilter],
    /,
    *,
    cube: IndexedDiscoveryCube,
    scenario_name: str,
) -> list[str]:
    filters = [
        _generate_filter(
            hierarchy_filter,
            cube=cube,
            hierarchy_coordinates=hierarchy_coordinates,
        )
        for hierarchy_coordinates, hierarchy_filter in hierarchy_coordinates_to_filter.items()
    ]

    if scenario_name != BASE_SCENARIO_NAME:
        filters.append(
            _generate_member_unique_name(
                [Constant(scenario_name)],
                cube=cube,
                hierarchy_coordinates=HierarchyCoordinates("Epoch", "Epoch"),
            )
        )

    return filters


def _generate_from_clause(
    filters: Sequence[str],
    /,
    *,
    cube: IndexedDiscoveryCube,
) -> str:
    from_cube = f"""FROM [{_escape(cube["name"])}]"""

    if not filters:
        return from_cube

    return f"FROM (SELECT {filters[-1]} ON COLUMNS {_generate_from_clause(filters[0:-1], cube=cube)})"


def _generate_mdx_with_decombined_conditions(
    *,
    comparison_conditions: Iterable[
        ComparisonCondition[LevelCoordinates, Literal["eq", "ne"], Constant]
    ] = (),
    cube: IndexedDiscoveryCube,
    hierarchy_isin_conditions: Iterable[HierarchyIsinCondition] = (),
    include_empty_rows: bool = False,
    include_totals: bool = False,
    isin_conditions: Iterable[IsinCondition[LevelCoordinates, Constant]] = (),
    levels_coordinates: Iterable[LevelCoordinates],
    measures_coordinates: Iterable[MeasureCoordinates],
    scenario_name: str,
) -> str:
    mdx = f"SELECT {_generate_columns_set(measures_coordinates)} ON COLUMNS"

    deepest_levels = _keep_only_deepest_levels(levels_coordinates, cube=cube)

    if deepest_levels:
        mdx = f"{mdx}, {'' if include_empty_rows else 'NON EMPTY '}{_generate_rows_set(deepest_levels, cube=cube, include_totals=include_totals)} ON ROWS"

    hierarchy_coordinates_to_filter = _generate_hierarchy_coordinates_to_filter(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        isin_conditions=isin_conditions,
    )

    filters = _generate_filters(
        hierarchy_coordinates_to_filter,
        cube=cube,
        scenario_name=scenario_name,
    )

    return f"{mdx} {_generate_from_clause(filters, cube=cube)}"


def generate_mdx(
    *,
    cube: IndexedDiscoveryCube,
    filter: Optional[QueryFilter] = None,  # noqa: A002
    include_empty_rows: bool = False,
    include_totals: bool = False,
    levels_coordinates: Iterable[LevelCoordinates] = (),
    measures_coordinates: Iterable[MeasureCoordinates] = (),
    scenario: str = BASE_SCENARIO_NAME,
) -> str:
    """Return the corresponding MDX query.

    The value of the measures is given on all the members of the given levels.
    If no level is specified then the value at the top level is returned.
    """
    allowed_comparison_operators: tuple[Literal["eq", "ne"], ...] = ("eq", "ne")

    comparison_conditions, isin_conditions, hierarchy_isin_conditions = (
        ((), (), ())
        if filter is None
        else decombine_condition(
            filter,
            allowed_subject_types=(LevelCoordinates,),
            allowed_comparison_operators=allowed_comparison_operators,
            allowed_target_types=(Constant,),
            allowed_combination_operators=("and",),
            allowed_isin_element_types=(Constant,),
        )[0]
    )

    return _generate_mdx_with_decombined_conditions(
        comparison_conditions=comparison_conditions,
        cube=cube,
        hierarchy_isin_conditions=hierarchy_isin_conditions,
        include_empty_rows=include_empty_rows,
        include_totals=include_totals,
        isin_conditions=isin_conditions,
        levels_coordinates=levels_coordinates,
        measures_coordinates=measures_coordinates,
        scenario_name=scenario,
    )
