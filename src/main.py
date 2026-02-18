from src.data_load import load_data
from src.analysis import most_common_vehicle_type


def main():
    data_df = load_data()
    if data_df is None:
        print("Failed to load data.")
        return
    
    print("Data loaded successfully:")
    print(data_df.head())

    print(f"Basic quality analysis:\n{data_df.describe()}")

    print("\nMost common vehicle types: ")
    print(most_common_vehicle_type(data_df))


if __name__ == "__main__":
    main()
