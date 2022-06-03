# The constants to be updated are:
# - MAJOR_LINK_ID_LIST


from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import utils
import pickle

def update_major_link_id_list():
   
    driver = webdriver.Chrome()
    driver.get(utils.ALBERT_URL)

    major_elements = driver.find_elements(by=By.XPATH , value=".//a[contains(@id, 'LINK1$')]")
    
    majors = []

    for major_element in major_elements:
        major = major_element.text
        print(f"Major: {major}")
        majors.append(major)
    
    with open("MAJOR_LINK_ID_LIST.pk", "wb") as file:
        pickle.dump(majors, file)

update_major_link_id_list()