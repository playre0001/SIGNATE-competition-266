import utils
import config

def CreateLearningData(src):
    images=[]
    strs={}
    nums=[]
    category=[]
    outputs=[]

    for key in src:
        if key in config.IMAGE_HEADER:
            images.append(src[key])

        elif key in config.STR_HEADER:
            strs[key]=src[key]

        elif key in config.CATEGORY_HEADER:
            category.append(src[key])
            
        elif key in "y":
            outputs.append(src[key])

        else:
            nums.append(src[key])
    
    return images,strs,utils.ConvertTensor(nums),utils.ConcateTensor(category),outputs

def Preprocess(train_path,test_path):
    train_dst=None
    test_dst=None
    
    rowbase_train,clm_names_train=utils.ConvertRowBaseDictionaly(utils.LoadCSV(train_path))
    del clm_names_train
    
    mean_dict={}
    stddev_dict={}
    items={}

    for key in rowbase_train.keys():
        if key=="amenities":
            rowbase_train[key],items[key]=utils.ToOneHotVector([x.replace("{","").replace("}","").replace('"',"").split(",") for x in rowbase_train[key]])
        else:
            if config.CSV_HEADER_TYPE[key] in ("INT","FLOAT","DATE"):
                rowbase_train[key],mean_dict[key],stddev_dict[key]=utils.Normalization(rowbase_train[key])
            # elif config.CSV_HEADER_TYPE[key] in ("IMAGEURL",):
            #     rowbase_train[key]=utils.ImageNormalization(rowbase_train[key])
            elif config.CSV_HEADER_TYPE[key] in ("CATEGORY",):
                rowbase_train[key],items[key]=utils.ToOneHotVector([[x] for x in rowbase_train[key]])
            # elif config.CSV_HEADER_TYPE[key] in ("STR",):
            #     rowbase_train[key]=utils.ToOneHotVector([x.split(" ") for x in rowbase_train[key]])

    train_dst=CreateLearningData(rowbase_train)

    if test_path is not None:
        rowbase_test,clm_names_test=utils.ConvertRowBaseDictionaly(utils.LoadCSV(test_path))
        del clm_names_test

        for key in rowbase_test.keys():
            if key=="amenities":
                rowbase_test[key],_=utils.ToOneHotVector([x.replace("{","").replace("}","").replace('"',"").split(",") for x in rowbase_test[key]],items[key])
            else:
                if config.CSV_HEADER_TYPE[key] in ("INT","FLOAT","DATE"):
                    rowbase_test[key],_,_=utils.Normalization(rowbase_test[key],mean=mean_dict[key],stddev=stddev_dict[key])[:100]
                # elif config.CSV_HEADER_TYPE[key] in ("IMAGEURL",):
                #     rowbase_test[key]=utils.ImageNormalization(rowbase_test[key])
                elif config.CSV_HEADER_TYPE[key] in ("CATEGORY",):
                    rowbase_test[key],_=utils.ToOneHotVector([[x] for x in rowbase_test[key]],items[key])
                # elif config.CSV_HEADER_TYPE[key] in ("STR",):
                #     rowbase_test[key],_=utils.ToOneHotVector([x.split(" ") for x in rowbase_test[key]])

        test_dst=CreateLearningData(rowbase_test)

    return train_dst,test_dst
