import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pyautogui
import time
from datetime import date

# executable_path=r'C:/Users/Umar Sheikh/Downloads/chromedriver_win32/chromedriver.exe''

login_info = {
              'rm1' : ['https://login.airview.resmed.com/custom-login?response_type=code&client_id=0oa7ca7b9yNqH8sBI297&scope=openid%20email%20profile&state=yrebdRlYyAvp8n5YaaTqpZ24FE-uypYOqMyKmcLHaJA%3D&redirect_uri=https://login.airview.resmed.com/authorization-code/callback&nonce=sgJCAiO33lvMlHuD_0EzFdauqKmEUD00ArPkav9ppEI',
                    'cpapdoc', 'Mpsc_2015'],
              'rm2' : ['https://login.airview.resmed.com/custom-login?response_type=code&client_id=0oa7ca7b9yNqH8sBI297&scope=openid%20email%20profile&state=yrebdRlYyAvp8n5YaaTqpZ24FE-uypYOqMyKmcLHaJA%3D&redirect_uri=https://login.airview.resmed.com/authorization-code/callback&nonce=sgJCAiO33lvMlHuD_0EzFdauqKmEUD00ArPkav9ppEI',
                    'metroplex2', 'Mpsc_2021'],
              'co' : ['https://www.careorchestrator.com/#/login',
                    'jmodesto', 'Mpsc2020!']
}


def get_info():
    print("Copy the appointment list from eClinicalWorks: (click ctrl+d when done) \n")
    appointment_list = sys.stdin.readlines()
    temp = []
    patient_names = []
    for appointment in appointment_list:
        patient = appointment.split()[3:5]
        temp.append(patient)
    temp.remove(temp[0])
    for name in temp:
        str = name[1] + ' ' + name[0].replace(',', '')
        patient_names.append(str)
    return patient_names


def check_element_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True


def check_element_exists_by_css_selector(id):
    try:
        driver.find_element_by_css_selector(id)
    except NoSuchElementException:
        return False
    return True


def check_rm(num_rm):
    driver.get(login_info['rm{}'.format(num_rm)][0])
    user_name_box = driver.find_element_by_name('username')
    user_name_box.send_keys(login_info['rm{}'.format(num_rm)][1])
    user_name_box.submit()

    pass_box = driver.find_element_by_name('password')
    pass_box.send_keys(login_info['rm{}'.format(num_rm)][2])
    pass_box.submit()

    driver.find_element_by_link_text('https://airviewid.resmed.com/oauth2/aus7x84n01F9ecUUX297').click()

    driver.get('https://airview.resmed.com/wireless')

    for patient in patient_list:
        search_bar = driver.find_element_by_id('q')
        search_bar.clear()
        search_bar.send_keys(patient)
        search_bar.submit()

        if not check_element_exists_by_id('empty-patient-label'):
            # make the following step a bit faster
            patient_code = driver.find_element_by_class_name('patient-row').get_attribute('id')
            cpap_report_url = 'https://airview.resmed.com/patients/{}/report/complianceandtherapy/Compliance_and_therapy_report_06292021_183334.pdf?returningUrl=%2Fpatients%2F{}%2Fcharts&reportType=ComplianceAndTherapy&reportPeriodType=SUPPLIED&reportingPeriodLength=90&reportingPeriodStart=undefined&reportingPeriodEnd=06%2F28%2F2021&nightProfileDays=7'.format(patient_code, patient_code)
            driver.get(cpap_report_url)
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(2)
            pyautogui.press('Enter')
            driver.execute_script("window.history.go(-1)")
            patient_list.remove(patient)

    driver.find_element_by_id('logout-link').click()


def check_co():
    driver.get(login_info['co'][0])
    user_name_box = driver.find_element_by_id('username')
    user_name_box.send_keys(login_info['co'][1])
    user_name_box.submit()

    pass_box = driver.find_element_by_name('password')
    pass_box.send_keys(login_info['co'][2])
    pass_box.submit()

    for patient in patient_list:
        search_bar = driver.find_element_by_name('search-term')
        search_bar.clear()
        search_bar.send_keys(patient)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(2)

        if check_element_exists_by_css_selector('h3.pr-result-title.pr-result-title-link'):
            first_patient_on_page = driver.find_element_by_css_selector('h3.pr-result-title.pr-result-title-link')
            if first_patient_on_page.text.lower() in patient_list:
                first_patient_on_page.click()
                time.sleep(2)
                pyautogui.hotkey('ctrl', 'p')
                time.sleep(2)
                pyautogui.press('Enter')
                driver.execute_script("window.history.go(-1)")

    driver.close()


patient_list = get_info()
driver = webdriver.Chrome(executable_path=r'C:/Users/Umar Sheikh/Downloads/chromedriver_win32/chromedriver.exe')
driver.maximize_window() # For maximizing window
driver.implicitly_wait(10) # gives an implicit wait for 10 seconds
check_rm(1)
check_rm(2)
check_co()