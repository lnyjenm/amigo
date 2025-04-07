from module.auto_click import *
from selenium.webdriver.support.ui import Select
import FunctionForTestPlan
import datetime
a.parse_arguments()
start_time = time.time()
time.sleep(5)
is_passed = True
try:
    print("DKP1611004-0001")
    
    #Factory Reset
    print("\n+++++ 01.Reset DUT +++++\n")
    result_restorToFactoryDefault, execution_time, current_time = FunctionForTestPlan.restorToFactoryDefault()
    
    #DHCP Default Wizard
    print("\n+++++ 02.Run DHCP Default Wizard +++++\n")
    result_DHCPDefaultWizard, execution_time, current_time = FunctionForTestPlan.DHCPDefaultWizard()
    
    #Add 6 website with parental concrol profile
    print("\n+++++ 03.Parental control profile  add website +++++\n")
    result_AddWebsite, execution_time, current_time = FunctionForTestPlan.AddWebsite()
    
    #Check 3 Restricted website
    print("\n+++++ 04.Check Restricted website +++++\n")
    result_CheckRestrictedWeb, execution_time, current_time = FunctionForTestPlan.CheckRestrictedWeb()
    
    #Remove Rule
    print("\n+++++ 05.Remove Rule +++++\n")
    result_RemoveProfile, execution_time, current_time = FunctionForTestPlan.RemoveProfile()
    
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
    with open(log_file_path, "w", encoding="big5") as log_file:
        with open(log_file_path, "a", encoding="big5") as f:
            f.write(f"TestCase:DKP1611004-0001\n")
            f.write(f"01:{result_restorToFactoryDefault}\n")
            f.write(f"02:{result_DHCPDefaultWizard}\n")
            f.write(f"03:{result_AddWebsite}\n")
            f.write(f"04:{result_CheckRestrictedWeb}\n")
            f.write(f"05:{result_RemoveProfile}\n")
            if is_passed == True:
                f.write("DKP1611004_0001.Result: Pass\n")
            else:
                f.write("DKP1611004_0001.Result: Fail\n")
            f.write("Execution Time: {} seconds\n".format(execution_time))
            f.write("Current Time: {}\n".format(current_time))