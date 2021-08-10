import datetime
import os
import requests
import numpy as np
#import cv2
import re

def ConvertValueType(type_name,data):
    if type_name=="INT":
        return Toint(data)
    elif type_name=="FLOAT":
        return Tofloat(data)
    elif type_name=="BOOL":
        return Tobool(data)
    elif type_name=="STR":
        return Tostr(data)
    elif type_name=="DATE":
        return Todate(data)
    elif type_name=="CATEGORY":
        return Tocategory(data)
    elif type_name=="PERCENT":
        return Toprecent(data)
    elif type_name=="IMAGEURL":
        return Toimage(data)
    elif type_name=="ANSWER":
        return Tofloat(data)
    return None

def Toint(x):
    if x=="":
        return int("0")
    else:
        try:
            return int(float(x))
        except:
            return 0

def Tofloat(x):
    if x=="":
        return 0.
    else:
        return float(x)

def Tobool(x):
    if x=="t":
        return 1.
    else:
        return 0.

def Tostr(x):
    if x=="":
        return "NOTHING_DESCRIPTION"
    else:
        return str(x)

def Todate(x):
    if x=="":
        return 0.
    else:
        sep=re.search("[0-9]+([^0-9]+)[0-9]+",x).groups()[0]
        return datetime.datetime(*list(map(int,x.split(sep)))).timestamp()

def Toprecent(x):
    if x=="":
        return -1.
    else:
        return float(x[:-1])/100.

def Tocategory(x):
    if x=="":
        return "NOTHING_DESCRIPTION"
    else:
        return str(x)

counter=0

def Toimage(url):
    global counter
    
    if url=="":
        counter+=1
        return "Z"
    else:
        
        file_name=str(counter)+".jpg"
        dir_path="DownloadImages"
        file_path=os.path.join(dir_path,file_name)

        # if not os.path.isfile(file_path):
        #     #download image
        #     os.makedirs(dir_path,exist_ok=True)

        #     with open(file_path,"wb")as fp:
        #         fp.write(requests.get(url).content)

        counter+=1

        return file_path#cv2.imread(file_path)

