import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt

from src.data_load import load_data
from src.analysis import most_common_vehicle_type, vehicle_ownership_by_region


data_url = "https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/resource/3f13166f-090b-499e-8e23-e9851c5a5f67/download/reestrtz2026.zip"


def main():
    data_df = load_data(data_url)
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
        ownership_by_region = vehicle_ownership_by_region(data_df)
        print(ownership_by_region)
        # Visualize ownership by region
        sns.barplot(data=ownership_by_region.to_pandas(), x="HUMAN_REGION", y="len")
        sns.despine()

        plt.show()


if __name__ == "__main__":
    main()
