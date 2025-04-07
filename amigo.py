import argparse
# 預設值
DUT_default_pwd = "yrntq43786"
DUT_modelName = "MS30"
DUT_admin_pwd = "admin12345"
ip = "200"
fw = None
remote = None
browser = None
def parse_arguments():
    global DUT_default_pwd, DUT_admin_pwd, DUT_modelName, fw, remote, browser
    parser = argparse.ArgumentParser(description='Fetch data from the router.')
    parser.add_argument('-default_pwd', type=str, help='Router default password')
    parser.add_argument('-admin_pwd', type=str, help='Router admin password')
    parser.add_argument('-remote', type=str, help='Selenium remote host')
    parser.add_argument('-model', type=str, help='Model name')
    parser.add_argument('-fw', type=str, help='Firmware version')
    parser.add_argument('-browser', type=str, default='chrome', help='Browser to use (default: chrome)')
    args = parser.parse_args()
    # 檢查 args 並設置預設值
    DUT_default_pwd = args.default_pwd if args.default_pwd else DUT_default_pwd
    DUT_admin_pwd = args.admin_pwd if args.admin_pwd else DUT_admin_pwd
    DUT_modelName = args.model if args.model else DUT_modelName
    fw = args.fw if args.fw else "Undefined"
    remote = args.remote
    browser = args.browser
    set_dut_wifi_info()

def set_dut_wifi_info():
    global DUTMAC, DUT_Wifi_SSID, DUT_Wifi_SSID6, CheckDUTWiFiName, url1, url2
    DUTMAC = "4DF0"
    DUT_Wifi_SSID = "AmigoAuto1"
    DUT_Wifi_SSID6 = "AmigoAuto1_6G"
    CheckDUTWiFiName = f"{DUT_modelName}-{DUTMAC}"
    url1 = f"http://{DUTMAC}.devicesetup.net/"
    url2 = f"http://{DUT_modelName}-{DUTMAC}.local/"
#################################################################################
#WLAN connect time
WiFi_time = 120

#MS30.MS60=300/M95=350
wizard_time = 300
reboot_time = 300
save_time = 300

#MS30.MS60=60/M95=120
button_time = 60

#MS30.MS60=5/M95=10
buffer_time = 5
#################################################################################
#網卡(有換電腦要改)
#筆電
hostname = "LAPTOP-OJ1O8HV7"
MACAddress = "10:7C:61:B9:BE:9B"
Lan1_MAC = "107c61b9be9b"
Lan2_MAC = "00e04c680a3b"
clientMac_wireless = '04:ec:d8:c8:85:f2'
wirelessClientName = 'Intel(R) Wi-Fi 6 AX201 160MHz'
#無線網卡
Wifi = 'Wi-Fi'
Lan1 = "乙太網路"
Lan2 = "乙太網路 2"
#uplink ip[如果沒接實驗室的DHCP就要改]
DNS_IP = "192.168.17.1"
Uplink_adminpwd = "admin123"
#################################################################################
#Telnet
SundayDate = 'date 2025-02-02'
MondayDate = 'date 2025-02-03'
#################################################################################
#(以下不太需要改動)
#vm = (1000, 700)
#windows = (1400,900)
W = 1400
H = 900
editData1 = "editData(1)"
editData2 = "editData(2)"
pcdevice0 = "pcdevice_chk_0"
pcdevice1 = "pcdevice_chk_1"
#################################################################################
#IP
DUT_GUI_url = f"http://192.168.{ip}.1"
Uplink_GUI_url = f"http://{DNS_IP}"
DUT_default_Lan_IP = f"192.168.{ip}.1"
client_PC = f"192.168.{ip}.145"
client1IP = f"192.168.{ip}.150"
client2IP = f"192.168.{ip}.160"
client3IP = f"192.168.{ip}.220"
DUT_clientRSIP = f"192.168.{ip}."
blocked_internet_pause = f"http://192.168.{ip}.1/__blocked_internet_pause.html"
versionTXT = f"http://192.168.{ip}.1/version.txt"
#################################################################################
#path
Log_folder = r"D:\Auto\TestReport"
New_auto_folder = r"D:\Auto"
all_file_path = r"D:\python\AmigoAuto"
download_path = r"C:\Users\user\Downloads"
Result_log = r"D:\Auto\TestReport\Result_log.txt"
wifiinfoview_path = r"C:\Users\user\Downloads\wifiinfoview-x64\WifiInfoView.exe"
TERATERM_PATH = r"C:\Program Files (x86)\teraterm\ttermpro.exe"
wireshark_path = r'C:\Program Files\Wireshark\tshark.exe'
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
pytesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Wireshark = r"C:\Program Files\Wireshark\wireshark.exe"
WiFi_pwd = "admin12345"
#CHT
#"77335509@ip.hinet.net"
CHT_name = "77335509@hinet.net"
CHT_static_name = "77335509@ip.hinet.net"
CHT_pwd = "jijhkwfp"
CHT_static = "122.117.181.240"
#L2TP
L2TP_Server = "192.168.77.23"
userName_L2TP = "amigotp"
password_L2TP = "amigotp"
#PPTP
PPTP_Server = "192.168.77.23"
userName_PPTP = "amigopp"
password_PPTP = "amigopp"
#################################################################################
#不同系列DUT圖片的編碼可能不一樣(深藍色GUI-AQUILA PRO AI/淺藍色GUI-EAGLE PRO AI)
#1
#HomeRouterWiFi(首頁DUT的圖片)
#MS60.MS30
#v=2ff9a9bd40
#RM18
#v=1bdaebd234
#M95
#v=132d2445ce
HomeRouterWiFi = 'img[src="image/router-wifi.png?v=2ff9a9bd40"]'


#2
#HomeConnected(綠色勾勾)
#MS60.MS30.M95
#v=7ddc815576
#RM18.G415
#v=c3d3a4b979
HomeConnected = 'img[src="/image/connected.png?v=7ddc815576"]'

#3
#HomeDisconnected(紅色叉叉)
#MS60.MS30.M95
#v=3fa28a3216
#RM18.G415
#v = 3e3747ccf7
HomeDisconnected = 'img[src="/image/disconnected.png?v=3fa28a3216"]'


#4
#EditIcon(筆)
#MS60.MS30.RM18.M95
#v=2fc10c4616
EditIcon = "//img[contains(@src, 'edit_btn.png?v=2fc10c4616')]"


#5
#RemoveIcon(垃圾桶)
#MS60.MS30.RM18.M95
#v=8fee37bb10
RemoveIcon = "//img[contains(@src, 'trash.png?v=8fee37bb10')]"
#################################################################################
'''
1.Pwd:012 34 56 aA
AmigoAuto1_GuestZone 34 56 _-Ab@
012 34 56 aA_24GHz
012 34 56 aA_5GHz

2.pwd:~!@#$% ^&*()_+1a
~!@#$% ^&*()_+1a

3.
-i~[-=)<-i~[-i=#$>('~;)*
-i~[-=)<-i~[-i=#$>('~;)*_ac3
-i~[-=)<-i~[-i=#$>('~;)*_ac23
00012 34 56 _-ABCabc0123嗨嗨

4.
AmigoAuto1(none)
AmigoAuto1_GuestZone(none)
AmigoAuto1_GuestZone5GHz(none)
AmigoAuto1_GuestZone24GHz(none)

5.
AmigoAuto1
AmigoAuto1_5GHz
AmigoAuto1_24GHz
AmigoAuto1_WPA3_5
AmigoAuto1_GuestZone
AmigoAuto1_GuestZone5GHz
AmigoAuto1_GuestZone24GHz
AmigoAuto1_bgn
AmigoAuto1_gn
'''



###
'''
##實驗室電腦Auto-B(左)
DUT_Wifi_SSID = "AmigoAuto"
DUT_Wifi_SSID6 = "AmigoAuto_6G"
#################################################################################
hostname = "Auto-B"
MACAddress = "84:69:93:80:E5:33"
Lan1_MAC = "84699380E533"
Lan2_MAC = "00e04c683ee4"
clientMac_wireless = 'a4:2a:95:45:1c:73'
wirelessClientName = 'DWA-X1850'
#無線網卡
Wifi = 'Wi-Fi'
Lan1 = "乙太網路"
Lan2 = "乙太網路 3"



##實驗室電腦Auto-A(右)
DUT_Wifi_SSID = "AmigoAuto3"
DUT_Wifi_SSID6 = "AmigoAuto3_6G"
#################################################################################
hostname = "AUTO-A"
MACAddress = "84:69:93:80:e8:e3"
Lan1_MAC = "84699380e8e3"
Lan2_MAC = "00e04c681efC"
clientMac_wireless = 'c8:cb:9e:ee:81:62'
wirelessClientName = 'Intel(R) Wireless-AC 9462'
#無線網卡
Wifi = 'Wi-Fi 1'
Lan1 = "乙太網路"
Lan2 = "乙太網路 2"



#筆電_acer
DUT_Wifi_SSID = "AmigoAuto2"
DUT_Wifi_SSID6 = "AmigoAuto2_6G"
#################################################################################
hostname = "LAPTOP-L9EGCT5O"
MACAddress = "08:8F:C3:4C:55:4A"
Lan1_MAC = "088fc34c554a"
Lan2_MAC = "00e04c683ec7"
clientMac_wireless = '4c:03:4f:db:da:49'
wirelessClientName = 'Intel(R) Wi-Fi 6 AX201 160MHz'
#無線網卡
Wifi = 'Wi-Fi'
Lan1 = "乙太網路"
Lan2 = "乙太網路 3"



#筆電_ASUS
DUT_Wifi_SSID = "AmigoAuto1"
DUT_Wifi_SSID6 = "AmigoAuto1_6G"
#################################################################################
hostname = "LAPTOP-OJ1O8HV7"
MACAddress = "10:7C:61:B9:BE:9B"
Lan1_MAC = "107c61b9be9b"
Lan2_MAC = "00e04c680a3b"
clientMac_wireless = '04:ec:d8:c8:85:f2'
wirelessClientName = 'Intel(R) Wi-Fi 6 AX201 160MHz'
#無線網卡
Wifi = 'Wi-Fi'
Lan1 = "乙太網路"
Lan2 = "乙太網路2"
'''