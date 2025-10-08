# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import pytest
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# TODO: Correct database access


@pytest.fixture()
def index_url():
    return reverse("geoentries:index")


@pytest.fixture()
def create_url():
    return reverse("geoentries:create")


def setup(live_server, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{live_server}{url}")
    return driver


def teardown(driver):
    driver.quit()


# NOTE: Test Index
def test_map_in_index(live_server, index_url):
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
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "Alle")
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


# NOTE: Test create request
def test_map_in_create(live_server, create_url):
    """
    Check if the map is present, when it shall be shown
    """
    driver = setup(live_server, create_url)

    # test if leaflet div is correct
    map_div = driver.find_element(value="map")

    if map_div.is_displayed():
        map_height = int(map_div.value_of_css_property("height").replace("px", ""))
        assert map_height > 0
    else:
        pytest.skip("Map exists, but is not displayed")

    teardown(driver)


def id_present(driver, value: str) -> bool:
    """
    Checks if an id is present in the DOM.
    Next to the presented value, it also checks if there is an element with the given value create by django.
    This is done by adding "id_" as a prefix.

    Args:
        driver: webdriver
            The selenium webdriver, which controls the browser
        value: str
            The id, which shall be checked

    Returns:
        True if there is a element with value as an id.
    """
    is_present = False
    try:
        driver.find_element(By.ID, value)
        is_present = True
    except NoSuchElementException:
        pass
    if "id" not in value:
        value = "id_" + value
    try:
        driver.find_element(By.ID, value)
        is_present = True
    except NoSuchElementException:
        pass

    return is_present


def test_create_elements(live_server, create_url) -> None:
    """
    Checks if all input elements are available.

    Args:
        live_server
            A live_server used for testing
        create_url:
            The url given by the fixture create_url
    """
    driver = setup(live_server, create_url)
    assert id_present(driver, "title") is True
    assert id_present(driver, "description") is True
    assert id_present(driver, "latitude") is True
    assert id_present(driver, "longitude") is True
    assert id_present(driver, "category") is True
    assert id_present(driver, "email") is True
    teardown(driver)


# TODO: Check required fields
# TODO: Test Latitude / Longitude selection
