import json
import re

def parse_log_content(log_content, log_file_name, model, firmware):
    """Parse content of a log file and return a list of dictionaries."""

    # Initialize variables
    test_plan = "country channel"
    test_item_number = 1
    countries = []
    current_country = None

    for line in log_content.splitlines():
        # Detecting the country (which will be used as the "value" in "Test Case")
        match = re.match(r"Results for (.+):", line)
        if match:
            country_name = match.group(1).strip()
            continue

        # Detecting and storing test items and their results
        if "comparison result" in line:
            test_item_name = line.split("comparison result")[0].strip()

            # Save the previous country
            if current_country:
                countries.append(current_country)

            # Initialize the current country
            current_country = {
                "Test Plan": test_plan,
                "Test Case": country_name,
                "Test item": {
                    "no": test_item_number,
                    "name": test_item_name,
                    "detail": {}
                },
                "Result": "",
                "Log file": log_file_name,
                "Model": model,
                "Firmware": firmware
            }

            # Parse the result
            result = line.split(":")[1].strip()
            current_country["Result"] = result

            test_item_number += 1
            continue

        # Detecting and storing the expected and found details for the test items
        if "Expected" in line or "Found" in line or "Errors" in line:
            key, value = line.split(": ", 1)
            value_list = [x.strip() for x in value.strip("[]").split(",") if x.strip()]
            current_country["Test item"]["detail"][key.strip()] = value_list

    # Add the last processed country to the list
    if current_country:
        countries.append(current_country)

    # Return the list of all countries
    return countries

def write_json_to_file(json_data, file_path):
    with open(file_path, 'w') as json_file:
        for entry in json_data:
            json.dump(entry, json_file)
            json_file.write('\n')  # Write each JSON object to a new line
if __name__ == "__main__":
    
    # Load the log file and convert to JSON
    log_file_path = 'log_20240823_172829.txt'  # Update this with your log file path
    with open(log_file_path, 'r') as file:
        log_content = file.read()
    
    # Parse log content
    parsed_data = parse_log_content(log_content,"log_20240823_172829.txt", "MS30", "1.00B99")
    
    # Write JSON result to a file, one "Test Plan" per line
    write_json_to_file(parsed_data, 'converted_log.json')
    
    #Print the JSON result (for verification)
    for entry in parsed_data:
        print(json.dumps(entry, indent=2))
    
