import pytest
import pandas as pd
from utils import localline

SMALL_SAMPLE = './tests/fixture/short_sample.csv'

@pytest.fixture
def small_sample():
    return localline.transform_data(
        localline.load_csv(SMALL_SAMPLE)
    )

def test_customer_delivery_report(small_sample):
    the_reports = list(localline.delivery_report(SMALL_SAMPLE))

    4/0
    pass