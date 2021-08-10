import os
import csv
import datetime
import numpy as np
#import cv2
import tensorflow as tf
import copy

import config
from type import ConvertValueType

def LoadCSV(path):
    assert os.path.splitext(path)[1]==".csv" or os.path.splitext(path)[1]==".CSV"

    dst=None

    with open(path,"r",encoding="utf-8") as fp:
        reader=csv.reader(fp)
        dst=[x for x in reader]

    return dst

def ConvertRowBaseDictionaly(tables):
    clm_names=tables[0]
    dst={name:[] for name in clm_names}

    for row in tables[1:]:
        for i,data in enumerate(row):
            dst[clm_names[i]].append(ConvertValueType(config.CSV_HEADER_TYPE[clm_names[i]],data))

    for key in dst.keys():
        if key in config.NUMBER_HEADER:
            dst[key]=np.array(dst[key])

    return dst,clm_names
      
def Normalization(datas,mean=None,stddev=None):
    temp=datas.astype(np.float32)

    if mean is None:
        mean=np.mean(temp)
    if stddev is None:
        stddev=np.std(temp)

    return (temp-mean)/stddev,mean,stddev

def ToOneHotVector(datas,items=None):
    if items is None:
        items=set()

        datas=list(datas)
        for i in range(len(datas)):
            for data in datas[i]:
                items.add(data)

    keep_items=copy.copy(items)

    item_num=len(items)
    item_position={items.pop():i for i in range(item_num)}

    for i in range(len(datas)):
        temp=np.zeros([item_num],dtype=np.float32)
        for j in range(len(datas[i])):
            pos=item_position.get(datas[i][j],-1)
            if not pos!=-1:
                temp[pos]=1.

        datas[i]=temp

    return datas,keep_items
            
# def ImageNormalization(image_paths):
#     cv2.imwrite(os.path.join("DownloadImages","NODATA.jpg"),np.zeros((224,224,3),np.uint8))
#     for i in range(len(image_paths)):
#         try:
#             image=tf.io.read_file(image_paths[i])
#             extention=str(image_paths[i]).replace("'","").split(".")[-1]

#             if extention in ("png","PNG"):
#                 image=tf.image.decode_png(image,channels=3)
#             elif extention in ("jpg","jpeg","JPG","JPEG"):
#                 image=tf.image.decode_jpeg(image,channels=3)
#             else:
#                 image=tf.io.decode_image(image)
#         except:
#             #print(image_paths[i])
#             image_paths[i]=os.path.join("DownloadImages","NODATA.jpg")

#         # image=cv2.imread(image_paths[i])
#         # if image is None:
#         #     image_paths[i]=os.path.join("DownloadImages","NODATA.jpg")
    
#     return image_paths

#     # dir_path="NormalizedImages"
#     # os.makedirs(dir_path,exist_ok=True)

#     # for i in range(len(image_paths)):
#     #     file_name=os.path.splitext(os.path.basename(image_paths[i]))[0]
#     #     file_path=os.path.join(dir_path,file_name)
        
#     #     if not os.path.isfile(file_path):
#     #         if file_name=="Z":
#     #             np.save(file_path,np.zeros((224,224,3),dtype=np.float32))

#     #         else:
#     #             image=cv2.imread(image_paths[i])
#     #             if image is None:
#     #                 file_path=os.path.join(dir_path,"Z")
#     #             else:
#     #                 image=cv2.resize(image,(224,224))
#     #                 image=image.astype(np.float32)
#     #                 image/=255.
#     #                 np.save(file_path,image)

#     #     image_paths[i]=file_path+".npy"

#     # return image_paths

def ConvertTensor(array):
    datas_length=len(array[0])
    dst=[]
    for i in range(1,len(array)):
        assert datas_length<=len(array[i])

    for i in range(datas_length):
        temp=[array[0][i]]
        for j in range(1,len(array)):
            temp.append(array[j][i])
        dst.append(np.array(temp))

    return dst

def ConcateTensor(array):
    dst=[]
    data_lengh=len(array[0])
    for i in range(1,len(array)):
        assert data_lengh<=len(array[i])
    
    for i in range(data_lengh):
        temp=array[0][i]
        for j in range(1,len(array)):
            temp=np.concatenate([temp,array[j][i]])
        dst.append(temp)

    return dst

def RMSE(y_true,y_pred):
    return tf.math.sqrt(tf.math.reduce_mean(tf.math.square(y_pred - y_true)))

def CSVWrite(prediced):
    summary=[x[0] for x in prediced]

    os.makedirs(config.OUTPUT_PATH,exist_ok=True)

    with open(os.path.join(config.OUTPUT_PATH,"test_prediction.csv"),"w",encoding="utf-8",newline="") as fp:
        writer=csv.writer(fp)
        for i in range(len(summary)):
            writer.writerow([i,summary[i]])
