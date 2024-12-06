import time
from selenium.webdriver.common.by import By
import pyautogui
import pyperclip


class SharePoint:
    search = ""
    
    
    def upload_folder(self,driver:object,url:str,folder_path:str):
        """_summary_

        Args:
            driver: selenium.chrome.WebDriver
            url : Url of the Sharepoint Folder 
            folder_path : Folder Path to be Uploaded 

        Returns:
            True if the folder Uploaded Succcessfully 
        """
        
        self.driver = driver
        
        self.driver.get(url)
        time.sleep(2)
        
        upload_button = self.driver.find_element(By.NAME,'Upload')
        upload_button.click()
        time.sleep(1)
        
        folder_button = self.driver.find_element(By.NAME,'Folder')
        folder_button.click()
        time.sleep(2)
        
        pyperclip.copy(folder_path)
        print("folder path is:", folder_path)
        pyautogui.hotkey('ctrl','v')
        print('ctrl v pressed')
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)
        # pyautogui.click(645, 450)
        # pyautogui.hotkey('ctrl','a')
        # time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.press('left')
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(10)
        print("success")
        return True

        
    def handle_login(self,driver:object):
        """_summary_

        Args:
            driver : selenium.chrome.WebDriver
        """
        
        url='https://nskkogyo.sharepoint.com/sites/2021'
        
        self.driver = driver
        # Assuming the login page has input fields with IDs 'username' and 'password'
        self.driver.get(url)

        username = "kushalnasiwak@nskkogyo.onmicrosoft.com"
        password = "Vay32135"
        time.sleep(2.5)
        # Find the username input field on the login page
        self.driver.find_element(By.XPATH, '//*[@id="i0116"]').clear()

        self.driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(username)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        time.sleep(1.5)
        # Find the password input field on the login page
        if self.driver.find_element(By.XPATH, '//*[@id="i0118"]').text:
            self.driver.find_element(By.XPATH, '//*[@id="i0118"]').clear()
        self.driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
        time.sleep(1.5)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        time.sleep(2)
        print('Logged in to Sharepoint\nPlease wait.....')


    