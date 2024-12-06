from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
        
        """_summary_
        creates a selenium.chrome.WebDriver and returns it

        Returns:
            selenium.chrome.WebDriver : Chrome WebDrivere 
        """
        chrome_options = Options()
        # download_folder = os.path.join(os.getcwd(), f'{id_folder_name}')
        chrome_options.add_experimental_option("prefs", {
        #"download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
        })


        # Initialize the WebDriver before the loop
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        
        return driver