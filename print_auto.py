import sys
import time

import pyautogui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# executable_path=r'C:/Users/Umar Sheikh/Downloads/chromedriver_win32/chromedriver.exe''

login_info = {
    'rm1': [
        'https://login.airview.resmed.com/custom-login?response_type=code&client_id=0oa7ca7b9yNqH8sBI297&scope=openid%20email%20profile&state=yrebdRlYyAvp8n5YaaTqpZ24FE-uypYOqMyKmcLHaJA%3D&redirect_uri=https://login.airview.resmed.com/authorization-code/callback&nonce=sgJCAiO33lvMlHuD_0EzFdauqKmEUD00ArPkav9ppEI',
        '***', '***'],
    'rm2': [
        'https://login.airview.resmed.com/custom-login?response_type=code&client_id=0oa7ca7b9yNqH8sBI297&scope=openid%20email%20profile&state=yrebdRlYyAvp8n5YaaTqpZ24FE-uypYOqMyKmcLHaJA%3D&redirect_uri=https://login.airview.resmed.com/authorization-code/callback&nonce=sgJCAiO33lvMlHuD_0EzFdauqKmEUD00ArPkav9ppEI',
        '***', '***'],
    'co': ['https://www.careorchestrator.com/#/login',
           '***', '***']
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
    for name in temp[:-1]:
        str = name[1].lower() + ' ' + name[0].replace(',', '').lower()
        patient_names.append(str)
    return patient_names


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

        if check_element_exists_by_css_selector('a.nameAsLink'):
            patient_code = driver.find_element_by_class_name('patient-row').get_attribute('id')
            cpap_report_url = 'https://airview.resmed.com/patients/{}/report/complianceandtherapy/Compliance_and_therapy_report_06292021_183334.pdf?returningUrl=%2Fpatients%2F{}%2Fcharts&reportType=ComplianceAndTherapy&reportPeriodType=SUPPLIED&reportingPeriodLength=90&reportingPeriodStart=undefined&reportingPeriodEnd=06%2F28%2F2021&nightProfileDays=7'.format(
                patient_code, patient_code)
            driver.get(cpap_report_url)
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'p')
            time.sleep(3)
            pyautogui.press('Enter')
            time.sleep(1)
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
                driver.find_element_by_link_text('Therapy data').click()
                cpap_report_url = driver.find_element_by_tag_name('pr-pdf-viewer').get_attribute('src')
                driver.get(cpap_report_url)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'p')
                time.sleep(3)
                pyautogui.press('Enter')
                time.sleep(1)
                driver.get('https://www.careorchestrator.com/#/patient/search')

    driver.close()


patient_list = get_info()
driver = webdriver.Chrome(executable_path=r'C:/Users/Umar Sheikh/Downloads/chromedriver_win32/chromedriver.exe')
driver.maximize_window()  # For maximizing window
driver.implicitly_wait(10)  # gives an implicit wait for 10 seconds
check_rm(1)
check_rm(2)
check_co()
