from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
import time
import chromedriver_autoinstaller 
import random
from seleniumbase import Driver

class SingleProductScrapper:

    def __init__(self, searched_ean_or_text):
        self.driver = None
        self.searched_ean_or_text = searched_ean_or_text
        self.baseUrl = "https://allegro.pl/"
        self.startingUrl = "https://allegro.pl/listing?string=" + str(searched_ean_or_text)
        self.usedUserAgend = ""

        self.offersTitle = []
        self.offersPrice = []
        self.offersBought = []
        self.isOfferSponsored = []

        self.bestOfferDescription = []


        # Here we put all data for single product, we want to return it and save to excel or show on webpage. 
        # This has to be single product, that have all the best informations we can get 
        self.singleProductAnalyzed = {}

    # Runs driver at some starting url and updates the driver
    def driver_init(self, run_undetected = True):

        # Commented stuff is for Chrome
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")


        # driver = webdriver.Chrome(options=options)

        chromedriver_autoinstaller.install() 

        service = Service()
        options = webdriver.ChromeOptions()

        options.add_argument(r'--user-data-dir=/Users/marcelmilosz/Library/Application Support/Google/Chrome/Default')
        options.add_argument(r'--profile-directory=Profile 1')

        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 

        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 

        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) 

        # Setting the driver path and requesting a page 

        if run_undetected:
            print("Running undetected Driver")
            self.driver = Driver(uc=True)
            

        else:
            print("Running normal Driver")
            driver = webdriver.Chrome(service=service, options=options)

            user_agent_array = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
            ]

            random_useragent = random.randint(0, len(user_agent_array) - 1)
            self.usedUserAgend = user_agent_array[random_useragent]
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent_array[random_useragent]})

            self.driver = driver


    # Run this to start
    def start(self):
        
        # Open page 
        self.driver_init(run_undetected=True) 

        print("\nDriver inited")
        print(f"Starting URL: \n{self.startingUrl}")
        print(f"Searched Ean or text: {self.searched_ean_or_text}")
        print(f"User Agent: ", self.usedUserAgend)

        self.driver.get(self.baseUrl)

        # Click Cookies

        time.sleep(self.generate_random_float(2.5, 5))
        self.driver_click_element_by_XPATH("button", "data-testid", "accept_home_view_action", timeout=2) 
        time.sleep(self.generate_random_float(1, 2))

        # Search for input bar and type ean 
        time.sleep(self.generate_random_float(2.5, 5))
        self.driver_click_and_type_text_element_by_XPATH("input", "class", "m7er_k4 mgn2_14 mp0t_0a m0qj_5r m9tr_5r mli8_k4 mx7m_1 m911_co mnyp_co mdwl_co mlkp_6x mefy_5r mm2b_0 mldj_0 mtag_2 msbw_2 msts_pt mgmw_wo mr3m_1 mli2_1 mh85_0 mjyo_6x mse2_40 mqu1_40 mp4t_0 m3h2_0 mryx_0 munh_0 mvrt_8 mg9e_0 mj7a_0 mh36_0 _535b5_Sviv7", timeout=2, text=self.searched_ean_or_text) 
        time.sleep(self.generate_random_float(1, 2))

        # Get all offers Title 
        self.offersTitle = self.driver_find_all_elements_by_XPATH("a", "class", "mgn2_14 mp0t_0a mgmw_wo mj9z_5r mli8_k4 mqen_m6 l1fas l1igl meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_XVsLO  ")

        if len(self.offersTitle) > 0:

            self.linksToOffers = self.driver_find_all_elements_by_XPATH("a", "class", "mgn2_14 mp0t_0a mgmw_wo mj9z_5r mli8_k4 mqen_m6 l1fas l1igl meqh_en mpof_z0 mqu1_16 m6ax_n4 _6a66d_XVsLO  ", return_href = True)

            # Get all offers price
            self.offersPrice = self.driver_find_all_elements_by_XPATH("div", "class", "mli8_k4 msa3_z4 mqu1_1 mp0t_ji m9qz_yo mgmw_qw mgn2_27 mgn2_30_s")

            # Get all containers that hold (and may not hold) information about how many offers in this category was bought
            self.offersBought = self.driver_find_all_elements_by_XPATH("div", "class", "mpof_ki m389_a6 munh_56_l mj7a_4")

            # Get if offer is sponsored 
            self.isOfferSponsored = self.driver_find_all_elements_by_XPATH("div", "class", "mj7a_4 m3h2_56")

            # Analyze data and print data in console
            try:
                self.analyze_data()
                self.generate_random_float(0.5, 3)
            except Exception as e:
                print("Something went wrong with analyze_data")
                print("Error message: ", e.message)

            # self.driver.quit()

            return self.singleProductAnalyzed
        
        else:
            return {"error": "Product not found!"}

    def generate_random_float(self, from_num, to_num, step = 0.1):
        random_float = round(random.uniform(from_num, to_num) / step) * step
        print("Random time wait: ", round(random_float, 2))
        return round(random_float, 2)
    
    def generate_random_number(self, from_num, to_num):
        random_int = random.randint(from_num, to_num)
        print("Random number: ", random_int)
        return random_int

    def driver_move_to_url(self, url):
        self.generate_random_float(0.5, 3)
        self.driver.get(url)
    
    def driver_scroll_to_bottom(self):
        # Splitted into some parts becuase Allegro will notice wierd movement
        # we also randomize scroll
        sum = 0 
        for i in range(0, 8):
            sum += self.generate_random_number(100, 400)
            self.driver.execute_script(f"window.scrollTo(0, {sum});")
            time.sleep(0.5)
    
    # Clicks any element on page. Waits for it for @timeout time in seconds
    def driver_click_element_by_XPATH(self, element, attr, attrVal, timeout = 5): 

        element_to_click = f"element: {element} | attribute: {attr} | attributeValue: {attrVal}"

        try:
            print(f"\nTrying to click element: {element_to_click}\n")
            print(f"Timeout: {timeout} seconds")

            element_locator = (By.XPATH, f'//{element}[@{attr}="{attrVal}"]')
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_locator))
            
            self.driver.find_element(*element_locator).click()
            print("Success.. ")
        except Exception as e:
            print(f"\nCouldn't click on element: {element_to_click}")
            print("Error message: ", str(e))

    def driver_click_and_type_text_element_by_XPATH(self, element, attr, attrVal, timeout = 5, text = ""): 

        element_to_click = f"element: {element} | attribute: {attr} | attributeValue: {attrVal}"

        try:
            print(f"\nTrying to click element: {element_to_click}\n")
            print(f"Timeout: {timeout} seconds")

            element_locator = (By.XPATH, f'//{element}[@{attr}="{attrVal}"]')
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_locator))
            
            foundElement = self.driver.find_element(*element_locator)
            foundElement.click()

            for letter in text:
                foundElement.send_keys(letter)
                time.sleep(self.generate_random_float(0, 0.3))

            foundElement.send_keys(Keys.RETURN)

            print("Success.. ")
        except Exception as e:
            print(f"\nCouldn't click on element: {element_to_click}")
            print("Error message: ", str(e))


    # Find, display and save all elements by XPATH
    # Returns array of elements (text)
    def driver_find_all_elements_by_XPATH(self, element, attr, attrVal, timeout = 5, return_href = False, return_src = False):
        elements_to_find = f"element: {element} | attribute: {attr} | attributeValue: {attrVal}"

        try:
            print(f"\nTrying to find elements: {elements_to_find}\n")
            print(f"Timeout: {timeout} seconds")

            element_locator = (By.XPATH, f'//{element}[@{attr}="{attrVal}"]')
            WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(element_locator))
            
            elements = self.driver.find_elements(*element_locator)
            print(f"\nFound {len(elements)} matching elements")
            print("===" * 30)

            arr = []

            for index, el in enumerate(elements):
                print(f"{index + 1}. {el.text}")

                if return_href:
                    arr.append(el.get_attribute('href'))
                elif return_src:
                    arr.append(el.get_attribute('src'))
                else:
                    arr.append(el.text)

            print("===" * 30)
            print()

            print("Success..")

            return arr

        except Exception as e:
            print(f"\nCouldn't find any elements: {elements_to_find}")
            print("Error message: ", str(e))

            return []

    def offers_prices_formatted(self):
        arr = []

        for i in self.offersPrice: 
            arr.append(float(i.replace(",", ".").replace(" zł", "")))

        return arr

    def offers_bought_formatted(self):
        arr = [] 

        for i in self.offersBought: 
            if i and len(i) > 0:
                arr.append(int(i.replace(" osób kupiło", "").replace("osoba kupiła", "").replace("osoby kupiły", "")))
            else:
                arr.append(0)

        return arr

    def analyze_data(self):

        if (len(self.offersTitle) > 0):

            ## Data from global offers (where we have them all splitted)
            lowest_price = min(self.offers_prices_formatted())
            highest_price = max(self.offers_prices_formatted())
            avgPrice = round(float(sum(self.offers_prices_formatted())  / len(self.offersPrice)), 2)

            offersBoughtFormatted = self.offers_bought_formatted()
            max_howManyBought = max(offersBoughtFormatted)
            highestBoughtIndex = offersBoughtFormatted.index(max_howManyBought)
            howManyBought = sum(offersBoughtFormatted)

            bestOffer_link = self.linksToOffers[highestBoughtIndex]
            
            bestTitle = self.offersTitle[highestBoughtIndex]
            bestPrice = float(self.offersPrice[highestBoughtIndex].replace(",", ".").replace(" zł", ""))

            ## Data from single offer (mainly this best one)
            self.driver_move_to_url(bestOffer_link)
            self.driver_scroll_to_bottom() # This helps with images loading when we scroll into view!

            bestOffer_description = self.driver_find_all_elements_by_XPATH("div", "class", "mgn2_14 mp0t_0a mqu1_21 mli8_k4 mgmw_wo msts_pt _0d3bd_K6Qpj")
            bestOffer_parameters = self.driver_find_all_elements_by_XPATH("table", "class", "myre_zn mp7g_oh m7er_k4 q2unx mp0t_0a msts_pt")
            bestOffer_img_link = self.driver_find_all_elements_by_XPATH("img", "class", "msub_k4 mupj_5k mjru_k4 mse2_k4 mp7g_f6 mq1m_0 mj7u_0 m7er_k4 lazyloaded", return_src = True)

            bestOffer_category = self.driver_find_all_elements_by_XPATH("ol", "class", "mg9e_0 mvrt_0 mj7a_0 mh36_0 mp4t_0 m3h2_0 mryx_0 munh_0 mv5s_z3 mr0s_56 bceg6w mzmg_7i msa3_z4")

            ## Display data for user
            print("\nAnaliza.. ")
            print("===" * 30)
            print(f"Produkt / Ean: {self.searched_ean_or_text}")
            print(f"Link do ofert: {self.startingUrl}")
            print(f"Ilość ofert: {len(self.offersTitle)}")
            print(f"\nNajlepszy tytuł: {bestTitle}")
            print(f"Najwięcej kupionych: {max_howManyBought} szt. za cenę {bestPrice}")
            print(f"Kupionych łącznie: {howManyBought} szt.")
            print(f"Najnizsza cena: {lowest_price} zł")
            print(f"Najwyzsza cena: {highest_price} zł")
            print(f"Średnia cena: {avgPrice} zł")
            print(f"\nLink do najlepszej oferty:")
            print(f"{bestOffer_link}")
            print(f"\nNajlepszy opis:")
            print(f"{bestOffer_description}")
            print(f"\nParametry:")
            print(f"{bestOffer_parameters}")
            print(f"\nLink do zdjęć:")
            print(f"{bestOffer_img_link}")
            print(f"\nKategoria: ")
            print(f"{bestOffer_category}")
            print(f"")

            print("===" * 30)

            preview_link = ""

            if bestOffer_img_link:
                preview_link = bestOffer_img_link[0]

            ## Add data for final return 
            self.singleProductAnalyzed = {
                "product_or_ean": self.searched_ean_or_text,
                "how_many_offers": len(self.offersTitle),
                "offer_link": self.startingUrl,
                "best_title": bestTitle,
                "max_howManyBought": max_howManyBought,
                "best_price": bestPrice,
                "lowest_price": lowest_price,
                "highest_price": highest_price,
                "avg_price": avgPrice,
                "best_offer_link": bestOffer_link,
                "photos_links": bestOffer_img_link,
                "first_photo_link": preview_link,
            }

            if len(bestOffer_description) > 0 and len(bestOffer_parameters) > 0 and len(bestOffer_category) > 0:
                self.singleProductAnalyzed["best_description"] = bestOffer_description[0]
                self.singleProductAnalyzed["parameters"] = bestOffer_parameters[0]
                self.singleProductAnalyzed["product_category"] = bestOffer_category[0].replace("\n", " - ")

            

# myScrapper = SingleProductScrapper("5060896625461")
# myScrapper.start()

# import undetected_chromedriver as uc
# driver = uc.Chrome(headless=True,use_subprocess=False)
# driver.get('https://nowsecure.nl')


