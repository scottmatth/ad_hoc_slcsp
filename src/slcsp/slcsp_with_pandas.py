import pandas as pd
from slcsp import ROOT_SRC_DIR

def determine_second_lowest_rate(zipcode:str, zip_to_rates:pd.DataFrame) -> int | None:
    result = None
    if len(set(zip_to_rates.query(f"zipcode == @zipcode").rate.values)) > 1:
        if len(set(zip_to_rates.query(f"zipcode == @zipcode").index)) == 1:
            result = sorted(list(map(float, set(zip_to_rates.query(f"zipcode == @zipcode").rate.values))))[1]
    return result

if __name__ == '__main__':

    all_plans = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/plans.csv",
                            index_col=['state', 'rate_area'],dtype=pd.StringDtype())

    all_zips = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/zips.csv",
                           index_col=["zipcode","state", "rate_area"],dtype=pd.StringDtype())

    plans_for_zips = all_zips.join(all_plans[all_plans['metal_level'] == 'Silver'],
                                   on =["state", "rate_area"],
                                   lsuffix="_plans", rsuffix="zips",
                                   how="inner")

    slcsp_source = pd.read_csv(str(ROOT_SRC_DIR) + "/data_files/slcsp.csv",dtype=pd.StringDtype())
    for slcsp in slcsp_source.values:
        second_lowest = determine_second_lowest_rate(slcsp[0], plans_for_zips)
        output = slcsp[0] + "," + (str(second_lowest) if second_lowest is not None else "")
        print(output)

    
##    print(slcsp_source.values)
##    control_zipcodes = slcsp_source. 
    
##    print(plans_for_zips.index)

##    print(plans_for_zips.query("zipcode == 82605")["rate_area"].nunique())
##    print(len(set(plans_for_zips.query("zipcode == 82605").index)))
##    print(len(set(plans_for_zips.query("zipcode == 82605").rate.values)))

##    just_36003 = plans_for_zips.query("zipcode==36003 and metal_level=='Silver'").head(100)
##    just_silver = plans_for_zips.query("metal_level=='Silver'")
##    just_silver = plans_for_zips.query()
##    print(just_silver.head(20))
