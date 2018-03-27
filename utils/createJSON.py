# createJSON.py
# Author: Moises Marin
# Date: November 28, 2017
# Purpose: To create JSON from html file
#
#
from CheckPrice import CheckPrice
import urllib
import re
import os
import time
import glob
import sys
import json

def parse(config_file):
    if config_file:
        checkPrice=CheckPrice(config_file)
        for title in checkPrice.runlist:

            line_identifier=checkPrice.sites[title]['collection']
            line_base_url=checkPrice.sites[title]['url'].split(".com")[0].strip()+".com"
            dir_list=glob.glob('./_downloads/'+line_identifier+'*')
            mongo_file = open('./mongo_file_'+line_identifier, 'w')
            
            for filename in dir_list:
                if re.search("www.elpalaciodehierro.com", line_base_url):

                    #print "\n"+"Processing : "+filename

                    color=''
                    product_name=''
                    product_url_page=''
                    product_trademark=''
                    product_url_picture=''
                    product_retailPrice=''
                    product_originalPrice=''
                    product_id_model=''
                    size=[]
                    item={}
                    data={}
                    products={}
                    color_array={}
                    colorwayPrimaryImages={}

                    brand_keyword="brand:'"
                    brand_split="'"
                    brand_position=1

                    name_keyword="prod:'"
                    name_split="'"
                    name_position=1

                    image_keyword="<img id=\"image\""
                    image_split="\""
                    image_position=3

                    id_keyword="<img id=\"image\""
                    image_split="\""
                    image_position=3


                    currency_rate=18.03


                    color_flag=False
                    ignorecase = re.compile('.jpg', re.IGNORECASE)
                    color_image_found=False
                    color_id=''


                    with open(filename) as search:
                        for line in search:
                        
                    
                            if re.search("Product.Config", line):
                                d=line.split("(")[1].replace(");", "")
                                #print d
                                json_data = json.loads(d)
                                #print json_data
                                            
                                product_retailPrice= json_data['basePrice']
                                product_originalPrice= json_data['oldPrice']  
                                for option in json_data['attributes']['592']['options']:
                                    for key in  option['products']:
                                        products[key]={
                                                    'color':'',
                                                    'size':'',
                                                    'retailPrice':product_retailPrice,
                                                    'originalPrice':product_originalPrice
                                                    }            
                                
                                
                                for option in json_data['attributes']['592']['options']:
                                    #print option['label']
                                    #print option['products']
                                    for key in option['products']:
                                        products[key]['size']=option['label']
                                                    
                                for option in json_data['attributes']['92']['options']:
                                    #print option['label']
                                    #print option['products']
                                    for key in option['products']:
                                        products[key]['color']=option['label']
                                        #this should change to capture other colors
                                        color=option['label']
                                        
                                #print products

                            # if re.search("dataLayer =", line):
                            #     d=line.split("[")[1].split("]")[0].replace("'","\"").replace("Women\"Secret", "Women'Secret").replace("\"s ", "'s ").replace("\"d ", "'d ").replace("\"S(", "'S(").replace("D\"A", "D'A")
                            #     #print d
                            #     try:
                            #         json_data = json.loads(d)
                            #     except Exception:
                            #         print "Bad JSON: \n"+d
                            #         break
                                

                            #     #print json_data['photo'].replace(":","/").replace("///","://")
                            #     product_url_page= json_data['URL'].replace(":","/").replace("///","://")
                            #     #print json_data['pageTitle'].split("-")[0].strip()
                            #     product_id_model=json_data['prodIDsku']
                            
                            if re.search("dataLayer =", line):
                                try:
                                    product_url_page=line.split("'URL':'")[1].split("'")[0].replace(":","/").replace("///","://")
                                except Exception:
                                    print ("======== E X C E P T I O N ================\n")
                                    print ("This failed\n")
                                    print (line)
                                    print ("======== E X C E P T I O N ================\n")


                            if re.search(brand_keyword, line):
                                product_trademark= line.split(brand_split)[brand_position].strip()
                                #print product_trademark
                            
                            if re.search(name_keyword, line):
                                product_name= line.split(name_split)[name_position].strip()
                                #print product_name
                                
                            if re.search(image_keyword, line):
                                product_url_picture= line.split(image_split)[image_position].strip()
                                #print product_url_picture
                            
                            #find links to other colors
                            if re.search('thumbnails-container bottom swatch-', line):
                                #print ("color started:"+line.split(' swatch')[1].replace("-",""))
                                color_id=line.split(' swatch')[1].replace("-","")
                                color_flag=True
                                color_image_found=False

                            #search 1st jpg
                            if re.search(ignorecase, line) and color_flag and not color_image_found:
                                #print (line.strip().split("\"")[1])
                                color_image_url=(line.strip().split("\"")[1].replace(" ","%20"))
                                color_image_found=True
                                if color_id!='parent':
                                    color_array[color_id]={
                                        'color':color_image_url
                                    } 


                            if re.search('</div>', line) and color_flag:
                                #print ("color ended")
                                color_flag=False
                            
                            

                    #print products
                    #print color_array

                    #traverse products, use its color as key of colorway, its value is color in color array
                    #if no colors in array use default color
                    #if key is not in color array, use default color
                    for key in products:
                        #print (key+":"+products[key]['color'])
                        if len (color_array) >0:
                            try:
                                colorwayPrimaryImages[products[key]['color'].lower()]=color_array[key]['color'].replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                            except KeyError:
                                colorwayPrimaryImages[products[key]['color'].lower()]=product_url_picture.replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                        else:
                            colorwayPrimaryImages[products[key]['color'].lower()]=product_url_picture.replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                        
                    #print colorwayPrimaryImages

                    data={
                            #        '_id' : product_id_model,
                                    'name' : '['+product_trademark+'] '+product_name,
                                'currency' : 'MXN',
                                    'url' : product_url_page,
                            'image_base_url' : 'https://media.elpalaciodehierro.com/media/catalog/product',
                                    'brand' : product_trademark,
                                'basePrice' : 0,
                                'oldPrice' : 0,                          
                    'colorwayPrimaryImages' : colorwayPrimaryImages,
                            'img_url' : product_url_picture
                            }




                    data['upcMap']  =[]
                    for product in products:
                        onSale= False
                        if (int(float(products[product]['originalPrice'])) - int(float(products[product]['retailPrice'])) > 0 ):
                            onSale= True

                        item=  {
                                        'upcID' : product,
                                'retailPrice' : int(float(products[product]['retailPrice'])),
                                'retailPriceUSD' : int(float(products[product]['retailPrice']))/currency_rate,
                                        'upc' : product,
                                        'color' : products[product]['color'].lower(),
                                'originalPrice' : int(float(products[product]['originalPrice'])),
                                'originalPriceUSD' : int(float(products[product]['originalPrice']))/currency_rate,
                                            'onSale':onSale,
                                        'size' : products[product]['size']
                                    }
                        data['upcMap'].append(item)
                        basePrice=int(float(products[product]['retailPrice']))
                        oldPrice=int(float(products[product]['originalPrice']))

                    data['basePrice']=basePrice
                    data['oldPrice']=oldPrice



                    json_data = json.dumps(data)
                    #print (json_data)
                    mongo_file.write(json_data+"\n")

                elif re.search("www.julio.com", line_base_url):
                    #print ("parsing: "+filename)
                    with open(filename) as search:
                        for line in search:
                            if re.search(">var skuJson_0", line):
                                d="{\"productId\""+line.split("{\"productId\"")[1].split("};")[0]+"}"
                                #print d
                                json_data = json.loads(d)
                                product_url_picture= json_data["skus"][0]["image"]
                                product_name=json_data["name"]
                            
                                #print json_data
                            elif re.search("vtex.events.addData", line):
                                d=line.split("vtex.events.addData(")[1].split(");")[0]
                                #print d
                                json_data = json.loads(d)
                                product_url_page=json_data["pageUrl"]
                                basePrice=int(float(json_data["productPriceTo"]))
                                oldPrice=int(float(json_data["productListPriceTo"]))
                                break
                    data={
                            #        '_id' : product_id_model,
                                    'name' : '[Julio] '+product_name,
                                'currency' : 'MXN',
                                    'url' : product_url_page,
                            'image_base_url' : 'https://media.elpalaciodehierro.com/media/catalog/product',
                                    'brand' : 'Julio',
                                'basePrice' : basePrice,
                                'oldPrice' : oldPrice,                          
                    'colorwayPrimaryImages' : '',
                            'img_url' : product_url_picture
                            }

                    #print data
                    json_data = json.dumps(data)
                    #print (json_data)
                    mongo_file.write(json_data+"\n")
                    

                else:
                    pass

            mongo_file.close()

        return "completed!"
    else:
        return "No arguments!"


def parse_site(config_file, site):
    if config_file:
        with open(config_file) as f:
            for line in f:
                if line.strip():
                    if not re.search("#", line):

                        line_identifier=line.split(" ")[3].strip()


                        dir_list=glob.glob('./_downloads/'+line_identifier+'*')
                        mongo_file = open('./mongo_file_'+line_identifier, 'w')
                        for filename in dir_list:
                            #print "\n"+"Processing : "+filename

                            color=''
                            product_name=''
                            product_url_page=''
                            product_trademark=''
                            product_url_picture=''
                            product_retailPrice=''
                            product_originalPrice=''
                            product_id_model=''
                            size=[]
                            item={}
                            data={}
                            products={}
                            color_array={}
                            colorwayPrimaryImages={}

                            brand_keyword="brand:'"
                            brand_split="'"
                            brand_position=1

                            name_keyword="prod:'"
                            name_split="'"
                            name_position=1

                            image_keyword="<img id=\"image\""
                            image_split="\""
                            image_position=3

                            id_keyword="<img id=\"image\""
                            image_split="\""
                            image_position=3


                            currency_rate=18.03


                            color_flag=False
                            ignorecase = re.compile('.jpg', re.IGNORECASE)
                            color_image_found=False
                            color_id=''


                            with open(filename) as search:
                                for line in search:
                                
                            
                                    if re.search("Product.Config", line):
                                        d=line.split("(")[1].replace(");", "")
                                        #print d
                                        json_data = json.loads(d)
                                        #print json_data
                                                    
                                        product_retailPrice= json_data['basePrice']
                                        product_originalPrice= json_data['oldPrice']  
                                        for option in json_data['attributes']['592']['options']:
                                            for key in  option['products']:
                                                products[key]={
                                                            'color':'',
                                                            'size':'',
                                                            'retailPrice':product_retailPrice,
                                                            'originalPrice':product_originalPrice
                                                            }            
                                        
                                        
                                        for option in json_data['attributes']['592']['options']:
                                            #print option['label']
                                            #print option['products']
                                            for key in option['products']:
                                                products[key]['size']=option['label']
                                                            
                                        for option in json_data['attributes']['92']['options']:
                                            #print option['label']
                                            #print option['products']
                                            for key in option['products']:
                                                products[key]['color']=option['label']
                                                #this should change to capture other colors
                                                color=option['label']
                                                
                                        #print products

                                    # if re.search("dataLayer =", line):
                                    #     d=line.split("[")[1].split("]")[0].replace("'","\"").replace("Women\"Secret", "Women'Secret").replace("\"s ", "'s ").replace("\"d ", "'d ").replace("\"S(", "'S(").replace("D\"A", "D'A")
                                    #     #print d
                                    #     try:
                                    #         json_data = json.loads(d)
                                    #     except Exception:
                                    #         print "Bad JSON: \n"+d
                                    #         break
                                        

                                    #     #print json_data['photo'].replace(":","/").replace("///","://")
                                    #     product_url_page= json_data['URL'].replace(":","/").replace("///","://")
                                    #     #print json_data['pageTitle'].split("-")[0].strip()
                                    #     product_id_model=json_data['prodIDsku']
                                    
                                    if re.search("dataLayer =", line):
                                        product_url_page=line.split("'URL':'")[1].split("'")[0].replace(":","/").replace("///","://")


                                    if re.search(brand_keyword, line):
                                        product_trademark= line.split(brand_split)[brand_position].strip()
                                        #print product_trademark
                                    
                                    if re.search(name_keyword, line):
                                        product_name= line.split(name_split)[name_position].strip()
                                        #print product_name
                                        
                                    if re.search(image_keyword, line):
                                        product_url_picture= line.split(image_split)[image_position].strip()
                                        #print product_url_picture
                                    
                                    #find links to other colors
                                    if re.search('thumbnails-container bottom swatch-', line):
                                        #print ("color started:"+line.split(' swatch')[1].replace("-",""))
                                        color_id=line.split(' swatch')[1].replace("-","")
                                        color_flag=True
                                        color_image_found=False

                                    #search 1st jpg
                                    if re.search(ignorecase, line) and color_flag and not color_image_found:
                                        #print (line.strip().split("\"")[1])
                                        color_image_url=(line.strip().split("\"")[1].replace(" ","%20"))
                                        color_image_found=True
                                        if color_id!='parent':
                                            color_array[color_id]={
                                                'color':color_image_url
                                            } 


                                    if re.search('</div>', line) and color_flag:
                                        #print ("color ended")
                                        color_flag=False
                                    
                                    

                            #print products
                            #print color_array

                            #traverse products, use its color as key of colorway, its value is color in color array
                            #if no colors in array use default color
                            #if key is not in color array, use default color
                            for key in products:
                                #print (key+":"+products[key]['color'])
                                if len (color_array) >0:
                                    try:
                                        colorwayPrimaryImages[products[key]['color'].lower()]=color_array[key]['color'].replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                                    except KeyError:
                                        colorwayPrimaryImages[products[key]['color'].lower()]=product_url_picture.replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                                else:
                                    colorwayPrimaryImages[products[key]['color'].lower()]=product_url_picture.replace("https://media.elpalaciodehierro.com/media/catalog/product","")
                                
                            #print colorwayPrimaryImages

                            data={
                                    #        '_id' : product_id_model,
                                            'name' : '['+product_trademark+'] '+product_name,
                                        'currency' : 'MXN',
                                            'url' : product_url_page,
                                    'image_base_url' : 'https://media.elpalaciodehierro.com/media/catalog/product',
                                            'brand' : product_trademark,
                                        'basePrice' : 0,
                                        'oldPrice' : 0,                          
                            'colorwayPrimaryImages' : colorwayPrimaryImages,
                                    'img_url' : product_url_picture
                                    }




                            data['upcMap']  =[]
                            for product in products:
                                onSale= False
                                if (int(float(products[product]['originalPrice'])) - int(float(products[product]['retailPrice'])) > 0 ):
                                    onSale= True

                                item=  {
                                                'upcID' : product,
                                        'retailPrice' : int(float(products[product]['retailPrice'])),
                                        'retailPriceUSD' : int(float(products[product]['retailPrice']))/currency_rate,
                                                'upc' : product,
                                                'color' : products[product]['color'].lower(),
                                        'originalPrice' : int(float(products[product]['originalPrice'])),
                                        'originalPriceUSD' : int(float(products[product]['originalPrice']))/currency_rate,
                                                    'onSale':onSale,
                                                'size' : products[product]['size']
                                            }
                                data['upcMap'].append(item)
                                basePrice=int(float(products[product]['retailPrice']))
                                oldPrice=int(float(products[product]['originalPrice']))

                            data['basePrice']=basePrice
                            data['oldPrice']=oldPrice



                            json_data = json.dumps(data)
                            #print (json_data)
                            mongo_file.write(json_data+"\n")
                        
                        mongo_file.close()

        return "completed!"
    else:
        return "No arguments!"

