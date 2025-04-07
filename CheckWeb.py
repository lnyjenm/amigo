from module.auto_click import *
from selenium.webdriver.support.ui import Select
import FunctionForTestPlan
import datetime
a.parse_arguments()
start_time = time.time()
time.sleep(5)
is_passed = True
try:
    print("\n+++++ 06.Check 3 website +++++\n")
    result_CheckWeb, execution_time, current_time = FunctionForTestPlan.CheckWeb()
    DKP_folder = 'DKP1611004-0001'
    FunctionForTestPlan.move_files(DKP_folder)
except Exception:
    print("\n+++++ False +++++\n")
    is_passed = False
finally:
    end_time = time.time()
    execution_time = end_time - start_time
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = "01websiteDKP1611004_0001website_log.txt"
    import amigo as a
    log_file_path = os.path.join(a.all_file_path, log_filename)
    with open(log_file_path, "a", encoding="big5") as log_file:
        with open(log_file_path, "a", encoding="big5") as f:
            f.write(f"06:{result_CheckWeb}\n")
            if is_passed == True:
                f.write("DKP1611004_0001.Result: Pass\n")
            else:
                f.write("DKP1611004_0001.Result: Fail\n")
            f.write("Execution Time: {} seconds\n".format(execution_time))
            f.write("Current Time: {}\n".format(current_time))