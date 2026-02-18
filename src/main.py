from src.data_load import load_data


def main():
    data_df = load_data()
    if data_df is not None:
        print("Data loaded successfully:")
        print(data_df.head())
    else:
        print("Failed to load data.")


if __name__ == "__main__":
    main()
