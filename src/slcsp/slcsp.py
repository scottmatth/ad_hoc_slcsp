from collections import defaultdict
from pathlib import Path

ROOT_SRC_DIR = Path(__file__).parent.parent


def parse_csv_and_filter(file_name:str, parse_index:int=None, filter:str = None):

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
    for plan in parse_csv_and_filter("plans.csv", 2, "Silver"):
        if silver_count > 0:
            silver_plans[(plan[1], plan[4])].append(plan[3])
        silver_count +=1

    zipcode_data = defaultdict(list)
    count = 0
    for zip in parse_csv_and_filter("zips.csv"):
        if count > 0:
            zipcode_data[zip[0]].append(zip)
        count += 1


        
    def find_second_lowest_rate(zipcode:str):
        zip_entries = zipcode_data[zipcode]

        rate_data = []
        for zip_data in zip_entries:
            current_data = silver_plans[(zip_data[1], zip_data[4])]
            if current_data and len(current_data) > 1:
                sorted(current_data)
                last = current_data[0]
                for idx in range(1, len(current_data)):
                    if current_data[idx] != last:
                        rate_data.append(current_data[idx])
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
