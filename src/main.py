import polars as pl

from src.data_load import load_data
from src.analysis import most_common_vehicle_type, vehicle_ownership_by_region


def main():
    data_df = load_data()
    if data_df is None:
        print("Failed to load data.")
        return
    
    print("Data loaded successfully:")
    print(data_df.head())

        
    with pl.Config() as config:
        config.set_tbl_rows(-1)

        print(f"Basic quality analysis:\n{data_df.describe()}")

        print("\nMost common vehicle types:")
        print(most_common_vehicle_type(data_df))

        print("\nVehicle ownership by region:")
        print(vehicle_ownership_by_region(data_df))


if __name__ == "__main__":
    main()
