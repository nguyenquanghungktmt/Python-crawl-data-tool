'''
Created on Oct 23, 2021

@author: Nguyen Quang Hung
'''

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import json
import logging

# Start
print('Starting application ... \n')

# create a url variable that is the website link that needs to crawl
url = 'https://banggia.hnx.vn/'   

# import browser firefox
# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()   

# declare logging
logging.basicConfig(level=logging.DEBUG, filename='crawl-stock-hnx.log', format='%(asctime)s %(levelname)s:%(message)s')
logging.disable(logging.DEBUG)

# Create stock-list to contain the stock-object
# Each item contains infomation of 1 stock like code, prices
stock_list = []


def crawl_stock_data(section):
    """
    This function takes as an input parameter the name of the stock item, and crawls the data of stock codes and prices. 
    Then put the data into the stock_list array

    Parameters:
    section (String): A input string describes the name of the stock section like ABC, DEF, GHI, ...

    Returns:
    this function doesn't return anything
    
    """

    # Create xpath to selenium click event
    xpath = '//div[@id="' + section +'"]/p'

    try:

        # Call selenium function to click on button on browser
        driver.find_element(By.XPATH, xpath).click()
        driver.implicitly_wait(10)

        # Call selenium function to fill all elements that have style "trChange"
        # Each element corresponds to a line describing a stock
        items = driver.find_elements(By.CLASS_NAME, 'trChange')

        # Notice to user
        print(f'Crawl {len(items)} stock items in {section} section')

        # log to logging file
        logging.info(f'Crawl {len(items)} stock items in {section} section')

        for item in tqdm(items):
            try:
                # Get the stock code
                stockCode = item.find_element(By.XPATH, './/td/div/div/span').text

                # If can't get the code for some reason, skip this iteration
                if not stockCode:
                    continue

                # Get the stock prices
                referencePrice = item.find_element(By.XPATH, './/td[4]/div').text
                cellingPrice = item.find_element(By.XPATH, './/td[5]/div').text
                floorPrice = item.find_element(By.XPATH, './/td[6]/div').text
                maxPrice = item.find_element(By.XPATH, './/td[26]/div').text
                minPrice = item.find_element(By.XPATH, './/td[27]/div').text
                averagePrice = item.find_element(By.XPATH, './/td[28]/div').text

                # Create element that contains stock information: code, prices
                stock_item = {
                    'stock-code': stockCode,
                    'reference-price': referencePrice,
                    'celling-price': cellingPrice,
                    'floor-price': floorPrice,
                    'max-price': maxPrice,
                    'min-rice': minPrice,
                    'average-price': averagePrice,
                }

                # push that element to the last of the stock item list
                stock_list.append(stock_item)

                # log to logging file
                logging.info(f'Success to get stock: {stockCode}')
            
            except:
                # There has some wrong with crawling data
                print(f'Opps! Something wrong when crawling a stock in {section} section')

                # log this error
                logging.error(f'Failed to crawl a stock in {section} section')

                continue

            # end loop

    except:
        # There has some wrong when start crawling in this section
        print(f'Opps! something wrong in {section} section')

        # log this error to logging file
        logging.error(f'Failed in {section} section')
        return

    # End function
    print('Done!\n')
    return


# main

try:
    print(f'Access the url {url} ...\n')

    # access the url
    driver.get(url)   

    # set implicit wait is 10s
    driver.implicitly_wait(10)

except Exception :
    # There has some wrong with connection problem
    print('Opps! We ran into some problems')
    print('Can\'t access the url. Please check your operation and try again.')

    # log that cannot access the url
    logging.error(f'Failed to access the url {url}')

    # close web browser
    driver.close()

    # shutdown app
    exit(0)

# call crawl_stock_data function to start crawling data from stock sections
crawl_stock_data('ABC')
crawl_stock_data('DEF')
crawl_stock_data('GHI')
crawl_stock_data('JKL')
crawl_stock_data('MNO')
crawl_stock_data('PQR')
crawl_stock_data('STUV')
crawl_stock_data('WXYZ')

# Finishing crawl data. Print the total number of stocks
print('\n======================================')
print('Completed. We have crawled', len(stock_list),'stocks')


# Convert stock-list (type: list) to type dictionary. 
stock_dict = {'stocks' : stock_list}

# Create json from stock dictionary
stock_json = json.dumps(stock_dict, indent=4)

# write data to file as json format
try:

    fw = open('stock-hnx-json.json', 'w')  # Open file and clear recent data of file
    fw.write(stock_json) 
    fw.close()   # Close file

    # log this step to file log
    logging.info('Success to export data to file as format json')

except:
    print('Cannot open or write data to json file')

    # log this error to file log
    logging.error('Failed to export data to file as format json')


# export data to file as csv format
try:
    df = pd.DataFrame(stock_list)
    df.to_csv(r'stock-hnx-csv.csv', index = None, header=True)

    logging.info('Success to export data to file as format csv')

except:
    print('Cannot export data to csv file')
    logging.error('Failed to export data to file as format csv')


# close web browser
driver.close()