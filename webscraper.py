from bs4 import BeautifulSoup
import urllib.request
import re
import csv


businesstype = 'employment'
pagenumbers = 10
companyurl = '{0}.txt'.format(businesstype)
#infooutput = 'infooutput-{0}.txt'.format(businesstype)
infooutput = 'infooutput.txt'
#gets url links to all companies in that kind of category


def getpages():
    for x in range(1,pagenumbers + 1):
        url = "http://businessdirectory.bizjournals.com/phoenix/{0}/page/{1}".format(businesstype,x)
        data = urllib.request.urlopen(url)
        #print(data.read())
        soup = BeautifulSoup(data)
        findcompanylinks(soup)

        
def findcompanylinks(webpage):
    with open(companyurl,'a') as f:
        linktofind = '\/phoenix\/{0}\/(\d)+\/.+'.format(businesstype)
        for link in webpage.find_all('a', href=re.compile(linktofind)):
            f.write(link.get('href') + "\n")

            
#/phoenix/information_technology/3281222/300-dollar-sites.html
#goes through each item in list and retrieves information for it
def companypage():
    with open(companyurl, 'r') as info:
        for line in info:
            url = "http://businessdirectory.bizjournals.com{0}".format(line)
            data = urllib.request.urlopen(url)
            soup = BeautifulSoup(data)
            getinformation(soup)

            
def getinformation(soup):
    try:
        companyname = soup.find("h2", class_="b2SecDetails-h2").getText().strip('\n')
        print(companyname)
    except Exception as e:
        companyname = ''
    try:
        city = soup.findAll("p", class_="b2sec-alphaText")[1].findAll('span')[0].getText().replace('\n',' ').strip(',')
        print(city)
    except Exception as e:
        city = ''
    try:
        zipcode = soup.findAll("p", class_="b2sec-alphaText")[1].findAll('span')[2].getText().replace('\n',' ').strip()
        print(zipcode)
    except Exception as e:
        zipcode = ''
    try:
        phone = soup.find(["p", "div"], class_="b2Local-greenTextmed").getText().strip()
        print(phone)
    except Exception as e:
        phone = ''
    try:
        website = soup.find("div", class_="b2secDetails-URL").ul.li.a.get('href')
        print(website)
    except Exception as e:
        website = ''
    try:
        about = soup.find('div', id = 'b2sec-alpha').findAll('p')[-2].getText('p').strip()
        print(about)
    except Exception as e:
        about = ''
    #information = ['"{0}", "{1}", "{2}", "{3}", "{4}", "{5}"'.format(companyname,city,zipcode,phone,website,about)]
    #information = list(companyname,city,zipcode,phone,website,about)
    information = [businesstype,companyname,city,zipcode,phone,website,about]
    buildcsv(information)

    
def buildcsv(info):
    with open(infooutput, 'a') as f:
        csvf = csv.writer(f, delimiter = ',')
        csvf.writerow(info)


#TODO seperate text files, various text stream output
getpages()
companypage()



