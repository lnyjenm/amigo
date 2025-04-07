from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from PIL import Image
import time, os, pytesseract
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import urllib3
import amigo as a
from selenium.webdriver.chrome.service import Service
second = 3

class OCRFailedError(Exception):
    pass

class Dlink:
    _driver = None

    def __init__(self, w=None, h=None, browser='chrome'):
        import amigo as a

        if w is not None and h is not None:
            self.w = w
            self.h = h
        else:
            self.w = a.W
            self.h = a.H
        if Dlink._driver is None:
            if browser == 'chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = a.chrome_path
                chrome_options_prefs = {
                    "download.default_directory": a.download_path,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True
                }
                chrome_options.add_experimental_option("prefs", chrome_options_prefs)
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_argument('--incognito')
                #chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                service = Service()
                # 定義要嘗試的Selenium Grid節點列表
                # 省略其他部分
                grid_nodes = [
                    f"http://{a.remote}:4444/wd/hub",
                    #'http://cdr-ms30:4444/wd/hub',
                    #'http://dhm-ms30.amigo.tp:4444/wd/hub',
                    #'http://192.168.77.122:4444/wd/hub'
                ]

                for node_url in grid_nodes:
                    try:
                        Dlink._driver = webdriver.Remote(
                            command_executor=node_url,
                            options=chrome_options,
                        )
                        print(f"Connected to Selenium Grid at {node_url}")
                        break  # 如果成功連接，則停止嘗試其他節點
                    except Exception as e:
                        print(f"Failed to connect to Selenium Grid at {node_url}. Error: {str(e)}. Trying the next node...")

                # 如果所有節點都失敗，則使用本地 WebDriver
                if Dlink._driver is None:
                    service = Service()
                    Dlink._driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("Test with local WebDriver")
            elif browser == 'firefox':
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.binary_location = a.firefox_path
                #firefox_options.add_argument('--headless')
                firefox_options_prefs = {
                    "browser.download.dir": a.download_path,
                    "browser.download.folderList": 2,
                    "browser.download.manager.showWhenStarting": False,
                    "browser.helperApps.neverAsk.saveToDisk": "application/pdf, application/octet-stream"
                }
                for key, value in firefox_options_prefs.items():
                    firefox_options.set_preference(key, value)
                firefox_options.add_argument('--ignore-certificate-errors')
                firefox_options.add_argument('--incognito')
                Dlink._driver = webdriver.Firefox(options=firefox_options)
            elif browser == 'edge':
                edge_options = webdriver.EdgeOptions()
                edge_options.binary_location = a.edge_path
                edge_options.add_argument('--ignore-certificate-errors')
                edge_options.add_argument('--incognito')
                Dlink._driver = webdriver.Edge(options=edge_options)
            elif browser == 'edge_chromium':
                edge_chromium_options = webdriver.EdgeOptions()
                edge_chromium_options.binary_location = a.edge_path
                edge_chromium_options.add_argument('--ignore-certificate-errors')
                edge_chromium_options.add_argument('--incognito')
                Dlink._driver = webdriver.Edge(options=edge_chromium_options)
            elif browser == 'safari':
                safari_options = webdriver.SafariOptions()
                safari_options.add_argument('--ignore-certificate-errors')
                safari_options.add_argument('--incognito')
                Dlink._driver = webdriver.Safari(options=safari_options)
            else:
                raise ValueError("Invalid browser specified. Use 'chrome', 'firefox', 'edge', 'edge_chromium', or 'safari'.")
        Dlink._driver.set_window_size(self.w, self.h)
        Dlink._driver.maximize_window()


    def open(self, url, passwd):
        driver = self._driver
        driver.set_page_load_timeout(300)
        driver.get(url)
        print("Open Home page")
        time.sleep(5)

        # Change Language to English
        language_select = Select(driver.find_element(By.ID, "Language"))
        desired_language = "en-us"
        language_select.select_by_value(desired_language)

        # Input password
        time.sleep(2)
        password = driver.find_element("name", "admin_Password")
        actions = ActionChains(driver)
        actions.move_to_element(password).click().perform()
        time.sleep(2)
        password.send_keys(passwd + Keys.ENTER)
        print("Enter Password")
        time.sleep(3)
        driver.refresh()
        time.sleep(3)

    def login(self, url, username, passwd):
        driver = self._driver
        driver.get(url)
        print("Open Home page")
        time.sleep(5)
        #登入
        #帳號
        #//*[@id="login_username"]
        login_username = driver.find_element("xpath",'//*[@id="login_username"]')
        actions = ActionChains(driver)
        actions.move_to_element(login_username).click().perform()
        time.sleep(5)
        print("Enter Username")
        login_username.send_keys(username)
        time.sleep(5)
        #密碼
        #//*[@id="login_filed"]/div[5]/input
        login_filed = driver.find_element("xpath",'//*[@id="login_filed"]/div[5]/input')
        actions = ActionChains(driver)
        actions.move_to_element(login_filed).click().perform()
        time.sleep(5)
        print("Enter Password")
        login_filed.send_keys(passwd + Keys.ENTER)
        time.sleep(10)


# Example usage:
# d = Dlink(browser='chrome')  # or d = Dlink(browser='firefox')
# d.open("your_url", "your_password")

    def language_select(self, url, passwd, lang):
        driver = self._driver
        driver.get(url)
        print("Open Home page")
        time.sleep(2)
        # Change Language to the desired language
        language_select = Select(driver.find_element(By.ID, "Language"))
        language_select.select_by_value(lang)
        # Input password
        time.sleep(2)
        password = driver.find_element("name", "admin_Password")
        actions = ActionChains(driver)
        actions.move_to_element(password).click().perform()
        time.sleep(2)
        password.send_keys(passwd + Keys.ENTER)
        print("Enter Password")
        time.sleep(3)
        driver.refresh()
        time.sleep(3)
        print(f"Login with {lang}")



# Example usage:
# your_instance.language_select("your_url", "your_password", "English")
# Change the desired_language parameter to switch between languages
    '''
    language_mapping = {
                "English": "en-us",
                "Traditional Chinese": "zh-tw",
                "Simplified Chinese": "zh-cn",
                "Korean": "ko-kr",
                "French": "fr-fr",
                "Brazilian Portuguese": "pt-br",
                "Spanish": "es-es",
                "Italian": "it-it",
                "German": "de-de",
                "Russian": "ru-ru",
            }
    '''
##############  Click Button  #########################

    def element(self, method, name=None, sec=2, datalist = 0, **kwargs):
        elm = None
        try:
            if method == "id":
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.ID, name)))
                class_name = elm.get_attribute("class")
                # print(f"class_name = {class_name}")

                # 判斷是哪一種按鈕, 是否 class name = chkbox, 這是用來判斷按鈕目前狀態的依據
                if class_name == "btn_bg":
                    # print(f"這是 A 型按鈕")
                    elm.click()
                else:
                    # print(f"這是 B 型按鈕")
                    Dlink._driver.execute_script("arguments[0].click();", elm)  

            elif method == "class":
                # elm = Dlink._driver.find_element(By.CLASS_NAME, name)
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
                Dlink._driver.execute_script("arguments[0].click();", elm)
                # elm.click() 

            elif method == "xpath":
                index = kwargs.get('index',1)
                xpath = f'({name})[{index}]'
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, xpath)))              
                Dlink._driver.execute_script("arguments[0].click();", elm)
                                           
            elif method == "css":
                elm = Dlink._driver.find_element(By.CSS_SELECTOR, name)
                elm.click() 
                
            elif method == "downmenu":
                name_length = len(name)
                index = kwargs.get('index',1)
                xpath = f'(//li/a[text()="{name}" and string-length(text())={name_length}])[{index}]'
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
                Dlink._driver.execute_script("arguments[0].click();", elm)  

            elif method == "advance":
                index = kwargs.get('index',1)
                xpath = f'(//span[contains(text(), "Advanced Settings")])[{index}]'
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
                Dlink._driver.execute_script("arguments[0].click();", elm)

            elif method == "java":
                js_code = f'CheckHTMLStatus("{name}");'
                Dlink._driver.execute_script(js_code)

            elif method == "input":
                txt = kwargs.get('txt')
                print(f"kwargs txt = {txt}")
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.element_to_be_clickable((By.ID, name)))
                current_input_text = elm.get_attribute("value")
                if current_input_text != txt:
                    elm.send_keys(Keys.CONTROL + "a")  # 全選
                    elm.send_keys(Keys.DELETE)
                    elm.clear()
                    elm.send_keys(txt)
                # # 判斷否為 connect client 的 IP Address 
                # if name == "client_IPAdrReserve":
                #     # print(f"這是 connect client 的 IP Address")
                #     elm.send_keys("")
                #     elm.send_keys(txt)
                # else:
                #     Dlink._driver.execute_script("arguments[0].value = '';", elm)
                #     Dlink._driver.execute_script("arguments[0].value = arguments[1];", elm, txt)               
   
            elif method == "checkbox":
                #<span class="chkbox_enabled"><script>I18N("h","Enabled")</script>Enabled</span>
                # 找到元素, 讀到狀態, 讀到 class name
                status = kwargs.get('status')
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.ID, name)))
                class_name = elm.get_attribute("class")
                print(f" \nclass_name = {class_name}")

                # 判斷是哪一種按鈕, 是否 class name = chkbox, 這是用來判斷按鈕目前狀態的依據
                if class_name == "chkbox":
                    print(f"This is the A-shaped button")
                    select = elm.is_selected()
                else:
                    print(f"This is the B-type button")
                    checkbox = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.ID, name + '_ck')))
                    select = checkbox.is_selected()
                print(f"Selected = {select}")

                # 判斷是否要改變按鈕狀態
                if select:
                    currect_status = "enable"
                else:
                    currect_status = "disable"

                if currect_status != status:
                    Dlink._driver.execute_script("arguments[0].click();", elm)
                    print(f"The current status is {currect_status}, the status you want to change is {status}, if the status is different, press the button to become {status}")
                else:
                    print(f"The current status is {currect_status}, the status you want to change is {status}, the status is the same, keep {status} ")

            
            elif method == "tick":
                # 目前沒勾<input type="checkbox" onchange="datalist.list[0].setEnable('true')">
                # 目前有勾<input type="checkbox" onchange="datalist.list[0].setEnable('false')" checked="">
                
                checkbox = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, f"//input[@type='checkbox'][@onchange=\"datalist.list[{datalist}].setEnable('{name}')\"]")))
                select = checkbox.is_selected()
                # 根據 select 的值設定 status
                if select:
                    status = "false"
                else:
                    status = "true"
                if "status" in kwargs:
                    # 如果提供了 status 參數，則使用提供的值，否則使用上面的計算結果
                    status = kwargs["status"].lower()
                
                if select and status == "true" or not select and status == "false":
                    Dlink._driver.execute_script("arguments[0].click();", checkbox)
                    print(f"The current status is {name}, the status you want to change is {status}, if the status is different, press the button to become {status}")
                else:
                    print(f"The current status is {name}, the status you want to change is {status}, the status is the same, keep {status}")

            elif method == "edit":
                elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='client_EditImage'][@onclick=\'{name}\']")))
                Dlink._driver.execute_script("arguments[0].click();", elm)
            elif method == "downmenu_Multiple":
                name_length = len(name)
                index = kwargs.get('index', 1)
                xpath = f'(//li/a[text()="{name}" and string-length(text())={name_length}])'
                
                # Wait for all matching elements to be present
                elements = WebDriverWait(Dlink._driver, a.button_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath))
                )
                
                # Click on each matching element
                for element in elements:
                    Dlink._driver.execute_script("arguments[0].click();", element)


            else:
                raise ValueError("Unsupported method")
            print(f"Method: {method}, Name: {name}")
            time.sleep(sec)
        except Exception as e:
            print(f"Error clicking elm: {e}")
        return elm       


##################  Function  #################
    def scrolldown(self, point, sec=3):
        Dlink._driver.execute_script(f"window.scrollTo(0, window.scrollY + {point})")
        print(f"Adjust the window {point} pixels down")
        time.sleep(sec)

    def screenshot(self, img="image.png", sec=3):
        Dlink._driver.save_screenshot(img)
        print(f"Screenshot {img}")
        time.sleep(sec)

    def save(self, sec=2, timeout=a.save_time):
        wait = WebDriverWait(Dlink._driver, timeout)
        try:
            elm = wait.until(EC.presence_of_element_located((By.ID, "Save_btn")))
            Dlink._driver.execute_script("arguments[0].click();", elm)
            print(f"Press SAVE and wait for OK to appear")
            ok_button = wait.until(EC.visibility_of_element_located((By.ID, "popalert_ok")))
            time.sleep(sec)
            ok_button.click()
            print(f"Press OK ")
        except TimeoutException:
            print("The Save_btn element cannot be found or the OK element does not appear within the specified timeout period. The button click operation will be skipped")
    
    def save_new(self, sec=2, timeout=a.save_time):
        wait = WebDriverWait(Dlink._driver, timeout)
        elm = wait.until(EC.presence_of_element_located((By.ID, "Save_btn")))
        time.sleep(sec)
        Dlink._driver.execute_script("arguments[0].click();", elm)
        print(f"Press SAVE and wait for OK to appear")
        try:
            ok_button = wait.until(EC.visibility_of_element_located((By.ID, "popalert_ok")))
            time.sleep(sec)
            ok_button.click()
        except Exception:
            print("skip")
        print(f"Press OK")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        for i in range(sec):
            url = a.DUT_GUI_url
            response = requests.get(url, verify=False)
            print(response)
            if response.status_code == 200:
                print(f"Successfully connected to DUT GUI.")
                time.sleep(sec)
                return True
            else:
                print(f"Failed to connect to DUT GUI, status code: {response.status_code}")
                if i < 4:
                    print(f"Retrying connection... (attempt {i+1}/5)")
                    time.sleep(sec)
                else:
                    print(f"Reached maximum number of retries, returning False.")
                    return False

    def ok(self, sec=2 ):
        wait = WebDriverWait(Dlink._driver, a.button_time)
        elm = wait.until(EC.presence_of_element_located((By.ID, "btn_OK")))
        Dlink._driver.execute_script("arguments[0].click();", elm)
        print(f"Press OK ")

    def plan(self, week, start_time, end_time, sec=2):
        week_place = Dlink._driver.find_element(By.ID, week)
        start_cell = week_place.find_element(By.XPATH, f".//li[@data='{start_time}']")
        end_cell = week_place.find_element(By.XPATH, f".//li[@data='{end_time}']")
        ActionChains(Dlink._driver).move_to_element(start_cell).perform()
        action_chains = ActionChains(Dlink._driver)
        action_chains.click_and_hold(start_cell)
        action_chains.move_to_element(end_cell)
        action_chains.release()
        action_chains.perform()
        print(f"mark schedule plan")
        time.sleep(sec)

    def del_plan(self, end_time, sec=2):
        xpath = f"//li[contains(@data, '{end_time}')]//div[contains(@title, 'Delete')]"
        elm = WebDriverWait(Dlink._driver, a.button_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"Delete plan for {end_time}")
        elm.click()
        time.sleep(sec)                              

    def close(self):
        Dlink._driver.close()

    def quit(self):
        Dlink._driver.quit()
        print("Exit automatic program")

    