'''
Created on Oct 23, 2021

@author: Nguyen Quang Hung
'''

from os import close
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd
import json
import logging, logging.handlers
import connection_utils

# Start
print('Starting application ... \n')

# create a url variable that is the website link that needs to crawl
url = 'https://banggia.hnx.vn'    

# declare logging
logging.basicConfig(level=logging.DEBUG, filename='crawl-stock-hnx.log', format='%(asctime)s %(levelname)s:%(message)s')
logging.disable(logging.DEBUG)

logger = logging.getLogger(__name__)

# declare variable STMP Handler, initialized with the from and to addresses and subject line of the email.
smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587),
                                            fromaddr='hungnguyenjr9@gmail.com',
                                            toaddrs=['hungnq.cdc@gmail.com',
                                                     'hung.nq183760@sis.hust.edu.vn'],
                                            subject='Crash in Crawl-Data-Tool',
                                            credentials=(
                                                'hungnguyenjr9@gmail.com',
                                                'wlpgtalknxstpftp'),
                                            secure=())
logger.addHandler(smtp_handler)

# Create stock-list to contain the stock-object
# Each item contains infomation of 1 stock like code, prices
stock_list = []


def crawl_stock_data(driver, section):
    """
    This function takes as 2 input parameters the Web Driver and the name of the stock item section, and crawls the data of stock codes and prices. 
    Then put the data into the stock_list array

    Parameters:
    driver : the instance of WebDriver 
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
        # logger.info(f'Crawl {len(items)} stock items in {section} section')

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
                    'min-price': minPrice,
                    'average-price': averagePrice,
                }

                # push that element to the last of the stock item list
                stock_list.append(stock_item)

                # log to logging file
                # logger.info(f'Success to get stock: {stockCode}')
            
            except:
                # There has some wrong with crawling data
                print(f'Opps! Something wrong when crawling a stock in {section} section')

                # log this error
                logger.error(f'Failed to crawl a stock in {section} section')

                continue

            # end loop

    except:
        # There has some wrong when start crawling in this section
        print(f'Opps! something wrong in {section} section')

        # log this error to logging file
        logger.error(f'Failed in {section} section')
        return

    # End function
    print('Done!\n')
    return


def export_file(data):

    """
    The function takes 1 input parameter of stock data in an array, from which to export the data to json and csv format.

    Parameters:
    data (list): A list data of stock codes and prices.

    Returns:
    this function doesn't return anything
    
    """

    # Convert stock-list (type: list) to type dictionary. 
    stock_dict = {'data' : data}

    # Create json from stock dictionary
    stock_json = json.dumps(stock_dict, indent=4)

    # write data to file as json format
    try:

        fw = open('stock-hnx-json.json', 'w')  # Open file and clear recent data of file
        fw.write(stock_json) 
        fw.close()   # Close file

        print("Exported data to file json")

        # log this step to file log
        # logger.info('Success to export data to file as format json')

    except:
        print('Cannot open or write data to json file')

        # log this error to file log
        # logger.error('Failed to export data to file as format json')


    # export data to file as csv format
    try:
        df = pd.DataFrame(stock_list)
        df.to_csv(r'stock-hnx-csv.csv', index = None, header=True)

        print("Exported data to file csv")

        # logger.info('Success to export data to file as format csv')

    except:
        print('Cannot export data to csv file')
        logger.error('Failed to export data to file as format csv')


# Save to mysql database
def save_database(stock_data):
    
    """
    The function save all stock data that just been crawled to mysql database.

    Parameters:
    stock_data (list): A list data of stock codes and prices.

    Returns:
    this function doesn't return anything
    
    """

    # Create a connection to database
    connection = connection_utils.getConnection() 

    print("Connect to database successful!")  
    print("================================")

    # Define sql query: select, insert, create
    select_query = "SELECT * FROM stock_items WHERE code = %s "

    insert_query =  "INSERT INTO stock_items (code, reference_price, celling_price, floor_price, max_price, min_price, average_price) " \
        + " VALUES (%s, %s, %s, %s, %s, %s, %s) " 

    update_query = "UPDATE stock_items SET reference_price = %s, celling_price = %s, floor_price = %s, max_price = %s, min_price = %s, average_price = %s WHERE code = %s " 


    try :
        # create a new cursor object using the connection
        cursor = connection.cursor()

        for item in stock_data:
            stockCode = item['stock-code']

            # execute
            if not ( cursor.execute(select_query, stockCode)) :
                # there are no record that has stock code in database
                # insert stock item to database

                cursor.execute(insert_query, (stockCode, item['reference-price'], item['celling-price'] , item['floor-price'], item['max-price'], item['min-price'], item['average-price'] ))

                print(f"Successful Insert {stockCode}")
            else:
                cursor.execute(update_query, (stockCode, item['reference-price'], item['celling-price'] , item['floor-price'], item['max-price'], item['min-price'], item['average-price'] )) 

                print(f"Successful Update {stockCode}")

        # Commit any pending transaction to the database
        connection.commit()  

    except:
        print('Error to save data tp database')
        logger.error('Error to save data tp database')

    finally: 
        # Close the connection to database now 
        connection.close()

        print('Complete save data to database\n')


# main
def main():
    try:
        print(f'Access the url {url} ...\n')

        # import browser firefox
        # driver = webdriver.Firefox(options=options)
        driver = webdriver.Firefox()  
        
        # access the url
        driver.get(url)   

        # set implicit wait is 10s
        driver.implicitly_wait(10)

    except Exception :
        # There has some wrong with connection problem
        print('Opps! We ran into some problems')
        print('Can\'t access the url. Please check your operation and try again.')

        # log that cannot access the url
        logger.error(f'Failed to access the url {url}')

        # close web browser
        driver.close()

        # shutdown app
        exit(0)

    # call crawl_stock_data function to start crawling data from stock sections
    crawl_stock_data(driver, 'ABC')
    crawl_stock_data(driver, 'DEF')
    crawl_stock_data(driver, 'GHI')
    crawl_stock_data(driver, 'JKL')
    crawl_stock_data(driver, 'MNO')
    crawl_stock_data(driver, 'PQR')
    crawl_stock_data(driver, 'STUV')
    crawl_stock_data(driver, 'WXYZ')

    # Finishing crawl data. Print the total number of stocks
    print('\n======================================')
    print('Completed. We have crawled', len(stock_list),'stocks')
    # close web browser
    driver.close()


if __name__ == '__main__':
    main()
    export_file(stock_list)
    save_database(stock_list)