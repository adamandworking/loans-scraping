# loans-scraping

This a python script for scraping loans data from [MoneyHero](https://www.moneyhero.com.hk/zh/personal-loan) by Selenium with Python. The result would be parsed as a json file (saved as './loans.json') and beprinted on the console. 

## Usage
```console
python loans_web_scraping.py [type of loan] [amount of money] [repayment period]
```
Argument1 - Type of loan - : There are 9 types of loan. You should input an integer which is corresponding to the specific loan.  
### The mapping table: 

    1: Personal Instalment Loans
    2: Tax Loans
    3: Lending Companies Loans
    4: Debt Consolidation Loans
    5: Car Loans
    6: Home Ownership Loans
    7: SME Lending
    8: Banks Loans
    9: Small Size Loans

Argument2 - Amount of money wanted to borrow - : The amount of money that you want to borrow. The input data type should be an integer

Argument3 - Repayment period - : The desired repayment period (months). The input data type should be an integer

## Example
If you want to choose type of loan as 'Lending Companies Loans', borrow $200,000 and your desired repayment period is 24 months.
Please type "`python loans_web_scraping.py 3 200000 24`" as your command.
