from src.data_load import load_data


def main():
    data_df = load_data()
    if data_df is None:
        print("Failed to load data.")
        return
    
    print("Data loaded successfully:")
    print(data_df.head())

    print(f"Basic quality analysis:\n{data_df.describe()}")


if __name__ == "__main__":
    main()
