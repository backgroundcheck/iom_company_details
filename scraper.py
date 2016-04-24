import scraperwiki
import lxml.html, lxml.etree
import urllib2
import datetime
import re


def ScrapeCD (number, html):
    root = lxml.html.fromstring(html)
#    print root.text_content()
    PNumber = "%04d" % (number)
    print PNumber

    
    CNSearch = root.cssselect('span#CompanyName')
#    print CNSearch[0].text_content()
    Cname = CNSearch[0].text_content()
    print "CompanyName:", Cname
 
    CASearch = root.cssselect('span#ShowAddress')
    CAText = CASearch[0].text_content()
    Caddress1 = re.sub("\r", " ", CAText)
    print Caddress1
    searchAddress = re.search("([a-zA-Z]{2,10}?\s?)", Caddress1)
    print searchAddress
    if searchAddress != None:
        Caddress = re.sub("'s", "", Caddress1)
    else:
        Caddress = "N/A"
    print "CompanyAddress:",Caddress
    
    CPSearch = root.cssselect('span#PostCode')
    cpc = CPSearch[1].text_content()
#    print "CompanyPostcode:", cpc
    postcode = re.search("([a-zA-Z]{1,2}[1-9][0-9]?\s?[0-9][0-9]?[a-zA-Z]{1,2})", cpc)
    if postcode != None:
        Cpostcode = str(postcode.group(0))
        print "CompanyPostcode:", Cpostcode
    else:
        Cpostcode = "N/A"
        print "CompanyPostcode:", Cpostcode

    Search1st = re.search('<p class="address">', html)

    MainSearch = root.cssselect('p.address')
    i = 0
    l = 0
    TelSearch = "N/A"
    FaxSearch = "N/A"
    MobileSearch = "N/A"
    WebSearch = "N/A"
    EmailSearch = "N/A"

    while i <= 4:     
        try:    
            i += 1
            MainSearch[i].text_content()
#            print i
        except IndexError:
            l = i  
#            print l  
#            print "EndLine of p.address of Cnumber: ", PNumber
            break
    j = l
#    print j

    k = j - 1

    while k >= 0:
        try:
            k -= 1
            MS = MainSearch[k].text_content()
    #        print MS
            if re.search("t. ", MS) != None:
                TelSearch = MS
    #            print "Telephone: ", TelSearch
            if re.search("f. ", MS) != None:
                FaxSearch = MS
#                print "FaxNO: ", FaxSearch
            if re.search("m. ", MS) != None:
                MobileSearch = MS
#                print "MobileNO: ", MobileSearch
            if re.search("w. ", MS) != None:
                WebSearch = MS
#                print "Website: ", WebSearch
            if re.search("e. ", MS) != None:
                EmailSearch = MS
#                print "Email: ", EmailSearch
        except IndexError:
            print "No data"
            break
    
#    print TelSearch, ", ", FaxSearch, ", ", MobileSearch, ", ", WebSearch, ", ", EmailSearch
    
    Ctel = re.sub("([a-z]\.\s?)", "", TelSearch)
    TelSearch = re.search("([a-zA-z]{2,10}\s?[a-zA-z]{2,10}\s?[a-zA-z]{2,10}\s?)", Ctel)
#    print TelSearch
    if TelSearch != None:
        TelConvert = str(TelSearch.group(0))
        TCsub = re.sub(TelConvert, "01624 ", Ctel)
        Ctel = TCsub
    else:
        Ctel = Ctel
    print "CompanyTelephone: ", Ctel

    Cfax = re.sub("([a-z]\.\s?)", "", FaxSearch)
    FaxSearch = re.search("([a-zA-z]{2,10}\s?[a-zA-z]{2,10}\s?[a-zA-z]{2,10}\s?)", Cfax)
    if FaxSearch != None:
        FaxConvert = str(FaxSearch.group(0))
        FCsub = re.sub(FaxConvert, "01624 ", Cfax)
        Cfax = FCsub
    else:
        Cfax = Cfax
    print "COmpanyFax: ", Cfax

    Cmobile = re.sub("([a-z]\.\s?)", "", MobileSearch)
    print "CompanyMobile: ", Cmobile

    Cweb = re.sub("w. ", "", WebSearch)
    WebCheck = re.search("www.", Cweb)
    if WebCheck != None:
        Cweb = Cweb
    else:
        Cweb = "N/A"
    print "CompanyWebsite: ", Cweb

    Cemail = re.sub("([a-z]\.\s?)", "", EmailSearch)
    EmailCheck = re.search("@", Cemail)
    if EmailCheck != None:
        Cemail = Cemail
    else:
        Cemail = "N/A"

    
    print "CompanyEmail: ", Cemail


    data = {"Cnumber":PNumber, "CompanyName":Cname, "Address":Caddress, "PostCode":Cpostcode, "ContactNO":Ctel, "MobileNO":Cmobile, "FaxNO":Cfax, "Website":Cweb, "Email":Cemail}
    
    
    scraperwiki.sqlite.save(unique_keys=["Cnumber"], data=data, table_name="CompanyDetails")

    print "###########################################################################################################"


def MainScrape():
    rows = scraperwiki.sqlite.attach("test2_5", "src")
    rows = scraperwiki.sqlite.select("number, html from src.Draft ORDER BY number ASC")
    for row in rows: 
        ScrapeCD(row["number"], row["html"])
    return

MainScrape()