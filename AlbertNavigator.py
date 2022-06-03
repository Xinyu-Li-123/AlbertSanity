import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import utils


class AlbertNavigator:
    def __init__(self, is_text_only=False):
        self.major = ""
        self.course_elements = []
        self.course_elements_dict = {}
        self.__page = utils.PAGE.INITIAL
        self.is_text_only = is_text_only

    @property
    def page(self):
        return self.__page

    def __enter__(self):
        driver = webdriver.Chrome()
        utils.nav_print("A new broswer is opened", 
                         utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)
        self.driver = driver
        self.driver.minimize_window()
        self.driver.get(utils.ALBERT_URL)
        utils.nav_print("Redirected to website: Albert - Public Course Search", 
                         utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)
        return self

    def __exit__(self, type=None, value=None, tb=None):
        self.driver.close()
        self._clear()
        self._page = utils.PAGE.INITIAL
        utils.nav_print("The current broswer is closed", 
                    utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)

    def open(self):
        self.__enter__()
    
    def close(self):
        self.__exit__()
    
    def _is_in_page(self, page):
        if self._page != page:
            return False
        return True
    

    def _clear(self):
        self.major = ""
        self.course_elements = []
        self.course_elements_dict = {}


    def _back(self): # go to next page
        if not self._is_in_page(utils.PAGE.INITIAL):
            self.driver.find_element(by=By.ID , value="NYU_CLS_DERIVED_BACK").click()
            self._page = utils.PAGE.INITIAL
            # for i in range(3):
            #     try:
            #         time.sleep(5)
            #         self.driver.find_elements(by=By.XPATH, value="//div[contains(@id,'win0divSELECT_COURSE_row$')]")
            #     except selenium.common.exceptions.NoSuchElementException:
            #         print("Connecting...")
            time.sleep(7)
                

    def _deselect_major(self):
        self._back()
        utils.nav_print(f"Deselecting major: {self.major}", 
                utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)
        self._clear()    
   

    def select_major(self, target_major_name):
        print()
        if not self._is_in_page( utils.PAGE.INITIAL):        # go back to inital page in case you are already in another major page
            self._deselect_major()
   
        entry_cnt = 0
        for major_name in utils.MAJOR_LINK_ID_LIST:
            # use acronym (CSCI-UA) or full major name (Computer Science (CSCI-UA))
            if target_major_name == major_name.split("(")[1][0:-1] or target_major_name == major_name:
                major_element = self.driver.find_element(by=By.ID , value=f"LINK1${entry_cnt}")
                self.major = major_element.text

                major_element.click()
                # for i in range(3):
                #     try:
                #         time.sleep(5)
                #         self.driver.find_elements(by=By.XPATH, value="//div[contains(@id,'win0divSELECT_COURSE_row$')]")
                #     except selenium.common.exceptions.NoSuchElementException:
                #         print("Connecting...")
                #TODO: mechanism similar to async - await
                time.sleep(7)
                    

                utils.nav_print(f"Redirected to webpage of major: {self.major}", 
                    utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)

                utils.nav_print("Scraping major information", 
                    utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)

                self.course_elements = self.driver.find_elements(by=By.XPATH, value="//div[contains(@id,'win0divSELECT_COURSE_row$')]")
            
                for course_element in self.course_elements:
                    course_name = course_element.find_element(by=By.TAG_NAME, value="b").text
                    self.course_elements_dict[course_name] = course_element

                utils.nav_print("Major information obtained", 
                    utils.HEADER.NAVIGATOR_HEADER, self.is_text_only)
                self._page = utils.PAGE.MAJOR
                return 
            entry_cnt += 1
        utils.nav_print(f"Major: '{major_name}' is not found, please try again.", 
            utils.HEADER.ERROR_HEADER, self.is_text_only)    


    def list_all_courses_of_major(self):
        print()
        if not self._is_in_page( utils.PAGE.MAJOR):
            utils.nav_print("You are not in the webpage of a Major. Please redirect to a Major page by Navigator.redirect_to_major(major_name).", 
                            utils.HEADER.ERROR_HEADER, self.is_text_only)    
            return 

        if self.major == "":
            utils.nav_print("You haven't chosen a major. Please choose one by Navigator.redirect_to_major(major_name).", 
                            utils.HEADER.ERROR_HEADER, self.is_text_only)    
            return 
    
        for course_name in self.course_elements_dict:
            utils.pretty_print(course_name, breakline=False)

        


    def list_all_classes_of_course(self, course_id, level_of_detail=utils.DETAIL.MINIMAL):
        print()
        level_of_detail = utils.LEVEL_OF_DETAIL[level_of_detail]
        if not self._is_in_page( utils.PAGE.MAJOR):
            utils.nav_print("You are not in the webpage of a Major. Please redirect to a Major page by Navigator.redirect_to_major(major_name).", 
                            utils.HEADER.ERROR_HEADER, self.is_text_only)    
            return  

        header, number = course_id.split(" ")
        for course_element in self.course_elements:
            course_name = course_element.find_element(by=By.TAG_NAME, value="b").text.split(" ")
            if header == course_name[0] and number == course_name[1]:
                time_slot_elements = course_element.find_elements(
                    by=By.XPATH, 
                    value=".//div[contains(@id, 'win0divSELECT_CLASS_row$')]")
                
                for time_slot_element in time_slot_elements:
                    class_info = {}
                    time_slot_info_01_element = time_slot_element.find_element(by=By.XPATH, value=".//div[contains(@id, 'COURSE')]")    # all info of a time slot except time, lecturer, notes
                    
                    for line in time_slot_info_01_element.text.split("\n"):
                        info = line.split(":")
                        if len(info) == 2:
                            class_info[info[0]] = info[1]                        

                    temp = time_slot_element.text.split("\n")
                    start = temp.index('')
                    schedule_and_lecturer = temp[start + 1]
                    if " with " in schedule_and_lecturer:
                        schedule, lecturer = schedule_and_lecturer.split(" with ")
                    else:
                        schedule = schedule_and_lecturer
                        lecturer = "Unknown"
                    notes = temp[start + 2]

                    class_info['Schedule'] = schedule
                    class_info['Lecturer'] = lecturer
                    class_info['Notes'] = notes

                    for info_header in class_info:
                        if info_header in level_of_detail:
                            if info_header != "Notes":
                                utils.pretty_print(f"{info_header}: {class_info[info_header]}", breakline=False)
                            else:
                                utils.pretty_print(f"{info_header}: {class_info[info_header]}", breakline=True)
        
                return
        utils.nav_print(f"Course ID: {course_id} is not found", 
            utils.HEADER.ERROR_HEADER, self.is_text_only)
            

    
    def check_class_status(self, class_no):
        try:
            class_element = self.driver.find_element(by=By.ID, value=f"COURSE{class_no}nyu")
            class_status = ""
            component = ""
            for line in class_element.text.split("\n"):
                if "Class Status" in line:
                    class_status = line.split(":")[1][1:]
                if "Component" in line:
                    component = line.split(":")[1][1:]
                    utils.print_class_status(class_no, class_status, component=component)
        except selenium.common.exceptions.NoSuchElementException as e:
            utils.nav_print(f"Class number {class_no} is not found", 
                                utils.HEADER.ERROR_HEADER, self.is_text_only)

    
    def listen_to(self, targets):
        print()
        if isinstance(targets, int):
            self.check_class_status(targets)
        
        elif isinstance(targets, list):
            for class_no in targets[major]:
                self.check_class_status(class_no)
        
        elif isinstance(targets, dict):
            for major in targets:
                print()
                self.select_major(major)
                for class_no in targets[major]:
                    if isinstance(class_no, int):
                        self.check_class_status(class_no)
                    else:
                        utils.nav_print(class_no, utils.HEADER.TEXT_HEADER, self.is_text_only)
        
    
    def get_course_information(self, target_course_id):
        print()
        if target_course_id != self.major.split("(")[1][:-1]:
        #     utils.nav_print("You are not in the webpage of a Major. Please redirect to a Major page by Navigator.redirect_to_major(major_name).", 
        #                 utils.HEADER.ERROR_HEADER, self.is_text_only)    
        #     return 
        # if self.major == "":
        #     utils.nav_print("You haven't chosen a major. Please choose one by Navigator.redirect_to_major(major_name).", 
        #                     utils.HEADER.ERROR_HEADER, self.is_text_only)    
        #     return 
            self.select_major(target_course_id.split(" ")[0])

        for course_name in self.course_elements_dict:
            course_id = " ".join(course_name.split(" ")[0:2])
            if target_course_id == course_id:
                course_element = self.course_elements_dict[course_name]
                school_name = course_element.find_element(by=By.CLASS_NAME, value="ps_box-value").text
                course_description = course_element.find_element(by=By.TAG_NAME, value="p").text
                utils.pretty_print(f"Course: {course_name}", breakline=False)
                utils.pretty_print(f"School: {school_name}", breakline=False)
                utils.pretty_print(f"Description: {course_description}", breakline=True)
                return
        utils.nav_print(f"Course id: {target_course_id} is not found", utils.HEADER.ERROR_HEADER)
        
            
if __name__ == "__main__":
    
    # demo
    with AlbertNavigator() as myNavigator:
    
        myNavigator.select_major("Computer Science (CSCI-UA)")
        myNavigator.list_all_courses_of_major()
        myNavigator.list_all_classes_of_course("CSCI-UA 201", level_of_detail=0)
        myNavigator.check_class_status(7444)

        myNavigator.select_major("MATH-GA")
        myNavigator.list_all_courses_of_major()

        myNavigator.get_course_information("MATH-UA 252")
        