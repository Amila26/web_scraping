# get webdriver
# get Service 
# Define Serach Parameters 
# Assing Some Filters
# Create Car Database
# Create House Database for all district all Island.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # this is help to the press enter key in web page
from selenium.webdriver.support.ui import WebDriverWait  # wait driver
from selenium.webdriver.support import expected_conditions as EC # Condition statement
from selenium.webdriver.common.keys import Keys
import time
import glob
from pathlib import Path 
from bs4 import BeautifulSoup

import pandas as pd

directory = r"D:\DE_PROJECT"
file_list = glob.glob(str(directory)+'\*exe') # Get chromedriver exce
file_name = Path(file_list[0])    


chrome_service = Service(file_name) # Excectutable Service Object chromwebdriver.exc
driver = webdriver.Chrome(service = chrome_service)
url = "https://ikman.lk"

driver.get(url)
print(driver.title)
# following is the eliment which is need to access for Consent Overlay for grather information
#<button class="fc-button fc-cta-consent fc-primary-button" role="button" aria-label="Consent" tabindex="0"><div class="fc-button-background"></div><p class="fc-button-label">Consent</p></button>
try:
    button  = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[@aria-label='Consent']")))
    button.click()
    print("Consent Overlay Sucsess")
except Exception as e:
    print(f"Consent Overlay Failed Error is  {e}")


# html_content = driver.page_source
# soup = BeautifulSoup(html_content,"html.parser")
# print(soup.prettify())

#driver.close()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"category-item--1h1A1")))
category_items = driver.find_elements(By.CLASS_NAME,"category-item--1h1A1") # This is retun a list
main_menue_data = []
for i,items in enumerate(category_items):
    title = items.find_element(By.CLASS_NAME,'info-title--3CkVD').text
    ads_count = items.find_element(By.XPATH,"//span[contains(@class, 'info-count---yfNr')]").text
    link = items.find_element(By.TAG_NAME,"a").get_attribute('href')
    main_menue_data.append( [title,ads_count,link])
print(main_menue_data)


# Now we Access to the Main Menu data set or iether derect access eliment
# link = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@href, 'property')]")))
# link.click()


# print(driver.title)
# print(driver.current_url)

# Or either I can loop Over Main Menu to Extract all Data From Page wise.

sub_url = main_menue_data[2][2]
driver.get(sub_url) # now we are in new page so I have to give search input and then filter if wrong ssearch back to search box finaly extract all data

# I am list down left side clickble topic and select any topic as I prefered 
sub_cat_list =[]
try:
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"wrapper--1X_z8")))
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME,"list-item--2dM7Z")))
    side_wrapper = driver.find_elements(By.CLASS_NAME,"wrapper--1X_z8")
    side_wrapper_entries = side_wrapper[0].find_elements(By.TAG_NAME,"a") # This is beacuse I am reffering first ul tag under wrapper class other wise you can take second ul for locations
    for entry in side_wrapper_entries:
       sub_link = entry.get_attribute('href')
       ads_details = entry.text
       sub_cat_list.append([sub_link,ads_details])
 
except Exception as e:

    print(f"get sublist failed due to {e}")


print(sub_cat_list)


second_url = sub_cat_list[6][0]
WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CLASS_NAME,"list-item--2dM7Z")))
print(second_url)


driver.get(second_url)
cat = second_url.split("/")[-1]

# or we can use java script prompt trigger to get input
# try:
#     search_this = driver.execute_script("return prompt('Please enter your search term:', 'Selenium WebDriver');") # even this is show as a comment it contain JS command

WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@aria-label='Search input']"))) 
search_this = input(f"Enter what you need to serach from {cat}")
scrap_data_list = []

base_url = ""

def serch_function(search_this):
    global base_url
    try:
        
        search_box = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//input[@aria-label='Search input']")))
        search_box.send_keys(search_this)
        search_box.send_keys(Keys.RETURN) # Press Enter after sending search text
        print("search_function_excecuted")
        time.sleep(10)
        base_url = driver.current_url[:-1]
        print(base_url)
    
    except Exception as e:
        print(e)


# Based On the page structure which is define a web scrap function 


def scrap_function():

    try:
        WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".normal--2QYVk.gtm-normal-ad")))
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"normal-ad--1TyjD")))
        WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".card-link--3ssYv.gtm-ad-item")))
        
        #last_height = driver.execute_script("return document.body.scrollHeight")

        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(2)  # Wait for new content to load
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height

    # above code ensure all the elimen load properly

        scrap_list = driver.find_elements(By.CSS_SELECTOR,".normal--2QYVk.gtm-normal-ad")
        for entry in scrap_list:
            item_link = entry.find_element(By.CSS_SELECTOR,".card-link--3ssYv.gtm-ad-item").get_attribute("href")
        
            all_text = entry.text.split("\n")
            if  "MEMBER" in all_text:
                all_text.remove("MEMBER")

            #WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.normal-ad--1TyjD')))
            # image_link = entry.find_element(By.CLASS_NAME,"normal-ad--1TyjD").get_attribute("src")
            all_text.append(item_link)
            scrap_data_list.append(all_text)

    except Exception as e:

        print(e)




# all Page Scrap Function Here Use Recursive Method To Scrap all web pages
i=1

def page_wise_scrap():
    global i
    try:
        single_page = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"single-page--1lRgs")))
        print("only_single_page")
        scrap_function()

    except:
        try:
            notfound = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"no-result-text--16bWr")))
            print("Scrapping finished")
        except:
            try:
                multi_page = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"page-number--2O3yQ")))
                try:
                    end_eliment = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"active-desktop--3b3Ed")))
                    for x in end_eliment:
                        print(x.text)
                except:
                    scrap_function()
                    i=i+1
                    j=str(i)
                    new_url = base_url+j
                    driver.get(new_url)
                    time.sleep(15)
                    print(new_url)
                    page_wise_scrap()
            except Exception as e:
                print(e)
        
                
           



if search_this:
    serch_function(search_this)
    try:
        notfound = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"no-result-text--16bWr")))
        print(f"Serach Result not found for {search_this}")
    except:
        try:
            found = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"//span[contains(@class, 'ads-count-text--1UYy_')]")))
            print(f"Serach Result found for {search_this}")
            #scrap_function()
            page_wise_scrap()
        except Exception as e:
            print(e)         
else:
    print("please enter valid text to search")




if len(scrap_data_list) > 0:
    df = pd.DataFrame(scrap_data_list)
    save_location = r"D:\DE_PROJECT\ikman_data"+f"\{search_this}.csv"
    df.to_csv(save_location,index=False)
    print("Data Saved")











