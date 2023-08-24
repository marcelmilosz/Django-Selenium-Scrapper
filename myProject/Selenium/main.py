from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ALLEGRO_STARTING_URL = "https://allegro.pl/listing?string=5907798850556"

class SingleProductScrapper:

    def __init__(self, startingUrl, searched_ean_or_text):
        self.driver = None
        self.searched_ean_or_text = searched_ean_or_text
        self.startingUrl = startingUrl

        self.offersTitle = []
        self.offersPrice = []

    # Run this to start
    def start(self):
        # Open page 
        self.chrome_start(self.startingUrl) 

        # Click Cookies 
        self.driver_click_element_by_XPATH("button", "data-testid", "accept_home_view_action") 

        # Get all offers Title 
        self.offersTitle = self.driver_find_all_elements_by_XPATH("a", "class", "mgn2_14 mp0t_0a mgmw_wo mj9z_5r mli8_k4 mqen_m6 l1fas l1igl meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_XVsLO  ")

        # Get all offers price
        self.offersPrice = self.driver_find_all_elements_by_XPATH("div", "class", "mli8_k4 msa3_z4 mqu1_1 mp0t_ji m9qz_yo mgmw_qw mgn2_27 mgn2_30_s")

    # Runs driver at some starting url and updates the driver
    def chrome_start(self, Starting_Url):

        options = Options()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        driver.get(Starting_Url)

        print("\nDriver inited")
        print(f"Starting URL: \n{Starting_Url}")
        print(f"Searched Ean or text: {self.searched_ean_or_text}")

        self.driver = driver
    
    # Clicks any element on page. Waits for it for @timeout time in seconds
    def driver_click_element_by_XPATH(self, element, attr, attrVal, timeout = 5): 

        element_to_click = f"element: {element} | attribute: {attr} | attributeValue: {attrVal}"

        try:
            print(f"\nTrying to click element: {element_to_click} | timeout: {timeout} seconds")

            element_locator = (By.XPATH, f'//{element}[@{attr}="{attrVal}"]')
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_locator))
            
            self.driver.find_element(*element_locator).click()
            print("Success.. ")
        except Exception as e:
            print(f"\nCouldn't click on element: {element_to_click}")
            print("Error message: ", str(e))

    # Find, display and save all elements by XPATH
    # Returns array of elements (text)
    def driver_find_all_elements_by_XPATH(self, element, attr, attrVal, timeout = 5):
        elements_to_find = f"element: {element} | attribute: {attr} | attributeValue: {attrVal}"

        try:
            print(f"\nTrying to find elements: {elements_to_find} | timeout: {timeout} seconds")

            element_locator = (By.XPATH, f'//{element}[@{attr}="{attrVal}"]')
            WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(element_locator))
            
            elements = self.driver.find_elements(*element_locator)
            print(f"\nFound {len(elements)} matching elements")
            print("===" * 30)

            arr = []

            for index, el in enumerate(elements):
                print(f"{index + 1}. {el.text}")
                arr.append(el.text)

            print("===" * 30)
            print()

            print("Success..")

            return arr

        except Exception as e:
            print(f"\nCouldn't find any elements: {elements_to_find}")
            print("Error message: ", str(e))

myScrapper = SingleProductScrapper(ALLEGRO_STARTING_URL, "5907798850556")
myScrapper.start()

