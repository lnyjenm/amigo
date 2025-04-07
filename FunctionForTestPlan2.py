from module.auto_click import *
import amigo as a
import datetime
import os
from urllib.parse import urlparse
import timedelta
from datetime import datetime, timedelta
from scapy.all import rdpcap, wrpcap
import re
import logging
import FunctionForTestPlan
from scapy.all import *
from scapy.layers.dhcp import DHCP
from scapy.layers.dns import DNS
from scapy.layers.inet import UDP
from scapy.layers.inet6 import ICMPv6EchoRequest, ICMPv6EchoReply,ICMPv6ND_RA
import threading
'''
def release_renew_network_interface(interface_name):
    try:
        release_command = f'ipconfig /release {interface_name}'
        renew_command = f'ipconfig /renew {interface_name}'
        subprocess.run(release_command, shell=True, check=True)
        subprocess.run(renew_command, shell=True, check=True)
        print(f"Released and renewed network interface: {interface_name}")
    except Exception as e:
        print(f"Error releasing and renewing network interface: {e}")

def capture_bootp_packets(duration=300):
    try:
        start_time = time.time()
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        wireshark_path = a.wireshark_path
        network_interface = "乙太網路"
        output_directory = a.all_file_path
        release_renew_network_interface(network_interface)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        output_file_path = os.path.join(output_directory, 'captured_packets.pcap')
        wireshark_command = f'"{wireshark_path}" -i {network_interface} -a duration:{duration} -w {output_file_path} -p'
        subprocess.run(wireshark_command, shell=True, check=True)
        print(f"Captured packets with Wireshark in {duration} seconds and saved to {output_file_path}")
        result_capture_bootp_packets = True
        print("Finish.")
    except Exception as e:
        print(e)
        print("\n+++++ False +++++\n")
        result_capture_bootp_packets = False
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return result_capture_bootp_packets, execution_time, current_time
    
def convert_pcap_to_txt(pcap_file_path, txt_file_path):
    try:
        tshark_path = a.wireshark_path
        tshark_command = f'"{tshark_path}" -r {pcap_file_path} -T fields -e ip.src -e ip.dst -e udp.srcport -e udp.dstport -E header=y -E separator=, > {txt_file_path}'
        subprocess.run(tshark_command, shell=True, check=True)
        print(f"Converted pcap file to txt: {txt_file_path}")
    except Exception as e:
        print(f"Error converting pcap to txt: {e}")

def search_ip_in_txt(txt_file_path, target_ip):
    found_target_ip = False
    try:
        with open(txt_file_path, 'r') as txt_file:
            for line in txt_file:
                if target_ip in line:
                    found_target_ip = True
                    break
    except Exception as e:
        print(f"Error searching IP in txt file: {e}")
    return found_target_ip
pcap_file_path = a.all_file_path +'\captured_packets.pcap'
txt_file_path = a.all_file_path +'\captured_packets.txt'
target_ip = '255.255.255.255'
convert_pcap_to_txt(pcap_file_path, txt_file_path)
if search_ip_in_txt(txt_file_path, target_ip):
    print(f"IP {target_ip} found in the text file.")
else:
    print(f"IP {target_ip} not found in the text file.")
'''

def TimeDifferenceTXT():
    file_path = f"{a.Log_folder}\\TimeDifferenceTXT.log"
    logger = FunctionForTestPlan.setup_logger(file_path)
    logger.info("Log message for TimeDifferenceTXT")
    start_time = time.time()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_TimeDifferenceTXT = False

    try:
        time.sleep(10)
        with open("ipconfigall.txt", "r", encoding="utf-8") as file:
            ipconfig_text = file.read()

        print("Contents of ipconfig_text:")
        print(ipconfig_text)

        lease_start_match = re.search(r'租用取得.*?(\d{4}年\d{1,2}月\d{1,2}日 (上午|下午) (\d{2}:\d{2}:\d{2}))', ipconfig_text)
        lease_end_match = re.search(r'租用到期.*?(\d{4}年\d{1,2}月\d{1,2}日 (上午|下午) (\d{2}:\d{2}:\d{2}))', ipconfig_text)

        if lease_start_match and lease_end_match:
            lease_start_str = lease_start_match.group(1)
            lease_end_str = lease_end_match.group(1)
            if "下午" in lease_start_str:
                datetime_format1 = "%Y年%m月%d日 下午 %I:%M:%S"
            else:
                datetime_format1 = "%Y年%m月%d日 上午 %I:%M:%S"
            if "下午" in lease_end_str:
                datetime_format2 = "%Y年%m月%d日 下午 %I:%M:%S"
            else:
                datetime_format2 = "%Y年%m月%d日 上午 %I:%M:%S"
            lease_start = datetime.strptime(lease_start_str, datetime_format1)
            lease_end = datetime.strptime(lease_end_str, datetime_format2)
            time_difference = lease_end - lease_start
            ten_minutes = timedelta(minutes=10)
            allowed_deviation = timedelta(seconds=30)

            print(f"Calculated Time Difference: {time_difference}")

            if abs(time_difference - ten_minutes) <= allowed_deviation:
                logger.info("Pass. DHCP lease time is within 10 minutes with a deviation of 30 seconds.")
                print("Pass.")
                result_TimeDifferenceTXT = True
            else:
                logger.error(f"Fail. {time_difference}")
                print("Fail.")
                result_TimeDifferenceTXT = False

        else:
            logger.error("Failed to extract lease start or end time from ipconfig_text.")
            print("Fail.")
            result_TimeDifferenceTXT = False

        directory, filename = os.path.split("ipconfigall.txt")
        new_filename = "ipconfigall_" + current_time + ".txt"
        new_filepath = os.path.join(directory, new_filename)
        os.rename("ipconfigall.txt", new_filepath)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print("\n+++++ False +++++\n")
        result_TimeDifferenceTXT = False

    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution Time:", execution_time, "seconds")
        print("Current Time:", current_time)
        logging.shutdown()
        return result_TimeDifferenceTXT, execution_time, current_time

def release_and_renew_ip():
    print("release IP...")
    subprocess.run(["ipconfig", "/release"], capture_output=True, text=True)
    time.sleep(5)
    print("renew IP...")
    subprocess.run(["ipconfig", "/renew"], capture_output=True, text=True)
    time.sleep(5)
def capture_dhcp_packets(options=1):
    start_time = time.time()
    result_capture_dhcp_discover_packets = False
    try:
        captured_packets = []
        def packet_callback(packet):
            if packet.haslayer(DHCP):
                dhcp_layer = packet[DHCP]
                if dhcp_layer.options[0][1] == options:
                    packet_info = f"Captured Packet:\n{packet.summary()}\n{packet.show(dump=True)}\n\n"
                    captured_packets.append(packet_info)
                    print(packet_info)
        ip_thread = threading.Thread(target=release_and_renew_ip)
        ip_thread.start()
        print("Start capturing DHCP Discover packets for 10 seconds...")
        end_time = time.time() + 10
        while time.time() < end_time:
            sniff(iface=a.Lan1, filter="udp and (port 67 or port 68)", prn=packet_callback, store=0, timeout=1)
        ip_thread.join()
        with open("dhcp_discover_packets.txt", "w") as f:
            f.writelines(captured_packets)
        print("Capture is complete and packets have been saved to dhcp_discover_packets.txt.")
        result_capture_dhcp_discover_packets = True
    except Exception as e:
        print(e)
        result_capture_dhcp_discover_packets = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return result_capture_dhcp_discover_packets, execution_time, current_time
def capture_dhcp_discover_packets():
    return capture_dhcp_packets(options=1)
def capture_dhcp_ACK_packets():
    return capture_dhcp_packets(options=5)
def check_packets(filename, search_term):
    start_time = time.time()
    result_check_packets = False
    try:
        with open(filename, "r") as f:
            content = f.read()
            if search_term in content:
                print(f"Pass.Found {search_term}.")
                result_check_packets = True
            else:
                print(f"Fail.Not found {search_term}")
                result_check_packets = False
    except FileNotFoundError:
        print("Fail.FileNotFoundError")
        result_check_packets = False
    except Exception as e:
        print(e)
        result_check_packets = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} has been deleted.")
        return result_check_packets, execution_time, current_time
    
def check_packets_NOTFound(filename, search_term):
    start_time = time.time()
    result_check_packets_NOTFound = False
    try:
        with open(filename, "r") as f:
            content = f.read()
            if search_term in content:
                print(f"Fail.Found {search_term}")
                result_check_packets_NOTFound = False
            else:
                print(f"Pass.Not Found {search_term}.")
                result_check_packets_NOTFound = True
    except FileNotFoundError:
        print("Fail.FileNotFoundError")
        result_check_packets_NOTFound = False
    except Exception as e:
        print(e)
        result_check_packets_NOTFound = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} has been deleted.")
        return result_check_packets_NOTFound, execution_time, current_time
'''
#Scapy
#常用過濾器
#1.IP 地址過濾
#捕獲特定源或目的 IP 的封包：
sniff(filter="ip src 192.168.1.1")
sniff(filter="ip dst 192.168.1.1")

#2.協議過濾
#捕獲特定協議的封包：
sniff(filter="tcp")
sniff(filter="udp")
sniff(filter="icmp")

#3.端口過濾
#捕獲特定端口的封包：
sniff(filter="tcp port 80")
sniff(filter="udp port 53")

#4.組合過濾
#組合多個條件：
sniff(filter="tcp and src port 80")
sniff(filter="ip and (src host 192.168.1.1 or dst host 192.168.1.2)") 

#5.排除過濾
#排除特定條件的封包：
sniff(filter="not tcp")

#1.物理層 (Layer 1)
#2.數據鏈路層 (Layer 2)
sniff(filter="ether", prn=lambda x: x.show())
#3.網路層 (Layer 3)
sniff(filter="ip", prn=lambda x: x.show())
#4.傳輸層 (Layer 4)
sniff(filter="tcp or udp", prn=lambda x: x.show())
#5.應用層 (Layer 7)
sniff(filter="tcp port 80", prn=lambda x: x.show())  # 捕獲 HTTP 封包

#Ethernet/IP/TCP/UDP/ICMP/ARP/DHCP/DNS
packet.haslayer(TCP)
'''
def dns_mdns_packet_handler(capture_duration=10, iface=a.Lan1):
    start_time = time.time()
    result_dns_mdns_packet_handler = False
    try:
        captured_packets = []
        def packet_callback(packet):
            if packet.haslayer(DNS) and packet[DNS].qr == 0:
                print(f"Received mDNS packet: {packet.summary()}")
                packet_info = f"Captured Packet:\n{packet.summary()}\n{packet.show(dump=True)}\n\n"
                captured_packets.append(packet_info)
                print(packet_info)
        ip_thread = threading.Thread(target=release_and_renew_ip)
        ip_thread.start()
        print("Start capturing mdns packets for 10 seconds...")
        end_time = time.time() + capture_duration
        while time.time() < end_time:
            sniff(iface=iface, filter="udp and port 5353", prn=packet_callback, store=0, timeout=1)
        ip_thread.join()
        with open("mdns_packets.txt", "w") as f:
            f.writelines(captured_packets)
        print("Capture is complete and packets have been saved to mdns_packets.txt.")
        result_dns_mdns_packet_handler = True
    except Exception as e:
        print(e)
        result_dns_mdns_packet_handler = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return result_dns_mdns_packet_handler, execution_time, current_time

def ra_packet_handler(capture_duration):
    start_time = time.time()
    result_ra_packet_handler = False
    try:
        captured_packets = []
        def packet_callback(packet):
            if packet.haslayer(ICMPv6ND_RA):
                elapsed_time = time.time() - start_time
                packet_info = f"Received ICMPv6 packet at {elapsed_time:.2f} seconds: {packet.summary()}\n"
                detailed_info = f"Captured Packet:\n{packet.summary()}\n{packet.show(dump=True)}\n\n"
                captured_packets.append(packet_info + detailed_info)
                print(packet_info + detailed_info)
        ip_thread = threading.Thread(target=release_and_renew_ip)
        ip_thread.start()
        print(f"Start capturing ICMPv6 packets for {capture_duration} seconds...")
        end_time = time.time() + capture_duration
        while time.time() < end_time:
            sniff(iface=a.Lan1, filter="icmp6", prn=packet_callback, store=0, timeout=1)
        with open("ICMPv6_packets.txt", "w") as f:
            f.writelines(captured_packets)
        print("Capture is complete and packets have been saved to ICMPv6_packets.txt.")
        result_ra_packet_handler = True
    except Exception as e:
        print(e)
        result_ra_packet_handler = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return result_ra_packet_handler, execution_time, current_time

def checkv6PK(filename, expected_m="0", expected_o="1"):
    start_time = time.time()
    expected_values = {"m": expected_m, "o": expected_o}
    result_checkv6PK = []
    found_router_advertisement_count = 0 
    try:
        with open(filename, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip().replace(' ', '').lower()
                if "routeradvertisement" in line:
                    found_router_advertisement_count += 1
                    print(f"Found Router Advertisement #{found_router_advertisement_count} at line {line_number}.")
                if "m=" in line or "o=" in line:
                    key_value = line.split('=')
                    if len(key_value) == 2:
                        key, value = key_value
                        if key == "m":
                            if value != expected_values["m"]:
                                print(f"Error: Found M={value}, expected M={expected_values['m']} at line {line_number}.")
                                result_checkv6PK.append(False)
                            else:
                                print(f"Correct: M={value} at line {line_number}.")
                                result_checkv6PK.append(True)
                        elif key == "o":
                            if value != expected_values["o"]:
                                print(f"Error: Found O={value}, expected O={expected_values['o']} at line {line_number}.")
                                result_checkv6PK.append(False)
                            else:
                                print(f"Correct: O={value} at line {line_number}.")
                                result_checkv6PK.append(True)
    except Exception as e:
        print(e)
        print("\n+++++ False +++++\n")
        time.sleep(5)
        result_checkv6PK = False
    finally:
        print(result_checkv6PK)
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} has been deleted.")
        return result_checkv6PK, execution_time, current_time

def SLAACstateless(expected_m="0", expected_o="1"):
    return checkv6PK('ICMPv6_packets.txt', expected_m, expected_o)
def SLAACRDNSS(expected_m="0", expected_o="0"):
    return checkv6PK('ICMPv6_packets.txt', expected_m, expected_o)
def StatefulDHCPv6(expected_m="1", expected_o="1"):
    return checkv6PK('ICMPv6_packets.txt', expected_m, expected_o)

def capture_llmnr_packets(capture_duration=120, iface=a.Lan1):
    start_time = time.time()
    result_capture_llmnr_packets = False
    try:
        captured_packets = []
        def packet_callback(packet):
            if packet.haslayer(UDP) and packet[UDP].dport == 5355:
                packet_info = f"Captured Packet:\n{packet.summary()}\n{packet.show(dump=True)}\n\n"
                captured_packets.append(packet_info)
                print(packet_info)
        print(f"Start capturing LLMNR packets for {capture_duration} seconds...")
        end_time = time.time() + capture_duration
        while time.time() < end_time:
            sniff(iface=iface, filter="udp and port 5355", prn=packet_callback, store=0, timeout=1)
        
        with open("llmnr_packets.txt", "w") as f:
            f.writelines(captured_packets)
        print("Capture is complete and packets have been saved to llmnr_packets.txt.")
        result_capture_llmnr_packets = True
    except Exception as e:
        print(e)
        result_capture_llmnr_packets = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return result_capture_llmnr_packets, execution_time, current_time

def check_packet_times(file_name):
    start_time = time.time()
    result_check_packet_times = []
    valid_packets = []
    invalid_packets = []
    elapsed_times = []
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
        pattern = r"Received ICMPv6 packet at ([\d.]+) seconds:"
        for line in lines:
            match = re.search(pattern, line)
            if match:
                elapsed_time = float(match.group(1))
                elapsed_times.append(elapsed_time)
                if 100 <= elapsed_time <= 650:
                    valid_packets.append(line.strip())
                    result_check_packet_times.append(True)
                else:
                    invalid_packets.append(line.strip())
                    result_check_packet_times.append(False)
        if valid_packets:
            print("Valid packets found within the range of 100 to 650 seconds:")
            for packet in valid_packets:
                result_check_packet_times.append(True)
        else:
            print("No valid packets found within the specified range.")
            result_check_packet_times.append(False)
        print("All elapsed times:")
        for Time in elapsed_times:
            status = "Valid" if 100 <= Time <= 650 else "Invalid"
            print(f"Elapsed time: {Time:.2f} seconds - Status: {status}")
        if invalid_packets:
            print("Invalid packets found:")
            for packet in invalid_packets:
                result_check_packet_times = False
    except Exception as e:
        print(e)
        result_check_packet_times = False
        print("\n+++++ False +++++\n")
        time.sleep(5)
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(result_check_packet_times)
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"{file_name} has been deleted.")
        return result_check_packet_times, execution_time, current_time