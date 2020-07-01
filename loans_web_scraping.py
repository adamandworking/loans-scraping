from selenium import webdriver 
import time
from selenium.webdriver.common.keys import Keys
import argparse
import json

DRIVER_PATH = '.\chromedriver.exe'
LOAN_URL = ['personal-instalment', 'tax-loan', 'lending-companies-loan', 'debt-consolidation', 'car-loans', 'home-ownership', 'commercial-lending', 'banks-loan', 'small-size-loans']

def web_scraping(args):
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.set_window_size(1920, 1080)
    driver.get('https://www.moneyhero.com.hk/en/personal-loan/'+ LOAN_URL[args.loan_type - 1])
    money_borrow = driver.find_element_by_id('input-2')
    money_borrow.send_keys(Keys.CONTROL + "a")
    money_borrow.send_keys(args.amount)

    repayment_period = driver.find_element_by_id('input-3')
    repayment_period.send_keys(Keys.CONTROL + "a")
    repayment_period.send_keys(args.period)
    time.sleep(2)

    number_of_result = driver.find_element_by_css_selector('h2.sc-AxjAm').text[:-12]
    number_of_result = int(number_of_result[9:])

    if number_of_result == 0:
        print('No result for the specification')

    loan_list = driver.find_elements_by_class_name('product-pane')
    while(len(loan_list) != number_of_result):
        driver.execute_script("window.scrollBy(0,100)")
        loan_list = driver.find_elements_by_class_name('product-pane')

    result = []
    for loan in loan_list:
        header = loan.find_element_by_css_selector('h3.heading').text
        numbers = loan.find_elements_by_css_selector('div.value')
        total_repayment = int(numbers[0].text[2:].replace(',',''))
        monthly_repayment = int(numbers[1].text[2:].replace(',',''))
        apr = float(numbers[2].text[:-2])

        result.append({'name': header, 'total_repayment': total_repayment, 'monthly_repayment': monthly_repayment, 'apr': apr})
    driver.quit()
    write_json(result)
    return result

def write_json(data):
    with open("loans.json", "w") as write_file:
        json.dump(data, write_file)

def console_log(loans_data):
    print('There is/are ' + str(len(loans_data)) + ' result(s) found:')
    for idx, loan in enumerate(loans_data):
        print(str(idx + 1) + '.')
        print('Name: ' + loan['name'])
        print('Total Repayment (as low as): ' + str(loan['total_repayment']))
        print('Monthly Repayment (as low as): ' + str(loan['monthly_repayment']))
        print('Annual Percentage Rate (as low as): ' + str(loan['apr']))
        print('------------------------------------')

def main():
    parser = argparse.ArgumentParser(
        description='''
        This a python script for scraping loans data from https://www.moneyhero.com.hk/zh/personal-loan.  
        ''',
        epilog=
        '''
        Usage: python loans_web_scraping.py [type of loan] [amount of money wanted to borrow] [repayment period].
        For example, if you want to choose type of loan as \'Personal Instalment Loans\', borrow $200,000 and the desired repayment period is 24 months.
        Please type \'python loans_web_scraping.py 1 200000 24\' as your command.
        '''
    )
    parser.add_argument('loan_type', type=int, help='''
        Please enter the type of loan (1~9):
        1: Personal Instalment Loans
        2: Tax Loans
        3: Lending Companies Loans
        4: Debt Consolidation Loans
        5: Car Loans
        6: Home Ownership Loans
        7: SME Lending
        8: Banks Loans
        9: Small Size Loans
        ''', choices=list(range(1,10)))
    parser.add_argument('amount', type=int, help='Please enter the amount of money that you want to borrow')
    parser.add_argument('period', type=int, help='Please enter the desired repayment period (months)')
    args = parser.parse_args()
    loans_data = web_scraping(args)
    console_log(loans_data)

if __name__ == "__main__":
    main()