# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import pytest
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By

# TODO: Correct database access


@pytest.fixture()
def index_url():
    return reverse("index")


def setup(live_server, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{live_server}{url}")
    return driver


def teardown(driver):
    driver.quit()


def test_map(live_server, index_url):
    """
    Check if the map is present, when it shall be shown
    """
    driver = setup(live_server, index_url)

    # test if leaflet div is correct
    map_div = driver.find_element(value="map")

    if map_div.is_displayed():
        map_height = int(map_div.value_of_css_property("height").replace("px", ""))
        assert map_height > 0
    else:
        pytest.skip("Map exists, but is not displayed")

    teardown(driver)


# TODO: The following tests are incomplete, since the linked sites do not exists
def test_link_melden(live_server, index_url):
    """
    Check, if there is a link to create a new request
    """
    driver = setup(live_server, index_url)

    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "melden")
        # TODO: Check if the link is set correct
    finally:
        teardown(driver)


def test_link_all(live_server, index_url):
    """
    Check, if there is a link to a list with all requests.
    """
    driver = setup(live_server, index_url)
    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "alle")
        # TODO: Check if the link is set correct
    finally:
        teardown(driver)


def test_link_login(live_server, index_url):
    """
    Check, if there is a button/link to login.
    """
    driver = setup(live_server, index_url)
    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "login")
        # TODO: Check if the link is set correct
    finally:
        teardown(driver)
