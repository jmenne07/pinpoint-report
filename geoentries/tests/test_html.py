# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
from urllib.parse import urlparse

import pytest
from django.urls import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# TODO: Correct database access


def setup(live_server, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{live_server}{url}")
    return driver


def teardown(driver):
    driver.quit()


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


# NOTE: Test Index
def test_map_in_index(live_server):
    """
    Check if the map is present, when it shall be shown
    """
    driver = setup(live_server, reverse("geoentries:index"))

    # test if leaflet div is correct
    map_div = driver.find_element(value="map")

    if map_div.is_displayed():
        map_height = float(map_div.value_of_css_property("height").replace("px", ""))
        assert map_height > 0
    else:
        pytest.skip("Map exists, but is not displayed")

    teardown(driver)


def test_link_melden(live_server):
    """
    Check, if there is a link to create a new request on the index page
    """
    driver = setup(live_server, reverse("geoentries:index"))

    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "melden")
        link.click()
        url_path = urlparse(driver.current_url).path
        assert url_path == reverse("geoentries:create")
    finally:
        teardown(driver)


def test_link_all(live_server):
    """
    Check, if there is a link to a list with all requests.
    """
    driver = setup(live_server, reverse("geoentries:index"))
    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "Alle")
        link.click()
        url_path = urlparse(driver.current_url).path
        assert url_path == reverse("geoentries:list")
    finally:
        teardown(driver)


def test_link_login(live_server):
    """
    Check, if there is a button/link to login.
    """
    driver = setup(live_server, reverse("geoentries:index"))
    try:
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "Login")
        if not link:
            link = driver.find_element(By.PARTIAL_LINK_TEXT, "login")
        link.click()
        assert reverse("admin:login") == urlparse(driver.current_url).path
    finally:
        teardown(driver)


# NOTE: Test create request
def test_map_in_create(live_server):
    """
    Check if the map is present, when it shall be shown
    """
    driver = setup(live_server, reverse("geoentries:create"))

    # test if leaflet div is correct
    map_div = driver.find_element(value="map")

    if map_div.is_displayed():
        map_height = int(map_div.value_of_css_property("height").replace("px", ""))
        assert map_height > 0
    else:
        pytest.skip("Map exists, but is not displayed")

    teardown(driver)


def test_create_elements(live_server) -> None:
    """
    Checks if all input elements are available.

    Args:
        live_server
            A live_server used for testing
        create_url:
            The url given by the fixture create_url
    """
    driver = setup(live_server, reverse("geoentries:create"))
    assert id_present(driver, "description")
    assert id_present(driver, "latitude")
    assert id_present(driver, "longitude")
    assert id_present(driver, "category")
    assert id_present(driver, "email")
    assert id_present(driver, "image")
    teardown(driver)


# TODO: Check required fields
# TODO: Test Latitude / Longitude selection
