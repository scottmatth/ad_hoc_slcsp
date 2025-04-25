from slcsp.slcsp import *

def test_csv_parser():
    count = 0
    for plan in parse_csv_and_filter("plans.csv", 2):
        count += 1

    assert count == 22241
