# Clicks on Selenium webelements at a certain screen position (x,y)

## pip install seleniumabsxy

### Tested against Windows 10 / Python 3.10 / Anaconda 


This module can benefit individuals or developers who need to automate browser interactions, 
such as clicking on specific elements or locations within a web page. By providing the ability to click on coordinates, 
it allows for precise interactions with web elements that may not be easily accessible through other means.

## Advantages of this module include:

### Automation: 

It enables automated clicking on specific coordinates within a browser window, which can save time and effort when performing repetitive tasks.

### Precise Interactions: 

By specifying exact coordinates, it allows for precise targeting of specific elements or locations on a web page.
Integration with Chrome: The module integrates with undetected_chromedriver, 
which provides an undetectable Chrome browser instance, allowing for seamless automation without detection by websites.


### Hotkey Support: 

The module offers the ability to set a hotkey combination to print the current cursor coordinates, which can be useful for debugging or identifying target locations.


```python
# This code imports necessary libraries and functions, sets a hotkey combination to show
# the cursor coordinates, creates a Chrome browser instance with specific options, assigns the
# driver to the coordsclicker module, waits for 5 seconds, opens a webpage (https://python.org), 
# maximizes the browser window, and provides instructions on how to use the click_on_coords function 
# to click on an object by specifying its coordinates.

# The Browser must either be maximized or the x-coordinate has to be 0 if not maximized

from time import sleep
import undetected_chromedriver as uc

from seleniumabsxy import set_show_hotkey_coords, click_on_coords, coordsclicker

if __name__ == "__main__":
    set_show_hotkey_coords(hotkey='ctrl+alt+k')
    chrome_opt = uc.ChromeOptions()
    chrome_opt.add_argument("--incognito")
    driver = uc.Chrome(
        options=chrome_opt,
    ) # works also with Selenium, but Chrome only 
    coordsclicker.driver = driver # important!!
    sleep(5)
    driver.get(r"https://python.org")
    driver.fullscreen_window()
    # Go to the object you want to click on, press 'ctrl+alt+k', and call click_on_coords(x,y)
    # The click_on_coords function retrieves a clickable element at the specified coordinates and clicks on it.
	
	# After pressing 'ctrl+alt+k', you will see something like this
    # x=1277, y=459

    # This is how you click
    # click_on_coords(x=1277, y=459)
```