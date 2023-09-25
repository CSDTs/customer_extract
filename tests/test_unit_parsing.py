import pytest
import pandas as pd
from utils import localline

SMALL_SAMPLE = './tests/fixture/short_sample.csv'

@pytest.fixture
def small_sample():
    return localline.transform_data(
        localline.load_csv(SMALL_SAMPLE)
    )


def test_number_of_customers(small_sample):
    customers = localline.extract_customers(small_sample)
    expected = 3
    assert expected == len(customers),f"Unexpected number of customers, {len(customers)} vs. {expected}"


def test_expect_one_delivery(small_sample):
    customers = localline.extract_customers(small_sample)
    products = localline.delivery_products(
        a_customer=customers[0]
    )

    assert products.empty, "Expected no products to be present!"

    products = localline.delivery_products(
        a_customer=customers[1]
    )

    assert not products.empty, "Expected products to be present!"
    assert 1 == len(products), "Expected only one (1) products to be present!"

    products = localline.delivery_products(
        a_customer=customers[2]
    )

    assert 1 == len(products), "Expected only one (1) products from person w 5 total orders!"

def test_multi_order():
    pass

