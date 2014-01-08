import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import rpy2.robjects as robjects
robjects.r("source('assign.R')")

r_assignments = robjects.globalenv['assignments']
a = r_assignments()
all_assignments = [list(a.rx(True, i))
                   for i in range(1, int(robjects.r.ncol(a)[0]) + 1)]
all_assignments = [[int(x) for x in xs] for xs in all_assignments]

name = sys.argv[1]
word = sys.argv[2]

log = open('a_log', 'w')
log.write("assignments: \n")
log.write(str(all_assignments))
log.write("\n\n\n")

baseurl = 'https://www.easychair.org/account/signin.cgi?conf=salt24'
submissionsurl = ('https://www.easychair.org/conferences/'
                  'submission_show_all.cgi?a=5181508')

driver = webdriver.Chrome()
driver.get(baseurl)

driver.find_element_by_name("name").send_keys(name)
driver.find_element_by_name("password").send_keys(word)
driver.find_element_by_name("Sign in").click()
driver.get(submissionsurl)

driver.find_element_by_id("menu1").click()

# have to make sure to skip over the withdrawn submissions
sub_indices = [x - 3 for x in (range(3, 39) + range(40, 185) +
                               range(186, 232) + range(233, 251))]

num_subs = 245
try:
    for i in range(num_subs):
        rev_as = all_assignments[sub_indices[i]]
        log.write("rev_as: " + ",".join([str(x) for x in rev_as]) + "\n")
        if sum(rev_as) == 0:
            continue
        sub_xp = "//tr[@id='row" + str(i + 1) + "1']/td[6]/a/img"
        log.write("sub_xp: " + sub_xp + "\n")
        driver.find_element_by_xpath(sub_xp).click()

        for a in [x for x in rev_as if x > 0 and x < 225]:
            rev_xp = "//tr[@id='row" + str(1 + 8 * a) + "']/td[2]/input"
            log.write("rev_xp: " + rev_xp + "\n")
            driver.find_element_by_xpath(rev_xp).click()
        time.sleep(.5)
        driver.find_element_by_id("menu1").click()

finally:
    driver.quit()
    log.close()
