# tweetCollection.py
# Author: Moises Marin
# Date: November 28, 2017
# Purpose: Call parse function
#
#
from CheckPrice import CheckPrice
import re
from random import randint
import json
import tweepy
import locale
import requests
import os
import time

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

#locale.setlocale(locale.LC_ALL, 'en_US')


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def check_config(cfg):
    checkPrice=CheckPrice(cfg)
    print (checkPrice.db_name)
    print (checkPrice.runlist)
    for site in checkPrice.sites:
        print (site)
    print ("_----------------_")
    print (checkPrice.sites[checkPrice.runlist[0]])
    print ("_----------------_")
    print (checkPrice.twitterAccounts[checkPrice.sites[checkPrice.runlist[0]]['twitter'][0]])
    print ("_----------------_")
    print (checkPrice.twitter_key('ChecaTuPrecio','consumer_key'))


def tweet_prices(config_file):
    if config_file:
        checkPrice=CheckPrice(config_file)
        for title in checkPrice.runlist:
            #checkPrice.sites[title]['url']
            #checkPrice.sites[title]['twitter']
            #checkPrice.sites[title]['PARM_start']
            #checkPrice.sites[title]['PARM_end']
            
            twitter_account=checkPrice.sites[title]['twitter'][0]   
            db_collection=checkPrice.sites[title]['collection']
            line_title=title
            line_tweet_text=checkPrice.sites[title]['tweet_text']
            line_tweet_flag=checkPrice.sites[title]['tweet_flag']

            # Define tweeter account to use
            cfg = { 
                "consumer_key"        : checkPrice.twitter_key(twitter_account, 'consumer_key'),
                "consumer_secret"     : checkPrice.twitter_key(twitter_account, 'consumer_secret'),
                "access_token"        : checkPrice.twitter_key(twitter_account, 'access_token'),
                "access_token_secret" : checkPrice.twitter_key(twitter_account, 'access_token_secret')
                }

            api = get_api(cfg)

            time.sleep(1)
            # Find most expensive ####################################################################
            pipe = [{ '$group' : { '_id': None, 'max': { '$max' : "$basePrice" }}}]
            results=checkPrice.query_collection(db_collection,pipe)

            #this is a good example to print a document from an aggregation result
            for doc in results:
                print('---------------------------------')
                #print(doc)
                max_price=doc['max']
                #print('Maximum current price:',max_price)
                result_max =  checkPrice.find_one(db_collection,{ 'basePrice' : max_price })
                #print(result_max)
                #print("Marca:" + str(result_max['brand']) ) 
                #print("---> Precio: $"+ str(result_max['basePrice']))
                #print("img_url:" + result_max['img_url'])
                #print("url:" + result_max['url'])
                print('---------------------------------')
                descuento= int(100-(float(result_max['basePrice'])*100)//float(result_max['oldPrice']))
                tl1="-> Precio: $"+ str(locale.format("%d", result_max['basePrice'], grouping=True))
                #tl2="->  Antes: $"+ str(locale.format("%d", result_max['oldPrice'], grouping=True))
                #tl3="-> Descuento: "+ str(descuento) + "%"
            
                #Formato 1 
                #tweet = "#ElPalacioDeHierro\nEllas > Blusas > " + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + tl3 +"\n"+  doc_discount['url']
                #tweet = "#PreciosPalacio\n" + line_title + " + $$$ esta semana:"+"\n" + str(result_max['brand'])+ "\n" + tl1 +"\n" + result_max['url']
                tweet = line_tweet_text[0]+"\n" + str(result_max['brand'])+ "\n" + tl1 +"\n" + result_max['url']
                
                print (tweet)
                url = result_max['img_url']

                filename = 'temp.jpg'
                request = requests.get(url, stream=True)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)

                    #comment out to avoid tweet
                    if line_tweet_flag == 'yes_tweet':
                        status = api.update_with_media(filename, status=tweet)
                    os.remove(filename)
                else:
                    print("Unable to download image")    
                break

            time.sleep(2)
            # Find least expensive ####################################################################
            pipe = [{ '$group' : { '_id': None, 'min': { '$min' : "$basePrice" }}}]
            results=checkPrice.query_collection(db_collection,pipe)

            #this is a good example to print a document from an aggregation result
            for doc in results:
                print('---------------------------------')
                #print(doc)
                min_price=doc['min']
                #print('Maximum current price:',max_price)
                result_min = checkPrice.find_one(db_collection,{ 'basePrice' : min_price })
                #print(min_price)
                #print("Marca:" + str(result_min['brand']) ) 
                #print("---> Precio: $"+ str(result_min['basePrice']))
                #print("img_url:" + result_min['img_url'])
                #print("url:" + result_min['url'])
                #print('---------------------------------')
                descuento= int(100-(float(result_min['basePrice'])*100)//float(result_min['oldPrice']))
                tl1="-> Precio: $"+ str(locale.format("%d", result_min['basePrice'], grouping=True))
                #tl2="->  Antes: $"+ str(locale.format("%d", result_min['oldPrice'], grouping=True))
                #tl3="-> Descuento: "+ str(descuento) + "%"
            
                #Formato 1 
                #tweet = "#ElPalacioDeHierro\nEllas > Blusas > " + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + tl3 +"\n"+  doc_discount['url']
                #tweet = "#PreciosPalacio\n"  + line_title + " menos $ esta semana:"+"\n" + str(result_min['brand'])+ "\n" + tl1 +"\n" + result_min['url']
                tweet = line_tweet_text[1]+"\n" + str(result_min['brand'])+ "\n" + tl1 +"\n" + result_min['url']
                
                print (tweet)
                url = result_min['img_url']

                filename = 'temp.jpg'
                request = requests.get(url, stream=True)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)

                    #comment out to avoid tweet
                    if line_tweet_flag == 'yes_tweet':
                        status = api.update_with_media(filename, status=tweet)
                    os.remove(filename)
                else:
                    print("Unable to download image")    
                break

            time.sleep(3)
            # Find biggest discount ####################################################################
            pipe = [{'$group':{'_id': None, 'maxDifference': { '$max': { '$subtract': [ "$oldPrice", "$basePrice" ] }} }}]
            results=checkPrice.query_collection(db_collection,pipe)
            #this is a good example to print a document from an aggregation result
            for doc in results:
                print('---------------------------------')
                #print(doc)
                max_discount=doc['maxDifference']
                #print('Maximum discount:',max_discount)
                #result_max_discount = db.find_one().where("this.oldPrice - this.basePrice == $max_discount")
                #search_pattern = "this.basePrice ==%s" % (max_discount)
                search_pattern ="this.oldPrice - this.basePrice   ==%s" % (max_discount)
                #print(search_pattern)
                result_max_discount = checkPrice.find_where(db_collection,search_pattern)
                #print ("Using search pattern")
                #print(result_max_discount)
                for doc_discount in result_max_discount:
                    #print(doc_discount)
                    #print ("Inside deep for")
                    descuento= int(100-(float(doc_discount['basePrice'])*100)//float(doc_discount['oldPrice']))
                    tl1="-> Precio: $"+ str(locale.format("%d", doc_discount['basePrice'], grouping=True))
                    tl2="->  Antes: $"+ str(locale.format("%d", doc_discount['oldPrice'], grouping=True))
                    #tl3="---> Descuento: "+ str(descuento) + "%"
            
                    #Formato 1 
                    #tweet = "#ElPalacioDeHierro\nEllas > Blusas > " + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + tl3 +"\n"+  doc_discount['url']
                    #tweet = "#Descuentazo\n" + "Mayor descuento esta semana: " +str(descuento) + "% !" +"\n" + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + doc_discount['url']
                    #tweet = "#MayorDescuentoPalacio esta semana: " +str(descuento) + "% !" +"\n" + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + doc_discount['url']
                    tweet = line_tweet_text[2]+str(descuento) + "% !" +"\n" + str(doc_discount['brand'])+ "\n" + tl1 +"\n" + tl2 +"\n" + doc_discount['url']
                    print (tweet)
                    print('---------------------------------')
                    url = doc_discount['img_url']

                    filename = 'temp.jpg'
                    request = requests.get(url, stream=True)
                    if request.status_code == 200:
                        with open(filename, 'wb') as image:
                            for chunk in request:
                                image.write(chunk)

                        #comment out to avoid tweet
                        if line_tweet_flag == 'yes_tweet':
                            status = api.update_with_media(filename, status=tweet)
                        os.remove(filename)
                    else:
                        print("Unable to download image")    
                    break


        # close the connection to MongoDB
        #connection.close()
        checkPrice.close_connection()
                        
        return "completed!"
    else:
        return "No arguments!"



