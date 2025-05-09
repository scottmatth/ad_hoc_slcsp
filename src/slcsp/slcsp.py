from collections import defaultdict
from pathlib import Path

ROOT_SRC_DIR = Path(__file__).parent.parent


def parse_csv_and_filter(file_name:str, parse_index:int=None, filter:str = None):
    """
    Generator which will return the values of a given csv filter said data if a filter is provided

    Parameters:
        file_name (str): The name of the file to be parsed
        parse_index (int): [Defaults to None to indicate no column to use]
            Index which corresponds to the column in the csv which should be filtered
        filter (str): [Defaults to None to indicate no filter to apply]
            Indicates the value found in the column which corresponds to parse_index by which results
            should be filtered

    Returns:
        Yielded values which adhere to the proposed filter
    """
    source_files_path = str(ROOT_SRC_DIR) + "/data_files/"
    for row in open(source_files_path + file_name, "r"):
        parsed_row = row.strip().split(",")
        if filter is None or (parse_index is not None and parsed_row[parse_index] == filter):
            yield parsed_row

def find_second_lowest_rate(zipcode:str, zipcode_data:dict(dict(list()))) ->float|None:
    """
    Given a working Zip Code , this method will cross reference the data along the
    State and Plan area to determine the Second lowest cost Silver plan

    Parameters:
        zipcode (str): Primary value by which the data is to be evaluated
    Returns:
        either None if data was not able to be found, OR the 
    """
    if zipcode in zipcode_data.keys():
        zip_entries = zipcode_data[zipcode]

        rate_data = None
        if len(zip_entries) == 1:
        # loop through all Zip Entries from zip.csv
            for zip_index, zip_data in zip_entries.items():
                # Find the plan data for the gien Zip Entry 
                if zip_data and len(zip_data) > 1:
                    plans_in_order = sorted(list(map(float, set(zip_data))))
                    rate_data = plans_in_order[1]
        return rate_data
                                                            


if __name__ == '__main__':
    """
    Load plans and filter out anything BUT the Silver level
        Plan_ids, State, metal_leval, rate, rate_area


    Load zips and correlate rate areas and state with plans
    """

    silver_plans = defaultdict(list)
    silver_count = 0
    # Load in all the plans which are of the Silver metal rate
    for plan in parse_csv_and_filter("plans.csv", 2, "Silver"):
        if silver_count > 0:
            # Populate the plan dict with all rates indexed by the State and Plan area
            silver_plans[(plan[1],plan[4])].append(plan[3])
        silver_count +=1

    zipcode_data = defaultdict(lambda:defaultdict(list))
    count = 0
    # Load in all of the Zip code data from the zips csv
    for zip in parse_csv_and_filter("zips.csv"):
        if count > 0:
            # Populate the zipcode dict with the corresponding rates for that zip code and state/rate_area combo
            zipcode_data[zip[0]][(zip[1],zip[4])].extend(silver_plans[(zip[1],zip[4])])
        count += 1


    count = 0
    for slcsp in parse_csv_and_filter("slcsp.csv"):
        slr = None
        if count > 0:
            slr = find_second_lowest_rate(slcsp[0], zipcode_data)
        output = slcsp[0]+"," + (str(slr) if slr is not None else slcsp[1])
        print(output)
        count +=1
        
    pass
