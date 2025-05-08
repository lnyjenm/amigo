import json
from datetime import datetime
import argparse
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import item_json

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetch data from the router.')
    parser.add_argument('-password', type=str, required=True, help='Router admin password')
    parser.add_argument('-remote', type=str, help='Selenium remote host')
    parser.add_argument('-model', type=str, help='Model name')
    parser.add_argument('-fw', type=str, help='Firmware version')
    return parser.parse_args()

def setup_driver(remote_host=None):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    if remote_host:
        grid_nodes = f"http://{remote_host}:4444/wd/hub"
        driver = webdriver.Remote(command_executor=grid_nodes, options=chrome_options)
    else:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def fetch_data(driver, url, password):
    driver.get(url)
    password_input = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.NAME, "admin_Password"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(password_input).click().perform()
    password_input.send_keys(password + Keys.ENTER)
    WebDriverWait(driver, 30).until(
        EC.url_contains("Home.html")  # Replace with the actual URL or condition
    )

def download_data(driver, base_url):
    driver.get(f"{base_url}/all_country.txt")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    all_country_content = driver.page_source
    with open("all_country.txt", "w") as file:
        file.write(all_country_content)
    print("Download successful, saved as all_country.txt")
    return all_country_content

def read_json_data():
    try:
        with open('data.json', 'r') as json_file:
            json_data = json.load(json_file)
            return json_data["countryList"]
    except FileNotFoundError:
        print("Error: data.json not found.")
        exit()
    except json.JSONDecodeError:
        print("Error: data.json is not a valid JSON file.")
        exit()
    except Exception as e:
        errors.append(str(e))
        return None

def parse_txt_data(file_path):
    try:
        with open(file_path, 'r') as txt_file:
            lines = txt_file.readlines()
            data = []
            current_country = None
            for line in lines:
                line = line.strip()
                if line.startswith("Country = "):
                    current_country = line.split(" = ")[1].split(" ")[0]
                    country_data = {"Country": current_country}
                    data.append(country_data)
                elif current_country and "ChannelList 2G" in line:
                    if " = " in line:
                        channel_list_2g = list(map(int, line.split(" = ")[1].split(',')))
                        data[-1]["ChannelList_2G"] = channel_list_2g
                elif current_country and "ChannelList 5G" in line:
                    if " = " in line:
                        channel_list_5g = line.split(" = ")[1].strip()
                        if channel_list_5g:
                            data[-1]["ChannelList_5G"] = list(map(int, channel_list_5g.split(',')))
                        else:
                            data[-1]["ChannelList_5G"] = []
                elif current_country and "ChannelList_DFS 5G" in line:
                    if " = " in line:
                        channel_list_dfs_5g = line.split(" = ")[1].strip()
                        if channel_list_dfs_5g:
                            data[-1]["ChannelList_DFS 5G"] = list(map(int, channel_list_dfs_5g.split(',')))
                        else:
                            data[-1]["ChannelList_DFS 5G"] = []
        return data
    except Exception as e:
        errors.append(str(e))

def compare_channel_lists(country_list, parsed_txt_data):
    try:
        results = {}
        total_pass = total_fail = total_skip = 0
        skipped_countries = []
        country_count = defaultdict(int)
        
        for country_info in parsed_txt_data:
            country_count[country_info["Country"]] += 1

        for country_info in parsed_txt_data:
            country_name = country_info["Country"]
            if country_name not in country_list:
                print(f"SKIP: {country_name} not found in JSON data.")
                total_skip += 1
                skipped_countries.append(country_name)
                continue
            
            json_2g = country_list[country_name]["ChannelList_2G"]
            json_5g = country_list[country_name]["ChannelList_5G"]
            json_dfs_5g = country_list[country_name]["ChannelList_DFS 5G"]
            
            txt_2g = country_info.get("ChannelList_2G", [])
            txt_5g = country_info.get("ChannelList_5G", [])
            txt_dfs_5g = country_info.get("ChannelList_DFS 5G", [])
            
            result_2g = "PASS" if json_2g == txt_2g else "FAIL"
            result_5g = "PASS" if json_5g == txt_5g else "FAIL"
            result_dfs_5g = "PASS" if json_dfs_5g == txt_dfs_5g else "FAIL"
            
            results[country_name] = {
                "Country_Code_24G": country_list[country_name]["Country_Code_24G"],
                "Country_Code_5G": country_list[country_name]["Country_Code_5G"],
                "ChannelList_2G": {"result": result_2g, "json": json_2g, "txt": txt_2g},
                "ChannelList_5G": {"result": result_5g, "json": json_5g, "txt": txt_5g},
                "ChannelList_DFS 5G": {"result": result_dfs_5g, "json": json_dfs_5g, "txt": txt_dfs_5g},
            }

            total_pass += (result_2g == "PASS") + (result_5g == "PASS") + (result_dfs_5g == "PASS")
            total_fail += (result_2g == "FAIL") + (result_5g == "FAIL") + (result_dfs_5g == "FAIL")
        
        return results, total_pass, total_fail, total_skip, skipped_countries, country_count
    except Exception as e:
        errors.append(str(e))

def log_results(parsed_txt_data,comparison_result, total_pass, total_fail, total_skip, skipped_countries, country_count, json_data, errors, all_country_content):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'log_{current_time}.txt'
    with open(log_filename, 'w') as log_file:
        if not errors and parsed_txt_data:
            for country, result in comparison_result.items():
                log_file.write(f"Results for {country}:\n")
                log_file.write(f"  Country_Code_24G: {result['Country_Code_24G']}\n")
                log_file.write(f"  Country_Code_5G: {result['Country_Code_5G']}\n")
                for channel_type, details in result.items():
                    if channel_type in ["ChannelList_2G", "ChannelList_5G", "ChannelList_DFS 5G"]:
                        log_file.write(f"  {channel_type} comparison result: {details['result']}\n")
                        log_file.write(f"    Expected: {details['json']}\n")
                        log_file.write(f"    Found: {details['txt']}\n")
                log_file.write("\n")

            log_file.write("Total Results:\n")
            log_file.write(f"  Total PASS: {total_pass}\n")
            log_file.write(f"  Total FAIL: {total_fail}\n")
            log_file.write(f"  Total SKIP: {total_skip}\n")
            
            if skipped_countries:
                log_file.write("Skipped Countries:\n")
                for country in skipped_countries:
                    log_file.write(f"  {country}\n")

            log_file.write("Duplicate Countries:\n")
            for country, count in country_count.items():
                if count > 1:
                    log_file.write(f"  {country}: {count} times\n")

            reference_value = json_data.get("Reference", "Reference not found")
            log_file.write(f"Reference: {reference_value}\n")
        else:
            if all_country_content:
                errors.append(str(all_country_content))
            log_file.write(f"Results for Undefined:\n")
            log_file.write(f"  Undefined comparison result: FAIL\n")
            log_file.write(f"    Errors: {errors}\n")

    return log_filename

def main():
    global errors
    global all_country_content
    errors = []
    all_country_content = None
    args = parse_arguments()
    driver = setup_driver(args.remote)
    model = "Undefined" if not args.model else args.model
    fw = "Undefined" if not args.fw else args.fw
    

    try:
        base_url = "https://192.168.200.1"
        fetch_data(driver, base_url, args.password)
        all_country_content = download_data(driver, base_url)
    except Exception as e:
        errors.append(str(e))
    finally:
        driver.close()
        driver.quit()

    country_list = read_json_data()
    parsed_txt_data = parse_txt_data('all_country.txt')

    try:
        comparison_result, total_pass, total_fail, total_skip, skipped_countries, country_count = compare_channel_lists(country_list, parsed_txt_data)
    except Exception as e:
        comparison_result = None
        total_pass = 0
        total_fail = 0
        total_skip = 0
        country_count = {}
        skipped_countries = []
        errors.append(str(e))

    log_filename = log_results(parsed_txt_data, comparison_result, total_pass, total_fail, total_skip, skipped_countries, country_count, country_list, errors, all_country_content)

    with open(log_filename, 'r') as file:
        log_content = file.read()
    parsed_data = item_json.parse_log_content(log_content, log_filename, model, fw)
    item_json.write_json_to_file(parsed_data, log_filename.replace(".txt", ".json"))

    try:
        os.remove("all_country.txt")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()