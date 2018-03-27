# CheckPrice.py
# Author: Moises Marin
# Date: December 3, 2017
# Purpose: Define CheckPrice class
#
#

from pymongo import MongoClient
import re
import json



class CheckPrice:

    connection = MongoClient()
    db_name=''
    configuration={}
    runlist=[]
    sites={}
    twitterAccounts={}

    def __init__(self,config_file):
        if config_file:
            with open(config_file) as f:
                self.configuration = json.load(f)
            line_db_connect=self.configuration['DB']
            self.connection = MongoClient(line_db_connect)
            self.db_name= line_db_connect.split("/")[3].strip()
            self.runlist=self.configuration['RunList']['active']
            for item in self.configuration['Sites']:
                self.sites[item['title']]=item
            for item in self.configuration['TwitterAccounts']:
                self.twitterAccounts[item['name']]=item

        else:
            raise Exception("-->No config file.")

    
    def drop_collection(self, db_collection):
        db = self.connection[self.db_name][db_collection]
        db.drop()
    
    def query_collection(self, db_collection, pipe):
        db = self.connection[self.db_name][db_collection]
        return db.aggregate(pipeline=pipe)

    def find_one(self, db_collection, pipe):
        db = self.connection[self.db_name][db_collection]
        return db.find_one(pipe)

    def find_where(self, db_collection, search_pattern):
        db = self.connection[self.db_name][db_collection]
        return db.find().where(search_pattern)

    def close_connection(self):
        self.connection.close()

    def download(self):
        pass

    def parse(self):
        pass

    def reload(self):
        pass

    def clean(self):
        pass

    def tweet(self):
        pass

    def read_config(self,cfg):
        """
        Expected sections in configuration file
        PriceBotTemplateFormatVersion
        Description
        RunList
        TwitterAccounts
        Sites
        DB
        """
        with open(cfg) as f:
            data = json.load(f)
            runlist=data['RunList']['active']
            twitterAccounts=data['TwitterAccounts']
            #consumer_key
            #consumer_secret
            #access_token
            #access_token_secret
            sites=data['Sites']
            # title
            # url
            # twitter
            # PARM_end
            # collection
            # inner_link
            # tweet_flag
            # PARM_start

            print (data['DB'])

        return data

    def twitter_key(self, name, value):
        return self.twitterAccounts[name][value]

