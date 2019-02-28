import numpy as np
from selenium import webdriver
from selenium.webdriver.support.color import Color

# define the customer probability of clicks
prob_list = [0.3, 0.8]

# instantiate the web brower
driver = webdriver.Chrome( executable_path='/Users/meigarom/chromedriver' )
driver.get( 'http://127.0.0.1:5000/home' )

# iterate over all clicks
trials = 101
episodes = 21
clicks = trials * episodes

for click in range( clicks ):
    if click % 100 == 0:
        print( 'Click: {} / {}'.format( click, clicks ) ) 

    button_color = driver.find_element_by_id( 'yesbtn' ).value_of_css_property( 'background-color' )

    color = Color.from_string( button_color ).hex

    if color == '#008cba': #blue background color
        web_page = 1
    else:
        web_page = 0

    if np.random.random() < prob_list[ web_page ]:
        driver.find_element_by_name( 'yescheckbox' ).click()
        driver.find_element_by_id( 'yesbtn' ).click()
    else:
        driver.find_element_by_name( 'nocheckbox' ).click()
        driver.find_element_by_id( 'nobtn' ).click()
















