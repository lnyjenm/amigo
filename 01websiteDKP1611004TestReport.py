import os
import re
import datetime
import shutil
import sys
import amigo as a
sys.path.append(a.all_file_path)

base_path = a.all_file_path

log_paths = [
    f"{base_path}\\01websiteDKP1611004_0001website_log.txt",
    ]


result_pattern = r"Result: (\w+)"
results = []

for log_path in log_paths:
    try:
        match = re.search(r"(\d{4})website", log_path)
        if match:
            schedule_number = match.group(1)
            with open(log_path, "r") as f:
                content = f.read()
                if not content:
                    results.append((schedule_number, "Fail (File is empty)"))
                else:
                    fail_or_false_count = content.count("Fail") + content.count("False")
                    if fail_or_false_count == 0 and "Execution Time" in content:
                        results.append((schedule_number, "Pass"))
                    else:
                        results.append((schedule_number, "Fail"))
    except FileNotFoundError:
        continue

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
auto_folder = a.New_auto_folder
report_folder_name = "TestReport"
report_folder = os.path.join(auto_folder, report_folder_name)
os.makedirs(report_folder, exist_ok=True)

# Write results to a text file
result_file_path = os.path.join(report_folder, "Result_log.txt")
if os.path.exists(result_file_path):
    mode = "a"  # Append mode if the file already exists
else:
    mode = "w"  # Write mode if the file doesn't exist

with open(result_file_path, mode) as f:
    for r in results:
        f.write(f"DKP1611004-{r[0]}, {r[1]}\n")

# Move log files to the report folder and rename them
for log_path in log_paths:
    try:
        match = re.search(r"(\d{4})website", log_path)
        if match:
            schedule_number = match.group(1)
            log_name = f"DKP1611004-{schedule_number}-log.txt"
            log_file_path = os.path.join(report_folder, log_name)

            # Check if the log file already exists
            if os.path.exists(log_file_path):
                log_file_path = os.path.join(report_folder, f"DKP1611004-{schedule_number}_{current_time}-log.txt")

            shutil.move(log_path, log_file_path)
    except FileNotFoundError:
        continue
