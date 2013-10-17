import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import pdb 
import sys

if len(sys.argv) > 1:
    start = int(sys.argv[1])
else:
    start = 0

multiple = 70

br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
br.open('https://www.easychair.org/account/signin.cgi?conf=salt23')



br.select_form(nr=0)

br.form['name'] = 'panand'
br.form['password'] = 'montague1930'

# Login
br.submit()
br.open('https://www.easychair.org/conferences/submission_show_all.cgi?a=2977716')

info_links = [l for l in br.links(url_regex='info_show')]

end = start+multiple
cur = start
for link in info_links[start:end]:
    br.open(link.absolute_url)
    html = br.response().read()
    soup = BeautifulSoup(html)
    def extractText(soupClass):
        try:
            return html2text.html2text(str(soupClass).decode("ascii", "ignore"))
        except UnicodeDecodeError:
            pdb.set_trace()
    keywords = extractText(soup.findAll('tr', attrs={'id': 'row9'})[0].findAll("td")[1]).replace("\n", "")
    abstract = extractText(soup.findAll('tr', attrs={'id': 'row12'})[0].findAll("td")[1]).replace("\n", " ")
    time = extractText(soup.findAll('tr', attrs={'id': 'row15'})[0].findAll("td")[1])
    
    if not keywords:
        keywords = "none"
    if not abstract:
        abstract = "none"
    if not time:
        time = "none"
        
    f = open("%d.tab" % (cur+1), "w")
    cur += 1
    f.write("\t".join([keywords, abstract, time]))
    f.close()

# Logout
br.open('https://www.easychair.org/account/signout.cgi')