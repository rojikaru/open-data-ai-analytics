import polars as pl


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
