#!/usr/bin/env python3
"""Open each html_url from the JSON file in Selenium, wait 5 seconds, then close."""

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mouse_operation import click_with_highlight, parse_coords

JSON_FILE = "rts_papers_output/papers_raw_20260212_132745.json"
ieee_home_page = "https://ieeexplore.ieee.org/Xplore/home.jsp"
download_button_x = 2450
download_button_y = 155

save_button_x = 1750
save_button_y = 215

sign_out_button = (1347, 168)
inst_sign_in_button = (1270, 188)
inst_sign_in_confirm_button = (1265, 300)
probable_prev_download_cancel_button = (812, 213)
download_wait_ms = 3
download_wait_ms_increament = 3


def relogin(driver):
    print(f"Logging in")
    time.sleep(2)
    driver.get(ieee_home_page)
    time.sleep(2)
    click_with_highlight(probable_prev_download_cancel_button[0], probable_prev_download_cancel_button[1], show_highlight=False)
    time.sleep(2)
    click_with_highlight(sign_out_button[0], sign_out_button[1], show_highlight=False)
    time.sleep(2)
    click_with_highlight(inst_sign_in_button[0], inst_sign_in_button[1], show_highlight=False)
    time.sleep(2)
    click_with_highlight(inst_sign_in_confirm_button[0], inst_sign_in_confirm_button[1], show_highlight=False)
    time.sleep(5)

def main():
    # Load the JSON file
    global download_wait_ms
    global download_wait_ms_increament
    global ieee_home_page
    global save_button_x
    global save_button_y
    global download_button_x
    global download_button_y
    
    with open(JSON_FILE, "r") as f:
        papers = json.load(f)

    print(f"Found {len(papers)} papers")

    # Connect to existing Chrome browser with remote debugging
    # Start Chrome first with: google-chrome --remote-debugging-port=9222
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # Connect to the existing browser instance
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(2)

    try:
        for i, paper in enumerate(papers):
            if i%10 == 0:
                download_wait_ms = download_wait_ms + download_wait_ms_increament
                download_wait_ms = min(download_wait_ms, 15)
            if "downloaded" in paper.keys() and paper["downloaded"] == True:
                print(f"{i+1}. {paper["title"]} already in downloaded files")
                continue
            if i%30 == 0:
                with open(JSON_FILE, "w", encoding="utf-8") as f:
                    json.dump(papers, f, indent=4)
                relogin(driver=driver)
            
            pdf_url = paper.get("pdf_url")
            if pdf_url:
                print(f"[{i+1}/{len(papers)}] Opening: {pdf_url}")
                driver.get(pdf_url)
                time.sleep(download_wait_ms)
                # x, y = parse_coords()
                click_with_highlight(download_button_x, download_button_y, show_highlight=False)
    
                time.sleep(download_wait_ms)
                # x, y = parse_coords()
                click_with_highlight(save_button_x, save_button_y, show_highlight=False)
                time.sleep(3)
                papers[i]["downloaded"] = True

            else:
                print(f"[{i+1}/{len(papers)}] No pdf_url found, skipping")

        print("All tabs opened!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Don't quit - we're attached to an existing browser
        print("Done! Browser remains open.")

if __name__ == "__main__":
    main()
