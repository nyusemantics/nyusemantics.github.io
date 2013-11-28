from selenium import webdriver

baseurl = 'https://www.easychair.org/account/signin.cgi?conf=salt24'
submissionsurl = ('https://www.easychair.org/conferences/'
                  'submission_show_all.cgi?a=5181508')


driver = webdriver.Chrome()
driver.get(baseurl)

driver.find_element_by_name("name").send_keys("dbumford")
driver.find_element_by_name("password").send_keys("number11")
driver.find_element_by_name("Sign in").click()
driver.get(submissionsurl)

submissions = []

for i in range(1, 14):
    tablepath = "//tr[@id='row" + str(i) + "1']"
    authorpath = tablepath + "/td[2]"
    titlepath = "//a[@name='" + str(i) + "']"
    infopath = tablepath + "/td[4]/a[1]"

    author = driver.find_element_by_xpath(authorpath)
    actualauthors = author.text.split(" and ")
    # take the first five authors (add blanks if needed)
    authors = (actualauthors + [""] * 10)[:5]
    title = driver.find_element_by_xpath(titlepath)
    submission = (title.text, authors)
    
    infolink = driver.find_element_by_xpath(infopath)
    infolink.click()
    actualinsts = []
    for i in range(len(actualauthors)):
        row = str(i + 3)
        instpath = ("//div[@class='ct_tbl'][2]//tr[" + row + "]/td[5]")
        inst = driver.find_element_by_xpath(instpath)
        actualinsts += [inst.text]
    institutions = (actualinsts + [""] * 10)[:5]
    submission += (institutions,)
    submissions += [submission]
    driver.back()

print submissions
pfs = (u'{},' * 10)[:-1]
print u'\n'.join(pfs.format(title, *[x for t in zip(authors, institutions) for
                                     x in t])
                 for (title, authors, institutions) in submissions)
