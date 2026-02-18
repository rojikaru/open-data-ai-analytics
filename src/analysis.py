import polars as pl
from src.processing import map_koatuu_to_region


def most_common_vehicle_type(
        vehicles_df: pl.DataFrame,
        target_column: str = "KIND"
) -> tuple[str, int]:
    """
    Find the most common vehicle type in the given DataFrame.

    :param vehicles_df (pl.DataFrame): A Polars DataFrame containing vehicle data.
    :param target_column (str): The column name to analyze for the most common vehicle type.

    :return (tuple[str, int]): The most common vehicle type and the count of them registered.
    """
    
    most_common = (vehicles_df.group_by(target_column)
        .len()
        .sort("len", descending=True)[0]
        .row())
    return most_common


def vehicle_ownership_by_region(
        vehicles_df: pl.DataFrame,
        target_codes: list[int] | None = None,
        region_column: str = "REG_ADDR_KOATUU",
        new_region_column: str = "HUMAN_REGION",
        status_column: str = "OPER_CODE",
) -> pl.DataFrame:
    """
    Analyze vehicle ownership by region.

    :param vehicles_df (pl.DataFrame): A Polars DataFrame containing vehicle data.
    :param region_column (str): The column name representing the region.
    :param new_region_column (str): The column name for the human-readable region after mapping.
    :param status_column (str): The column name representing the operational status.
    :param target_codes (list[int]): The list of target operational codes to filter for.

    :return (pl.DataFrame): A DataFrame showing the count of owned vs. non-owned vehicles by region.
    """

    if target_codes is None:
        target_codes = [100, 105, 430]
    
    vehicle_acquiry_df = vehicles_df.filter(pl.col(status_column).is_in(target_codes))
    transform_koatuu_to_human = (pl.col(region_column)
        .map_elements(map_koatuu_to_region)
        .alias(new_region_column))

    ownership_by_region = (vehicle_acquiry_df
        .with_columns(transform_koatuu_to_human)
        .group_by([new_region_column])
        .len()
        .sort(new_region_column))
    return ownership_by_region
