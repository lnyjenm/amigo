import json

def parse_results_to_json(log_file_path, test_plan, model, firmware, correct_count, incorrect_count):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    results = []
    current_item_no = 1

    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("Results for"):
            test_case = line.split("for ")[1]
        elif line.endswith("result: PASS") or line.endswith("result: Fail") or line.endswith("result: Skipped"):
            result = line.split("result: ")[1]
            item_name = line.split("_comparison result")[0].strip()
            
            # 確保有下一行可讀取，並讀取期望值行和實際值行
            if i + 1 < len(lines):
                expected_line = lines[i + 1].strip()  # 讀取期望值行
            if i + 2 < len(lines):
                found_line = lines[i + 2].strip()     # 讀取實際值行

            expected = expected_line.split("Expected: ")[1].strip("[]").split(",")
            found = found_line.split("Found: ")[1].strip("[]").split(",")

            # 構建 JSON 結構
            test_item = {
                "Test Plan": test_plan,
                "Test Case": test_case,
                "Test item": {
                    "no": current_item_no,
                    "name": item_name,
                    "detail": {
                        "Expected": [exp.strip() for exp in expected],
                        "Found": [f.strip() for f in found]
                    }
                },
                "Result": result,
                "Log file": log_file_path,
                "Model": model,
                "Firmware": firmware,
                "Statistics": {
                    "PASS": correct_count,
                    "Fail": incorrect_count,
                }
            }

            results.append(test_item)
            current_item_no += 1

    # 輸出到 JSON 檔案，每個項目一行
    with open('results.json', 'w') as json_file:
        for item in results:
            json_file.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("結果已成功轉換為 JSON 格式並儲存至 results.json")

# 如果需要單獨執行該檔案，可以添加以下代碼
if __name__ == "__main__":
    log_file_path = 'log_.txt'  # 輸入的 log 檔案
    test_plan = "country channel"
    model = "MS30"
    firmware = "1.00B99"

    # 這裡的參數需要根據實際情況調整
    correct_count = 0
    incorrect_count = 0

    parse_results_to_json(log_file_path, test_plan, model, firmware, correct_count, incorrect_count)
