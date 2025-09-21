from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# ✅ Test document path (use raw string to avoid escape issues)
TEST_DOC = r"D:\EPAN-card_meghana.png"

# Start Chrome browser
driver = webdriver.Chrome()

try:
    # Open Streamlit app
    driver.get("http://localhost:8501")

    # Upload the file
    file_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    file_input.send_keys(TEST_DOC)

    # Click the "Extract Details from Uploaded Files" button
    extract_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Extract Details from Uploaded Files')]")
        )
    )
    extract_btn.click()

    # Wait for the form to appear (first field)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Name')]"))
    )

    # Fields to extract
    field_labels = [
        "Name",
        "Father's Name",
        "Occupation",
        "Amount",
        "Address",
        "Company Name",
        "PAN ID",
        "Aadhar ID"
    ]

    extracted_values = {}

    # Extract values safely (handle stale elements)
    for label in field_labels:
        # Use double quotes if label contains apostrophe
        xpath_label = f'"{label}"' if "'" in label else f"'{label}'"

        if label == "Address":
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//textarea[contains(@aria-label, {xpath_label})]")
                )
            )
        else:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//input[contains(@aria-label, {xpath_label})]")
                )
            )

        # Access value immediately
        extracted_values[label] = element.get_attribute("value")

    # Print extracted values
    print("✅ Extracted KYC Details:")
    for k, v in extracted_values.items():
        print(f"{k}: {v}")

    # Click "Save KYC Info" button
    save_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save KYC Info')]"))
    )
    save_btn.click()

    # Wait a moment to ensure CSV is written
    time.sleep(2)

    # Verify CSV creation
    csv_path = "extracted_data/kyc_user_data.csv"
    if os.path.exists(csv_path):
        print(f"✅ Test Passed: CSV created successfully at {csv_path}")
    else:
        print(f"❌ Test Failed: CSV not found at {csv_path}")

finally:
    driver.quit()
