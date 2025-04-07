from module.auto_click import *
from selenium.webdriver.support.ui import Select
import FunctionForTestPlan
import FunctionForTestPlan2
import datetime
a.parse_arguments()
start_time = time.time()
time.sleep(5)
is_passed = True
try:
    print("DKP1611020-0036")
    
    #Factory Reset
    print("\n+++++ 01.Reset DUT +++++\n")
    result_restorToFactoryDefault, execution_time, current_time = FunctionForTestPlan.restorToFactoryDefault()
    
    #DHCP Default Wizard
    print("\n+++++ 02.DHCP Default Wizard +++++\n")
    result_DHCPDefaultWizard, execution_time, current_time = FunctionForTestPlan.DHCPDefaultWizard()
    
    #run_DownLan
    print("\n+++++ 03.run_DownLan +++++\n")
    result_DownLan, execution_time, current_time = FunctionForTestPlan.run_DownLan()

    #run_UpLan
    print("\n+++++ 04.run_UpLan +++++\n")
    result_UpLan, execution_time, current_time = FunctionForTestPlan.run_UpLan()
    time.sleep(10)
    
    #dns_mdns_packet_handler
    print("\n+++++ 05.dns_mdns_packet_handler +++++\n")
    result_dns_mdns_packet_handler, execution_time, current_time = FunctionForTestPlan2.dns_mdns_packet_handler()
    
    #check_packets
    print("\n+++++ 06.check_packets +++++\n")
    result_check_packets, execution_time, current_time = FunctionForTestPlan2.check_packets("mdns_packets.txt",a.hostname)
    
    DKP_folder = 'DKP1611020-0036'
    FunctionForTestPlan.move_files(DKP_folder)

except Exception:
    print("\n+++++ False +++++\n")
    is_passed = False
finally:
    end_time = time.time()
    execution_time = end_time - start_time
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = "07NetworkDKP1611020_0036Network_log.txt"
    import amigo as a
    log_file_path = os.path.join(a.all_file_path, log_filename)
    with open(log_file_path, "w", encoding="big5") as log_file:
        with open(log_file_path, "a", encoding="big5") as f:
            f.write(f"01:{result_restorToFactoryDefault}\n")
            f.write(f"02:{result_DHCPDefaultWizard}\n")
            f.write(f"03.{result_DownLan}\n")
            f.write(f"04.{result_UpLan}\n")
            f.write(f"05.{result_dns_mdns_packet_handler}\n")
            f.write(f"06.{result_check_packets}\n")
            if is_passed == True:
                f.write("DKP1611020-0036.Result: Pass\n")
            else:
                f.write("DKP1611020-0036.Result: Fail\n")
            f.write("Execution Time: {} seconds\n".format(execution_time))
            f.write("Current Time: {}\n".format(current_time))