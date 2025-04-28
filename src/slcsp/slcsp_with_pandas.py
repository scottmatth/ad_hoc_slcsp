import pandas as pd
from slcsp import ROOT_SRC_DIR

def determine_second_lowest_rate(zipcode:str,
                                 zip_to_rates:pd.DataFrame) -> float | None:
    """
    Parses the joined dataframe of existing zipcodes and rates to determine the
    second lowest cost silver rate for the given Zipcode

    Parameters:
        zipcode (str): zip code against which this method should find the second lowest
            rate (if) possible
        zip_to_rates (DataFrame): A pandas dataframe which is an Inner Join of the content of
            the provided plans.csv and the provided Zips.csv, joined by the State and Rate_area 
    """
    result = None

    # There must be more than one Rate to evaluate in order to find the second lowest rate
    if len(set(zip_to_rates.query(f"zipcode == @zipcode").rate.values)) > 1:
        # If there are more than one index combinations of Zipcode to State to Rate_area,
        # this is too ambiguous to determine
        if len(set(zip_to_rates.query(f"zipcode == @zipcode").index)) == 1:

            # Determine the second lowest rate by sorting the set of values (in case 2 are the same)
            # and getting the second one in the list
            result = sorted(list(map(float, set(zip_to_rates.query(f"zipcode == @zipcode").rate.values))))[1]
    return result

if __name__ == '__main__':

    all_plans = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/plans.csv",
                            index_col=['state', 'rate_area'],dtype=pd.StringDtype())

    all_zips = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/zips.csv",
                           index_col=["zipcode","state", "rate_area"],dtype=pd.StringDtype())

    # Inner Join the plans and zips csv's by the state and rate area
    plans_for_zips = all_zips.join(all_plans[all_plans['metal_level'] == 'Silver'],
                                   on =["state", "rate_area"],
                                   lsuffix="_plans", rsuffix="zips",
                                   how="inner")

    # Get the initial slcsp values from the provided file, and print them out with any
    # rate values we were able to assertain
    slcsp_source = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/slcsp.csv",
                               dtype=pd.StringDtype())
    print(f"{slcsp_source.columns[0]},{slcsp_source.columns[1]}")
    for slcsp in slcsp_source.values:
        second_lowest = determine_second_lowest_rate(slcsp[0], plans_for_zips)
        output = slcsp[0] + "," + (str(second_lowest) if second_lowest is not None else "")
        print(output)

