import numpy as np
from selenium import webdriver

# open a browser - http://chromedriver.chromium.org/downloads
options = webdriver.ChromeOptions()
options.add_argument( '--kiosk' )
driver = webdriver.Chrome( executable_path='/Users/meigarom/chromedriver', options=options )

# flask application address
driver.get( 'http://127.0.0.1:5000/home' )

# find the buttons and click on them
clicks = 100
for click in range( clicks ):
    if np.random.random() < 0.5:
        driver.find_element_by_name( 'yescheckbox' ).click()
        driver.find_element_by_id( 'yesbtn' ).click()
    else:
        driver.find_element_by_name( 'nocheckbox' ).click()
        driver.find_element_by_id( 'nobtn' ).click()

