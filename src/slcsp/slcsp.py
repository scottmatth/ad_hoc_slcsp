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
            silver_plans[(plan[1], plan[4])].append(plan[3])
        silver_count +=1

    zipcode_data = defaultdict(list)
    count = 0
    # Load in all of the Zip code data from the zips csv
    for zip in parse_csv_and_filter("zips.csv"):
        if count > 0:
            # Populate the zipcode dict with all zipcode data indexed by the zipcode itself
            zipcode_data[zip[0]].append(zip)
        count += 1

        
    def find_second_lowest_rate(zipcode:str):
        """
        Given a working Zip Code , this method will cross reference the data along the
        State and Plan area to determine the Second lowest cost Silver plan

        Parameters:
            zipcode (str): Primary value by which the data is to be evaluated
        Returns:
            either None if data was not able to be found, OR the 
        """
        zip_entries = zipcode_data[zipcode]

        rate_data = []
        # loop through all Zip Entries from zip.csv
        for zip_data in zip_entries:
            # Find the plan data for the gien Zip Entry 
            current_data = silver_plans[(zip_data[1], zip_data[4])]
            if current_data and len(current_data) > 1:
                plans_in_order = sorted(current_data)
                last = plans_in_order[0]
                for idx in range(1, len(plans_in_order)):
                    if plans_in_order[idx] != last:
                        rate_data.append(plans_in_order[idx])
                        break

        if len(rate_data) == 1:
            return next(iter(rate_data))
        else:
            return None
                                                                

    count = 0
    for slcsp in parse_csv_and_filter("slcsp.csv"):
        slr = None
        if count > 0:
            slr = find_second_lowest_rate(slcsp[0])
        output = slcsp[0]+","
        if slr:
            output = output + slr
        else:
            output = output + slcsp[1]
        print(output)
        count +=1
        
    pass
