#对多组数字参数的分析: 通过多组数据判断某一特征的目标
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split as tts
from sklearn.neighbors import KNeighborsClassifier as knc 
from sklearn.metrics import accuracy_score as acc
import mml_qae.MoreErrors as me
def max_of_list(l:list):
    """给定列表返回其中最大值"""
    maxium=l[0]
    for i in l:
        try:
            i=float(i)
        except:
            raise me.DataError2   
    for j in range(0,len(l)-1):
        a=l[j];b=l[j+1]
        if b>a:
            maxium=b
    return int(maxium)        

def predict(path:str,to_name:str,need_predict:pd.DataFrame):
    try:data=pd.read_csv(path,header=0)#读入csv数据
    except:raise me.CSVError
    try:  
        x_data=data.drop([to_name],axis=1)#从data中摘取特征组
        y_data=np.ravel(data[[to_name]])#从data中摘取目标组
    except:raise me.DataError3    
    x_trainset , x_testset , y_trainset , y_testset = tts(x_data,y_data,random_state=1)
    #建立训练集(训练特征组 和 训练目标组)和测试集(测试特征组 和 训练目标组)
    n=range(1,23)
    KNNs=[knc(n_neighbors=i) for i in n]
    scores=[KNNs[i].fit(x_trainset,y_trainset).score(x_testset,y_testset) for i in range(len(KNNs))]
    best=max_of_list(scores)
    bs=scores.index(best)+1
    new=knc(algorithm="kd_tree",n_neighbors=bs)
    new.fit(x_trainset,y_trainset)
    ny=new.predict(need_predict)
    return ny

def get_score(path:str,to_name:str):
    data1=pd.read_csv(path,header=0)
    x_data=data1.drop([to_name],axis=1)#从data中摘取特征组
    y_data=np.ravel(data1[[to_name]])#从data中摘取目标组
    x_trainset , x_testset , y_trainset , y_testset = tts(x_data,y_data,random_state=1) 
    n=range(1,23)
    KNNs=[knc(n_neighbors=i) for i in n]
    scores=[KNNs[i].fit(x_trainset,y_trainset).score(x_testset,y_testset) for i in range(len(KNNs))]
    best=max_of_list(scores)
    return best 