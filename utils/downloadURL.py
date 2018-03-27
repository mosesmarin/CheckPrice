# downloadURL.py
# Author: Moises Marin
# Date: November 27, 2017
# Purpose: To download links in a text file
#
#
from bs4 import BeautifulSoup
from CheckPrice import CheckPrice
import re
import os
import time
import requests



def download_links(config_file):
    if config_file:
        checkPrice=CheckPrice(config_file)

        file_content =''
        #webpage = urllib.URLopener()
        for title in checkPrice.runlist:

            line_url=checkPrice.sites[title]['url']
            line_start=checkPrice.sites[title]['PARM_start']
            line_end=checkPrice.sites[title]['PARM_end']
            line_identifier=checkPrice.sites[title]['collection']
            line_base_url=checkPrice.sites[title]['url'].split(".com")[0].strip()+".com"
            line_inner_link_pattern=checkPrice.sites[title]['inner_link']

            time.sleep(5)
            print ("Wait 5 seconds")
            for i in range(line_start,line_end+1):
                file_content = file_content + "\n" + line_url.replace("PARM", str(i) )
                file_path= "./_downloads/html_"+line_identifier+str(i)
                if not os.path.exists(file_path): 
                    #webpage.retrieve(line_url.replace("PARM", str(i) ), file_path)
                    #x = urllib.request.urlretrieve('https://www.google.com/')
                    #print(x.read())
                    webpage = requests.get(line_url.replace("PARM", str(i) ))
                    weblink_file = open('./'+file_path, 'w')
                    weblink_file.write(webpage.text)
                    weblink_file.close()
                else:
                    print ("HTML file exists...skipping: "+"html_"+file_path)

                if re.search("www.elpalaciodehierro.com", line_base_url):
                    with open(file_path) as link_gallery:
                        for line2 in link_gallery:
                            if re.search("<a href=\""+line_inner_link_pattern, line2):
                                inner_link= line2.strip().replace("\"","").replace("<a href=",line_base_url)
                                file_inner_link= "./_downloads/"+line_identifier+"_"+inner_link.split("/")[6] 
                                if not os.path.exists(file_inner_link):
                                    try:
                                        print (inner_link)
                                        #webpage.retrieve(inner_link, file_inner_link)
                                        webpage = requests.get(inner_link)
                                        weblink_file = open('./'+file_inner_link, 'w')
                                        weblink_file.write(webpage.text)
                                        weblink_file.close()
                                    except Exception: # catch *all* exceptions
                                        print ("Broken link!! ") + inner_link
                                else:
                                    print ("Deep File exists...skipping: "+file_inner_link)
                elif re.search("www.julio.com", line_base_url):
                    #http://www.julio.com/api/catalog_system/pub/products/variations/3105
                    with open(file_path) as link_gallery:
                        #print ("working on"+file_path)
                        soup = BeautifulSoup(link_gallery, 'html.parser')
                        all_links = set()
                        for a in soup.find_all('a', href=True):
                            all_links.add(a['href'])

                        for inner_link in all_links:
                            file_inner_link= "./_downloads/"+line_identifier+"_"+inner_link.split("/")[3] 
                            if not os.path.exists(file_inner_link):
                                try:
                                    #print inner_link
                                    #webpage.retrieve(inner_link, file_inner_link)
                                    webpage = requests.get(inner_link)
                                    weblink_file = open('./'+file_inner_link, 'w')
                                    weblink_file.write(webpage.text)
                                    weblink_file.close()
                                except Exception: # catch *all* exceptions
                                    print ("Broken link!! ") + inner_link
                            else:
                                print ("Deep File exists...skipping: "+file_inner_link)
                else:
                    print ("No site to download!")
                            
        return "completed!"
    else:
        return "No arguments!"


def download_site(site):
    if site:
        print (site)
        webpage = urllib.URLopener()
        file_path= "./_downloads/html_"+"Julio"
        webpage.retrieve(site, file_path)

                            
        return "completed!"
    else:
        return "No arguments!"
