# reloadCollection.py
# Author: Moises Marin
# Date: November 27, 2017
# Purpose: Call parse function
#
#
from CheckPrice import CheckPrice
import re
import os

def reload_collection(config_file):
    if config_file:
        checkPrice=CheckPrice(config_file)
        for title in checkPrice.runlist:


            line_identifier=checkPrice.sites[title]['collection']

            db_collection=line_identifier
            checkPrice.drop_collection(db_collection)
            
            # to be executed afterwards
            #mongoimport -h ds147789.mlab.com:47789 -d macys_shirts -c new_vestidos -u egypt -p pyramid123 < ./mongo_file
            
            mongo_file = "./mongo_file_"+line_identifier
            shell_command= "mongoimport -h .mlab.com: -d  -c "+line_identifier+" -u  -p  < " + mongo_file
            print (shell_command)
            os.system(shell_command)
            #os.remove(mongo_file)
        checkPrice.close_connection()
               
                        
        return "completed!"
    else:
        return "No arguments!"



