"""
End-to-end tests for splent_feature_reset.

Run with:  splent feature:test splent_feature_reset --e2e
"""

import pytest
from splent_framework.environment.host import get_host_for_selenium_testing
from splent_framework.selenium.common import initialize_driver, close_driver


@pytest.fixture()
def browser():
    driver = initialize_driver()
    yield driver
    close_driver(driver)


def test_forgot_page_loads(browser):
    host = get_host_for_selenium_testing()
    browser.get(f"{host}/reset/forgot")
    assert (
        "forgot" in browser.page_source.lower()
        or "email" in browser.page_source.lower()
    )
