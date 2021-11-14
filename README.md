# Python-crawl-data-tool

## Table of Contents
- [Description](#cescription)
- [Main features](#main-features)
- [Implementation Guide](#implemention-guide)
- [User Guide](#user-guide)
- [License](#license)
- [Release](#release)
- [Author](#author)


## Description

This tool uses Python Selenium to crawl data of stock and price from website https://banggia.hnx.vn/. Each stock includes data as code, reference price, ceiling price, floor price, min price, max price, average price. 

After that, all data is exported into 2 file formats, json and csv.


## Main features

- Crawl stock data 
- Export to file, json and csv format
- Export documentation as html

## Implementation Guide

Enviroment require: python. 
- In wwindows, you can download an install python in [`https://www.python.org/downloads/`](https://www.python.org/downloads/)


Libraries require: selenium, pandas, scrapy
- Install python libraries: turn on your terminal and type `pip install -r requirements.txt`


## User Guide

- Turn on your terminal and `cd` into this folder `Python-crawl-data-tool.`
- Run command on your terminal: `python selenium-crawl-hnx.py`
- Data exports to 2 file: stock-hnx-csv.csv (csv format) and stock-hnx-csv.json (json format)

If you want to read the documentation: 
- In your terminal, direct to this folder, type: `python -m pydoc -w selenium-crawl-hnx.py`
- documentation is exported to file `selenium-crawl-hnx.html`. You can watch on browser.


## License:

Copyright © 2021 Nguyen Quang Hung


## Release: 

Version: 0.4 update on Nov 14, 2021


# Author
- Nguyễn Quang Hưng
- Facebook: https://www.facebook.com/hungnq.SoICT/
- Email: nguyenquanghung.ktmt@gmail.com
- LinkedIn: https://www.linkedin.com/in/hungnq-soict