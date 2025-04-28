from slcsp.slcsp import *
from slcsp.slcsp_with_pandas import *
import pytest
import pandas as pd


@pytest.fixture
def zip_dataframe_fixture():
    fixtured_data = {"zipcode":["02188","02188","02188","02188","02188","02188","02188",
                                "11203","11203","11203","11203","11203","11203",
                                "33443"],
                     "state":["NY","NY","NY","NY","NY","NY","NY",
                              "GA","GA","GA","GA","GA","GA",
                              "TX"],
                     "rate_area":['5','5','5','5','5','5','5',
                                  '6','6','6','7','7','7',
                                  '2'],
                     "county_code":["99339","99339","99339","99339","99339","99339","99339",
                                    "19339","19339","19339","299339","299339","299339",
                                    "399339"],
                     "name":["county_test","county_test","county_test","county_test","county_test","county_test","county_test",
                             "county_test1","county_test1","county_test1","county_test2","county_test2","county_test2",
                             "county_test3"],
                     "plan_id":["1", "2", "3", "4", "5","6","7",
                                "11", "12", "13", "24", "25","26",
                                "36"],
                     "metal_level":["Silver", "Silver", "Silver", "Silver", "Silver", "Silver","Silver",
                                    "Silver", "Silver", "Silver", "Silver", "Silver", "Silver",
                                    "Silver"],
                     "rate":['1.0', '8.9', '9', '4', '4', '1.0', '3',
                             '4.3', '33.2', '2.0','1.0', '3.4', '5.5',
                             '9.3']}
    framed_fixture = pd.DataFrame(data=fixtured_data, dtype=pd.StringDtype()                                  )
    framed_fixture = framed_fixture.set_index(["zipcode", "state", "rate_area"])
    return framed_fixture


def test_csv_parser():
    count = 0
    for plan in parse_csv_and_filter("plans.csv", 2):
        count += 1

    assert count == 22241


@pytest.mark.parametrize('test_zipcode,result',
                         [ ('02188',3.0),
                           ('02198', None),
                           ('11203', None),
                           ('33443', None)
                            ])
def test_second_least_rate_non_panda(test_zipcode:str, result:float|None):
    ziplist = {'02188':{('NY', '5'):['1.0', '8.9', '9', '4', '4', '1.0', '3']},
                                     '11203':{('GA', '6'):['4.3', '33.2', '2.0'],('GA', '7'):['1.0', '3.4', '5.5']},
                                     '33443':{('TX', '2'):['9.3']}}

    found_rate = find_second_lowest_rate(test_zipcode, ziplist)
    
    assert result == found_rate


@pytest.mark.parametrize('test_zipcode, result',
                         [('02188',3.0),
                           ('02198',None),
                           ('11203',None),
                           ('33443',None)]
                         )
def test_second_least_rate_w_pandas(test_zipcode:str, result:float|None, zip_dataframe_fixture):
    found_rate = determine_second_lowest_rate(test_zipcode, zip_dataframe_fixture)

    assert found_rate == result
