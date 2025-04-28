from slcsp.slcsp import *
import pytest

def test_csv_parser():
    count = 0
    for plan in parse_csv_and_filter("plans.csv", 2):
        count += 1

    assert count == 22241

@pytest.mark.parametrize('test_zipcode,ziplist, result',
                         [ ('02188',{'02188':{('NY', '5'):['1.0', '8.9', '9', '4', '4', '1.0', '3']}}, 3.0),
                           ('02198',{'02188':{('NY', '5'):['1.0', '8.9', '9', '4', '4', '1.0', '3']}}, None),
                           ('11203',{'11203':{('GA', '5'):['4.3', '33.2', '2.0'],('GA', '7'):['1.0', '3.4', '5.5']}}, None),
                           ('33443',{'33443':{('TX', '2'):['9.3']}},None)
                            ])
def test_second_least_rate_non_panda(test_zipcode:str, ziplist:dict(dict(list())), result:float|None):
    found_rate = find_second_lowest_rate(test_zipcode, ziplist)
    assert result == found_rate
