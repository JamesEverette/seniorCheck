import csv
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from bs4 import BeautifulSoup
import getpass
#from termcolor import colored

def dump_html(page):
    html = urlopen(page)
    bsObj = BeautifulSoup(html, "html.parser")
    thisThing = bsObj.prettify()
    print(thisThing)

# def dump_html(page, tag):


##Use selenium to login to my.sc.edu and navigate to my transcript.
##I use waits and EC, as well as xpath for finding elements and clicking
##send keys to username and password boxes
##close driver and use regex to find courses completed
##create dictionary of course tag and course numbers
##Also grabs test scores to see if user tests out of courses (e.g. foreign language)
def getTranscript():
    if phantom == True:
        driver = webdriver.PhantomJS(executable_path=r'C:\Phantom\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    else:
        driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://my.sc.edu/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="student"]/dl/dd[1]/ul/li/a')))
    driver.find_element_by_xpath('//*[@id="student"]/dl/dd[1]/ul/li/a').click()
    logintxt = driver.find_element_by_name("username")
    logintxt.send_keys(vipID)
    pwdtxt = driver.find_element_by_id('vipid-password')
    pwdtxt.send_keys(password)
    # response = input("Please enter your name: ")
    # pwdtxt.send_keys(response)
    driver.find_element_by_xpath('//*[@id="vipid-submit"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bmenu--P_StuMainMnu___UID1"]/div/div/span')))
    driver.find_element_by_xpath(
        '//*[@id="bmenu--P_StuMainMnu___UID1"]/div/div/span').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="bmenu--P_AdminMnu___UID2"]/h3')))
    driver.find_element_by_xpath(
        '//*[@id="bmenu--P_AdminMnu___UID2"]/h3').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="contentItem12"]/h3')))
    driver.find_element_by_xpath('//*[@id="contentItem12"]/h3').click()
    driver.find_element_by_xpath('//*[@id="id____UID7"]/div/div/div').click()
    # dump_html(driver.current_url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="contentHolder"]/div[3]/table[1]/tbody')))
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    aPage = bsObj.findAll("td", {"class": "dddefault"})
    #driver.close()
    transcript = []
    aList = []
    pattern = re.compile("^[A-Z]{4}L?$")
    for element in aPage:
        # print("1")
        # print(type(element.text))
        lines = element.text
        aList.append(lines)
        # if pattern.match(lines):
        # transcipt[lines] =
        # print(lines)
    #print(len(aList))
    i = 0
    hit = False
    while i < len(aList):
        if hit == True:
        # courseNo = aList[i]
            transcript.append(str(aList[i - 1] + " " + str(aList[i])))
            hit = False
        else:  # hit == False:
            if pattern.match(aList[i]):
                # courseNo = aList[i]
                # transcript.append(str(aList[i]))
                hit = True
        i = i + 1

    driver.get("https://ssb.onecarolina.sc.edu/BANP/bwsktesc.p_view_tests")
    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    aPage = bsObj.findAll("td", {"class": "dddefault"})
    driver.close()

    testScores = []
    hit = False
    i = 0
    for element in aPage:
        if hit == False:
            if "Placement Exam" in element.text:
                testScores.append(element.text)
                hit = True
                i = i + 1
        else:
            testScores[i-1] = testScores[i-1] + " : " + element.text
            hit = False
    #print(testScores)
    return transcript, testScores

####

def getFakeTranscript():
    transcript = ['MATH 141', 'PHYS 202', 'PHYS 211', 'PHYS 211L', 'ENGL 101', 'CSCE 145','CSCE 190', 'GEOL 101', 'POLI 101', 'UNIV 101', 'CSCE 146', 'CSCE 211', 'SPCH 140', 'STAT 509', 'CSCE 215', 'CSCE 212', 'CSCE 240', 'MATH 374', 'PEDU 113', 'PEDU 185', 'PEDU 187', 'CSCE 311', 'CSCE 350', 'CSCE 390', 'MKTG 350', 'CSCE 330', 'CSCE 355', 'CSCE 416', 'CSCE 490', 'ECON 224', 'PEDU 134', 'PEDU 153', 'PEDU 182', 'CSCE 567', 'MATH 344', 'MATH 344L', 'CSCE 492', 'CSCE 520', 'CSCE 590', 'PEDU 121', 'SOCY 101']
    testScores = ['USCC Spanish Placement Exam : S1']
    return transcript, testScores

####

##use urllib.request urlopen to grab approved liberal arts courses
##beautifulsoup to parse html
##regex to find courses in the page
##interpret words like 'any' and 'except'
##returns list of approved liberal arts courses
#https://www.cse.sc.edu/undergraduate/approved-liberal-arts
def getLiberalArts2():
    print("Grabbing approved Liberal Arts courses...")

    html = urlopen('https://cse.sc.edu/undergraduate/approved-liberal-arts')
    bsObj = BeautifulSoup(html, "html.parser")
    pTags = bsObj.findAll('p')
    # thisThing = pTags.prettify()
    pTags = pTags[1:5]
    liberalArts = {}
    libArts = []
    for element in pTags:
        # print("1")
        # print(type(element.text))
        lines = element.text.splitlines()
        for line in lines:
            result = re.search('[A-Z]{4}', line)
            if result:
                courseNo = re.findall('[0-9]{3}', line)
                if("any course " in line) or ("any course," in line):
                    # print("special")
                    libArts.append(str(result.group(0)) + " any")

                elif "any course" in line:
                    # print("hi")
                    libArts.append(str(result.group(0)) + " any")

                if courseNo:
                    for element in courseNo:
                    # print("hi")
                        libArts.append(str(result.group(0)) +
                                       " " + str(element))
                else:
                    courseNo = re.match('any course', line)
                    if courseNo:
                        print(str(courseNo.group(0)))
                        # liberalArts[result.group(0)] = str(result.group(0)) + " " + str(result2)
                # print( result.group(0) )
    return libArts
####

##This uses selenium features for typing filter terms into a textbox and
##selecting how many entries to view on one page
##creates list of courses by identifying courses 'td' tags by class, using bs4
def checkAIU():
    print("Grabbing approved AIU courses...")
    if phantom == True:

        driver = webdriver.PhantomJS(executable_path=r'C:\Phantom\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    else:
        driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("http://www.sc.edu/about/offices_and_divisions/provost/academicpriorities/undergradstudies/carolinacore/courses/foundational-courses.php")
    
    driver.find_element_by_xpath("//input[@placeholder='type keywords to filter table results']").send_keys("AIU")
    driver.find_element_by_xpath("//*[@id='DataTables_Table_0_length']/label/select").click()
    driver.find_element_by_xpath("//*[@id='DataTables_Table_0_length']/label/select/option[4]").click()

    bsObj = BeautifulSoup(driver.page_source, "html.parser")
    aPage = bsObj.findAll("td", {"class": "sorting_1"})

    driver.close()
    aiuList = []
    for element in aPage:
        aiuList.append(element.text)
    return aiuList
####


##Simple function, pass in a course and it checks 
##the course against the transcript
def courseCheck(transcript, aCourse):
    if(aCourse not in transcript):
        #print(colored("!!! You need to take " + aCourse + " !!!", 'yellow'))
        print("!!! You need to take " + aCourse + " !!!")
        return False
    else:
        transcript.remove(aCourse)
        return True

####

##This checks for the 4 requried CHEM courses OR the 
##4 required PHYS courses. If user has not completed the requirement,
##it tells the user which courses would satisfy the requirement.
def checkSCI(aTranscript):
    chemCount = 0
    physCount = 0
    if(("CHEM 111" or "CHEM 111L" or "CHEM 112" or "CHEM 112L") in aTranscript):
        if "CHEM 111" in transcript:
            chemCount+=1
        if "CHEM 111L" in transcript:
            chemCount+=1
        if "CHEM 112" in transcript:
            chemCount+=1
        if "CHEM 112L" in transcript:
            chemCount+=1
    if(("PHYS 211" or "PHYS 211L" or "PHYS 212" or "PHYS 212L") in aTranscript):
        if "PHYS 211" in aTranscript:
            physCount+=1
        if "PHYS 211L" in aTranscript:
            physCount+=1
        if "PHYS 212" in aTranscript:
            physCount+=1
        if "PHYS 212L" in aTranscript:
            physCount+=1
    if((chemCount == 4) or (physCount == 4)):
        return
    else:
        print("You need to take more CHEM or more PHYS courses.")
    

####

##The basic flow of the program through the university undergrad bulletin
def graduationCheck():
    if fake == True:
        transcript, testScores = getFakeTranscript()
    else:
        transcript, testScores = getTranscript()   
    
    print("Checking CMW...")
    courseCheck(transcript, "ENGL 101")
    courseCheck(transcript, "ENGL 102")
    print("Checking ARP...")
    courseCheck(transcript, "MATH 141")
    courseCheck(transcript, "MATH 142")
    print("Checking SCI...")
    checkSCI(transcript)
    print("Checking AIU...")
    checkAIU()
    #checkGFL check for placement test
    #checkGHS
    #checkGSS
    print("Checking CMS...")
    courseCheck(transcript, "SPCH 140")
    print("Checking VSR...")
    courseCheck(transcript, "CSCE 390")
    print("Checking INF...")
    if "ENGL 102" not in transcript:
        if(courseCheck(transcript, "LIBR 101") == False):
            print("*** Unless you plan on taking ENGL 102 ***")

    print("Checking remaining Gen Ed...")
    courseCheck(transcript, "MATH 241")
    courseCheck(transcript, "MATH 374")
    courseCheck(transcript, "MATH 344")
    courseCheck(transcript, "MATH 344L")
    courseCheck(transcript, "STAT 509")
    print("Checking Lab Sci...")
    #checkLabElective
    print("Checking Engl Elective...")
    if ("ENGL 462" not in transcript) and ("ENGL 463" not in transcript):
        print("!!! You  need to take ENGL 462 or ENGL 463 !!!")
    print("Checking Liberal Arts...")
    libArts = getLiberalArts2()
    artsCount = 0
    for element in transcript:
        if element in libArts:
            artsCount = artsCount + 1
            if artsCount == 3:
                break
    if artsCount < 3:
        print("!!! You need to take " + str(3 - artsCount) + " more Liberal Arts !!!")

    courseCheck(transcript, "CSCE 145")
    courseCheck(transcript, "CSCE 146")
    courseCheck(transcript, "CSCE 190")
    courseCheck(transcript, "CSCE 211")
    courseCheck(transcript, "CSCE 212")
    courseCheck(transcript, "CSCE 215")
    courseCheck(transcript, "CSCE 240")
    courseCheck(transcript, "CSCE 311")
    courseCheck(transcript, "CSCE 330")
    courseCheck(transcript, "CSCE 350")
    courseCheck(transcript, "CSCE 355")
    courseCheck(transcript, "CSCE 416")
    courseCheck(transcript, "CSCE 490")
    courseCheck(transcript, "CSCE 492")
    #checkElective
    #checkAppArea
    print("All done!")
####

##Run the graduation check
vipID = input("Enter your VIP ID: ")
password = getpass.getpass("Enter your password: ")
phantom = input("Would you like to use PhantomJS instead of Chrome? (yes or no): ")
if(phantom == "yes"):
    phantom = True
else:
    phantom = False
fake = input("Would you like to run a fake test? (yes or no): ")
if(fake == "yes"):
    fake = True
else:
    fake = False
print("Grabbing Transcript...")
graduationCheck()
