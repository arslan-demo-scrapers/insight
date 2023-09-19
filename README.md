How to run spider script after make setup & configuration
*******  How to Setup Documentation *******

** I am placing website url that will help you while installing virtual environment:
https://www.geeksforgeeks.org/python-virtual-environment/
**

The tool is made in python 3
extract it to your system.

``` 
*** Step-1 ***

-> You need to install an IDE for managing project. Please download and install
Editor PyCharm Community Edition.
``` 

####You need to install some modules, just open terminal window in pycharm and write command:

`pip install scrapy`

###Note: 
####Now Set your project interpreter in which you have scrapy installed.



```` 
*** Step-2 ***

Before running make What to make sure is:
you are in the folder /insight/insight/spiders.
In spiders folder you can see input csv file "search_jobs.csv".
```` 
### Run script command: 

```` 
python3 insight_spider.py 
````
#### OR
```` 
python insight_spider.py 
```` 

Note: "insight_spider.py" is the name of script, that scrape data. Now Set your
project interpreter in which you have scrapy installed.

When Script will finish its execution, it will scrape all categories products
and store then in separate CSV files. Then you will need to run the another python
script, that will merge the all of CSV files to ONE EXCEL FILE. To Run that
Script.
### Run script command: 
```` 
python3 -m convert_csv_files_to_excel.py
````

#### OR

````
python convert_csv_files_to_excel.py 
````


This script will generate a excel file with name "Insight Products.xlsx". This file is stored inside a project folder
named "output".

#### Note:
if any issue you will face while installing libraries then download libraries from [HERE](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)

``` 
#### *** Step-3 ***
Now where will you get the output? 
when you run script after completed Script execution, then in the output 
folder you see all CSV files for each sheet there is one CSV file.
Also you will see a generate excel file with name "Insight Products.xlsx".
This file is stored inside a project folder named "output".
``` 

```` 
*** Step-4 ***
for any query please send me message.

Kind regards,
alifarslan

````

###Thank You!
