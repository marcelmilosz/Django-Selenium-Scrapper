from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SingleProductScrapper:

    def __init__(self, searched_ean_or_text):
        self.driver = None
        self.searched_ean_or_text = searched_ean_or_text
        self.startingUrl = "https://allegro.pl/listing?string=" + str(searched_ean_or_text)

        self.offersTitle = []
        self.offersPrice = []
        self.offersBought = []
        self.isOfferSponsored = []

        self.bestOfferDescription = []


        # Here we put all data for single product, we want to return it and save to excel or show on webpage. 
        # This has to be single product, that have all the best informations we can get 
        self.singleProductAnalyzed = {}

    # Run this to start
    def start(self):
        # Open page 
        self.chrome_start(self.startingUrl) 

        # Click Cookies 
        self.driver_click_element_by_XPATH("button", "data-testid", "accept_home_view_action") 

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
            self.analyze_data()

            self.driver.quit()

            return self.singleProductAnalyzed
        
        return {"error": "Product not found!"}


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

    def driver_move_to_url(self, url):
        self.driver.get(url)
    
    def driver_scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(1)
    
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

            ## Add data for final return 
            self.singleProductAnalyzed = {
                "product_or_ean": self.searched_ean_or_text,
                "offer_link": self.startingUrl,
                "best_title": bestTitle,
                "max_howManyBought": max_howManyBought,
                "best_price": bestPrice,
                "lowest_price": lowest_price,
                "highest_price": highest_price,
                "avg_price": avgPrice,
                "best_offer_link": bestOffer_link,
                "best_description": bestOffer_description[0],
                "parameters": bestOffer_parameters[0],
                "photos_links": bestOffer_img_link,
            }

myScrapper = SingleProductScrapper("5907798850556")
myScrapper.start()

