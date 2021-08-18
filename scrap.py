from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector

driver = webdriver.Chrome('/Users/Khushi Thakkar/chromedriver_win32/chromedriver.exe')
driver.get('https://www.linkedin.com')

# username
username = driver.find_element_by_id('session_key')
username.send_keys('techproject2022@gmail.com')
sleep(0.5)

# password
password = driver.find_element_by_id('session_password')
password.send_keys('mrisakhu@12')
sleep(0.5)

#submit value
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(0.5)

driver.get('https://www.google.com/')

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys('https://www.linkedin.com/in/khushi-thakkar-906b56188/')
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

# locate the first link
search_person = driver.find_element_by_class_name('yuRUbf')
search_person.click()

#load source code
sel = Selector(text=driver.page_source)

#scrap name
name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
if name:
    name = name.strip()

#scrap headline
headline = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()
if headline:
    headline = headline.strip()

#scrap location
location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()
if location:
    location = location.strip()

#scrap about
about = sel.xpath('//*[starts-with(@class, "lt-line-clamp__line lt-line-clamp__line--last")]/text()').extract_first()
if about:
    about = about.strip()

#Experience
experience = driver.find_elements_by_css_selector('#experience-section .pv-profile-section')

#Education
education = driver.find_elements_by_css_selector('.education-section ')

#Certification
certification = driver.find_elements_by_css_selector('#certifications-section li')

file = open('linkedin.txt', 'w')

file.write('Name is: ' +name+ "\n")
file.write('Headline is: ' +headline+ '\n')
file.write('Location is: ' +location+ '\n' )
file.write('About the person: ' +about+ '\n')
file.write('\n Experience \n ')
file.writelines("%s\n" % line.text for line in experience)
file.write('\n Education \n ')
file.writelines("%s\n" % line.text for line in education)
file.write('\n Certification \n ')
file.writelines("%s\n" % line.text for line in certification)
file.close()
