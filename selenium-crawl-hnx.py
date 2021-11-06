from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json

url = 'https://banggia.hnx.vn/' 
driver = webdriver.Chrome()
driver.get(url)

items = driver.find_elements(By.CLASS_NAME, 'trChange')
print(len(items))

stock_list = []

for item in items:
    stockCode = item.find_element(By.XPATH, './/td/div/div/span').text
    # if not stockCode:
    #     continue

    referencePrice = item.find_element(By.XPATH, './/td[4]/div').text
    cellingPrice = item.find_element(By.XPATH, './/td[5]/div').text
    floorPrice = item.find_element(By.XPATH, './/td[6]/div').text
    maxPrice = item.find_element(By.XPATH, './/td[26]/div').text
    minPrice = item.find_element(By.XPATH, './/td[27]/div').text
    averagePrice = item.find_element(By.XPATH, './/td[28]/div').text

    stock_item = {
        'stock-code': stockCode,
        'reference-price': referencePrice,
        'celling-price': cellingPrice,
        'floor-price': floorPrice,
        'max-price': maxPrice,
        'min-rice': minPrice,
        'average-price': averagePrice,
    }

    stock_list.append(stock_item)
    # break

stock_dict = {'stocks' : stock_list}

stock_json = json.dumps(stock_dict, indent=4)
# ghi ra file dưới dạng json
fw = open('stock-hnx-json.json', 'w')
fw.write(stock_json) 
fw.close()

# ghi ra file dưới dạng csv
df = pd.DataFrame(stock_list)
df.to_csv(r'stock-hnx-csv.csv', index = None, header=True)

# close stream
driver.close()