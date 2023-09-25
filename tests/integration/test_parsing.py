import pytest
import pandas as pd
from utils import localline

SMALL_SAMPLE = './tests/fixture/short_sample.csv'

@pytest.fixture
def small_sample():
    return localline.transform_data(
        localline.load_csv(SMALL_SAMPLE)
    )

#@pytest.mark.skip()
def test_customer_delivery_report(small_sample):
    the_reports = list(localline.delivery_report(SMALL_SAMPLE))

    delivery_in_reports = [True for a_report in the_reports if '$' in a_report['Product']]
    assert all(delivery_in_reports), "Assert report returns non deliverable items!"

