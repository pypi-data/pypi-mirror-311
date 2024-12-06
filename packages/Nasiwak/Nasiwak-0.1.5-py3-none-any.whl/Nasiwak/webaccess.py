from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests


# url = 'https://raw.githubusercontent.com/Kushal-Nasiwak/json-files/9807c0d9c14a44d6edf7d63f19e81ae1e8ded3d4/webaccess.json?token=GHSAT0AAAAAAC2VXSE5AJIPVBGYVU7L7PTKZZ7SBVA'
# url = 'https://raw.githubusercontent.com/Kushal-Nasiwak/json-files/refs/heads/main/webaccess.json?token=GHSAT0AAAAAAC2VXSE4QTAQJZOCCR6YLDM6ZZ7S26Q'
url = 'https://raw.githubusercontent.com/Kushal-Nasiwak/json-files/refs/heads/main/webaccess.json'
# Your personal access token
headers = {"Authorization": "token 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"}
response = requests.get(url, headers=headers)





class Webaccess:
    config = response.json()

    def WebAccess_login(self,driver:object,user_id:str = "NasiwakRobot",password:str = "159753"):
        
        
        """_summary_
        Used To login to WebAccess 
        Args:
            driver : selenium.chrome.WebDriver
            user_id : Userid of your account  default value -> "NasiwakRobot"
            password : Password of your account default value -> "159753"
        """
        
        # webaccess_url = 'https://webaccess.nsk-cad.com/order_list.php'
        webaccess_url = self.config["webaccess_url"]
        driver.get(webaccess_url)
        # user_id = "NasiwakRobot"
        # password = "159753"
        try:
            logid = driver.find_element("name","u")
            logpassword = driver.find_element("name","p")

            logid.clear()
            logpassword.clear()

            logid.send_keys(user_id)
            logpassword.send_keys(password)
            logid.submit()
            driver.implicitly_wait(10)

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located)
            print("Successfully logged in to Webaccess")
        except:
            print('logged in already')
            



    
    