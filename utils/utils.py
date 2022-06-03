import pickle
import os

ROOT_PATH = "D:\\Eiger\\Coding\\project\\albert_scrape"

os.chdir(ROOT_PATH)
print(ROOT_PATH)



ALBERT_URL = "https://sis.nyu.edu/psc/csprod/EMPLOYEE/SA/c/NYU_SR.NYU_CLS_SRCH.GBL"
# page
class PAGE:
    INITIAL = 0
    MAJOR = 1

# printer
class HEADER:
    NAVIGATOR_HEADER = 0
    ERROR_HEADER = 1
    TEXT_HEADER = 2

    def values():
        return [HEADER.__dict__[k] for k in HEADER.__dict__ if isinstance(HEADER.__dict__[k], int)]


# level of detail
class DETAIL:
    MINIMAL = 0
    MEDIUM = 1
    FULL = 2

LEVEL_OF_DETAIL = {
    DETAIL.MINIMAL: ["Class#", "Class Status", "Component", "Schedule"],
    DETAIL.MEDIUM: ["Class#", "Section", "Class Status", "Instruction Mode", "Component", "Schedule"],
    DETAIL.FULL: ["Class#", "Session", "Section", "Class Status", "Grading", "Instruction Mode", "Course Location", "Component", "Schedule", "Lecturer", "Notes"]
}


with open("MAJOR_LINK_ID_LIST.pk", "rb") as file:
    MAJOR_LINK_ID_LIST = pickle.load(file)

def pretty_print(string, breakline=False, line_width = 70, ):   
    if breakline:
        cnt = 0
        print("[\033[34;1mTEXT\033[0m]", end=" ")
        for word in string.split(" "):
            print(word, end="")
            cnt += len(word) + 1
            if cnt >= line_width:
                print()
                cnt = 0
                print("[\033[34;1mTEXT\033[0m]\t", end=" ")
            print(" ", end="")
        print()   
    else:
        lines = string.split('\n')
        print(f"[\033[34;1mTEXT\033[0m] {lines[0]}")
        for line in lines[1: ]:
            print(f"[\033[34;1mTEXT\033[0m] \t{line}")



def nav_print(string, header, is_text_only=False):
    if header not in HEADER.values():
        raise ValueError("Invalid HEADER")
    
    if header == HEADER.TEXT_HEADER:
        print("[\033[34;1mTEXT\033[0m] ", end="")
        print(string)
    elif header == HEADER.ERROR_HEADER:
        print("[\033[31;1mERROR\033[0m] ", end="")
        print(string)
    else:
        if not is_text_only:
            if header == HEADER.NAVIGATOR_HEADER:
                print("[\033[32;1mNAVIGATOR\033[0m] ", end="")
                print(string)

status_color = {
    "open": 102,
    "wait list": 103,
    "closed": 101,
}
def print_class_status(class_no, class_status, component=""):
    color = ""
    for k in status_color:
        if k in class_status.lower():
            color = status_color[k]
    nav_print(f"{class_no} {component}: \033[30;{color};1m{class_status}\033[0m",
              HEADER.TEXT_HEADER)
    


if __name__ == "__main__":
    print(MAJOR_LINK_ID_LIST[0:4])
    pretty_print("""Addresses the impact of the digital computer on individuals, organizations, and modern society as a whole, and the social, political, and ethical issues involved in the computer industry. Topics change to reflect changes in technology and current events. Guest lecturers from various fields are invited to speak in class.""",
                breakline=True, line_width=10)

