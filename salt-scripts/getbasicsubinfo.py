# -*- coding: utf-8 -*-
import sys
import codecs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

name = sys.argv[1]
word = sys.argv[2]

log = codecs.open('log', 'w', encoding='utf-8')
subs = codecs.open('subs2.csv', 'w', encoding='utf-8')
keys = codecs.open('keys.csv', 'w', encoding='utf-8')

baseurl = 'https://www.easychair.org/account/signin.cgi?conf=salt24'
submissionsurl = ('https://www.easychair.org/conferences/'
                  'submission_show_all.cgi?a=5181508')


driver = webdriver.Chrome()
driver.get(baseurl)

driver.find_element_by_name("name").send_keys(name)
driver.find_element_by_name("password").send_keys(word)
driver.find_element_by_name("Sign in").click()
driver.get(submissionsurl)

submissions = []
keywords = []

try:
    for i in [x for x in range(3, 250) if x != 39 and x != 185 and x != 232]:
        if i < 39:
            row = i - 2
        elif i < 185:
            row = i - 3
        elif i < 232:
            row = i - 4
        else:
            row = i - 5
        tablepath = "//tr[@id='row" + str(row) + "1']"
        titlepath = "//a[@name='" + str(i) + "']"
        infopath = tablepath + "/td[4]/a[1]"

        log.write("tablepath: " + tablepath + "\n" +
                  "titlepath: " + titlepath + "\n" +
                  "infopath: " + infopath + "\n") 

        try:
            authorpath = tablepath + "/td[2]"
            log.write("authorpath: " + authorpath + "\n")
            author = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, authorpath))
            ).text
        except:
            try:
                authorpath = tablepath + "/td[2]/span[1]"
                log.write("authorpath: " + authorpath + "\n")
                author = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, authorpath))
                ).text
            except:
                author = "FIND MEEEEE"

        actualauthors = reduce(lambda x, y: x + y,
                               [x.split(" and ") for x in author.split(", ")])
        # take the first five authors (add blanks if needed)
        authors = (actualauthors + [u""] * 10)[:5]
        title = driver.find_element_by_xpath(titlepath).text

        log.write(u"authors: " + u",".join(actualauthors) + "\n"
                  u"title: " + title + "\n")

        submission = (title, authors)
        
        infolink = driver.find_element_by_xpath(infopath)
        infolink.click()

        keywordpath = ("//div[@class='ct_tbl'][1]//"
                       "tr[contains(td, 'keywords')]/td[2]/div")
        log.write("keywordpath: " + keywordpath + "\n")
        ks = [x.text for x in driver.find_elements_by_xpath(keywordpath)]
        log.write(u"keywords: " + u", ".join(ks) + "\n")
        keywords.append(ks)

        actualinsts = []
        for authindex in range(len(actualauthors)):
            instrow = str(authindex + 3)
            instpath = ("//div[@class='ct_tbl'][2]//tr[" + instrow + "]/td[5]")

            log.write("instpath: " + instpath + "\n")

            inst = driver.find_element_by_xpath(instpath).text
            actualinsts += [inst]
        institutions = (actualinsts + [u""] * 10)[:5]

        log.write(u"insts: " + u",".join(actualinsts) + "\n\n")

        submission += (institutions,)
        submissions += [submission]
        driver.back()

finally:
    log.close()
    driver.quit()
    pfs = (u'{},' * 10)[:-1]
    subs.write(
        u'\n'.join(
            pfs.format(title, *[x for t in zip(authors, institutions)
                                for x in t])
            for (title, authors, institutions) in submissions
        )
    )
    subs.close()
    keys.write(u'\n'.join([u', '.join(x) for x in keywords]))
    keys.close()
