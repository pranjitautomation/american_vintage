from RPA.Browser.Selenium import Selenium
from  bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve as uretrieve
import os
import datetime



class DownloadImage:
    def __init__(self):
        self.browser = Selenium()
        self.input = 'E23'

    
    def open_browser(self):
        self.browser.open_available_browser('https://www.americanvintage-store.com/en/')
        self.browser.click_element_when_visible('//button[text()="ACCEPT ALL COOKIES"]')
        self.browser.click_button_when_visible('(//button[@class="close"])[2]')

    def search_products_and_load_all(self):
        self.browser.click_element('//button[@aria-label="Search"]')
        self.browser.input_text('//input[@placeholder="Enter search terms"]', self.input)
        self.browser.click_element_when_visible('//a[@class="mt-3 btn btn-block btn-outline-primary search-layer-seemore"]')
        self.browser.wait_until_element_is_visible('//span[@class="plp-header-meta-counter"]', timeout=10)
        prod_text = self.browser.get_text('//span[@class="plp-header-meta-counter"]')
        prod_no = int(prod_text.split(' ')[0].replace(',', ''))

        i = 0
        while i<prod_no:
            products = self.browser.find_elements('//h2[@class="product-tile-name"]')
            no_of_prods = len(products)
            self.browser.execute_javascript("window.scrollTo(0, document.body.scrollHeight);")
            i = no_of_prods

    def search_and_download_image(self): 
        products = self.browser.find_elements('//h2[@class="product-tile-name"]/a')
        href_list = []
        for prod in products:
            href = self.browser.get_element_attribute(prod, 'href')
            href_list.append(href)

        for each_href in href_list:
            self.download_image(each_href)

    def download_image(self, url):
        uClient = uReq(url)
        eachPage = uClient.read()
        uClient.close()
        product_html = bs(eachPage, "html.parser")
        
        reference_text = product_html.find("h2", {"class": "pdp-ref"})
        reference_no = reference_text.text.split(':')[1].strip()

        if self.input in reference_no:
            all_img_links = product_html.findAll("img", {"class": "pdp-slider-img zoomable"})
            for img_link in all_img_links[:int(len(all_img_links)/2)]:
                src = img_link['src']
                url = src
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
                filename = f"image{reference_no}-{timestamp}.png"  # Replace with the desired filename
                output_folder_path = os.path.join(os.getcwd(), 'output')
                filepath = os.path.join(output_folder_path, filename)
                os.makedirs(output_folder_path, exist_ok=True)

                uretrieve(url, filepath)

