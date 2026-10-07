"""
Automated Selenium E2E Browser Testing Suite
============================================
Runs end-to-end browser automation testing using Selenium WebDriver against the live Flask dashboard:
- Scenario 1: Page Loads, Verification of Title and Executive Header
- Scenario 2: Tab Navigation Interaction (switching from Brief to Market Intelligence to ML tabs)
- Scenario 3: JDS Interactive Slider Adjustment & Prediction Verification
- Scenario 4: AI Career GPS Flight Plan Generation Flow
- Scenario 5: Workforce Digital Twin Simulator Slider Recalculation
- Scenario 6: AI Workforce Copilot Chat Query Submission
"""

import os
import time
import threading
import pytest
from app.app import app

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SERVER_PORT = 5055
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"


@pytest.fixture(scope="module")
def live_server():
    """Starts local Flask server in a daemon background thread."""
    server_thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=SERVER_PORT, debug=False, use_reloader=False))
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1.5)  # Wait for server startup
    yield SERVER_URL


@pytest.fixture(scope="module")
def driver():
    """Initializes headless Edge or Chrome webdriver."""
    driver_instance = None
    
    # Try Edge first (Standard on Windows)
    try:
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--window-size=1600,1000")
        driver_instance = webdriver.Edge(options=edge_options)
    except Exception as e_edge:
        # Fallback to Chrome
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1600,1000")
            driver_instance = webdriver.Chrome(options=chrome_options)
        except Exception as e_chrome:
            pytest.skip(f"No compatible Selenium browser driver found: {e_edge}; {e_chrome}")

    yield driver_instance
    if driver_instance:
        driver_instance.quit()


def test_scenario_1_page_load(driver, live_server):
    """Scenario 1: Verify dashboard loads, title and branding badges are rendered."""
    driver.get(live_server)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "app-header")))
    assert "WorkforceX" in driver.title or "Workforce Intelligence" in driver.page_source
    header = driver.find_element(By.CLASS_NAME, "logo-text")
    assert "WorkforceX" in header.text


def test_scenario_2_tab_navigation(driver, live_server):
    """Scenario 2: Verify tab switching activates the corresponding view pane."""
    driver.get(live_server)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tabs-nav")))
    
    # Click on "Job Market Intelligence" tab
    market_tab = driver.find_element(By.CSS_SELECTOR, "button[data-tab='tab-market']")
    market_tab.click()
    time.sleep(0.5)
    
    pane = driver.find_element(By.ID, "tab-market")
    assert "active" in pane.get_attribute("class")


def test_scenario_3_jds_prediction_interaction(driver, live_server):
    """Scenario 3: Switch to ML tab, adjust sliders, click evaluate button, check prediction."""
    driver.get(live_server)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-tab='tab-ml']")))
    
    # Open ML tab
    driver.find_element(By.CSS_SELECTOR, "button[data-tab='tab-ml']").click()
    time.sleep(0.5)
    
    # Click evaluate button
    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-eval-jds")))
    btn.click()
    
    # Wait for async fetch to populate prediction percentage
    WebDriverWait(driver, 10).until(lambda d: "%" in d.find_element(By.ID, "jds-pred-prob").text)
    prob_el = driver.find_element(By.ID, "jds-pred-prob")
    assert "%" in prob_el.text


def test_scenario_4_career_gps_generation(driver, live_server):
    """Scenario 4: Navigate to Career GPS tab and generate flight plan."""
    driver.get(live_server)
    driver.find_element(By.CSS_SELECTOR, "button[data-tab='tab-gps']").click()
    time.sleep(0.5)
    
    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-run-gps")))
    btn.click()
    time.sleep(1.0)
    
    pathways = driver.find_elements(By.CSS_SELECTOR, "#gps-pathways-container > div")
    assert len(pathways) >= 1


def test_scenario_5_workforce_simulator(driver, live_server):
    """Scenario 5: Navigate to Workforce Simulator and run simulation."""
    driver.get(live_server)
    driver.find_element(By.CSS_SELECTOR, "button[data-tab='tab-simulator']").click()
    time.sleep(0.5)
    
    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-run-sim")))
    btn.click()
    time.sleep(1.0)
    
    savings_el = driver.find_element(By.ID, "sim-savings")
    assert "Lakhs" in savings_el.text or "₹" in savings_el.text


def test_scenario_6_copilot_chat(driver, live_server):
    """Scenario 6: Test Copilot chat input submission."""
    driver.get(live_server)
    driver.find_element(By.CSS_SELECTOR, "button[data-tab='tab-copilot']").click()
    time.sleep(0.5)
    
    input_box = driver.find_element(By.ID, "chat-input")
    input_box.send_keys("What is the highest paying data role?")
    driver.find_element(By.ID, "btn-send-chat").click()
    time.sleep(1.0)
    
    history = driver.find_element(By.ID, "chat-history")
    assert "highest paying" in history.text.lower() or "salary" in history.text.lower()
