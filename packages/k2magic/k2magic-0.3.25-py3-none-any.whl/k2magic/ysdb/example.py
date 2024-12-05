from ysdbLib import *

#连接示例
client = RdbClient()
ret = client.connect("127.0.0.1", 30221)
print(ret)



#读取实时量测示例
print("*******************实时量测*****************")
ids = [1,2,3,4,5]
retRealDatas = client.readFloatRealDatasById(ids)
print("实时数据读取个数：", len(retRealDatas))
print (retRealDatas[0].id, retRealDatas[0].val)
print (retRealDatas[1].id, retRealDatas[1].val)
print (retRealDatas[2].id, retRealDatas[2].val)

#读取Bool类型实时数值
print("******************Bool类型实时******************")
ids = [1,2,3,4,5]
retBoolDatas = client.readBoolRealDatasById(ids)
print("retBoolDatas count:", len(retBoolDatas))
for data in retBoolDatas:
    print(data.id, data.val)


#读取INT类型实时数值
print("*****************INT类型实时*******************")
ids = [1,2,3,4,5]
retIntDatas = client.readIntRealDatasById(ids)
print("retIntDatas count:", len(retIntDatas))
for data in retIntDatas:
    print(data.id, data.val)


#读取历史量测数据示例
print("*****************历史量测数*******************")
startTm = int(time.time()) - 500000
endTm = int(time.time())
hisQuery = HisQuery(0, 1, ''.encode('utf-8'), startTm, 0, endTm, 0, 0, 0)
retHisDatas = client.readFloatHisData(hisQuery)
print("Float hisDataCount", len(retHisDatas))
for data in retHisDatas:
    print(data.tm, data.ms,  data.val)

#读取历史BOOL数据示例
print("******************历史BOOL******************")
startTm = int(time.time()) - 500000
endTm = int(time.time())
retHisDatas = client.readBoolHisData(0, 1, '', startTm, 0, endTm, 0, 0, 0)
print("Bool hisDataCount", len(retHisDatas))
for data in retHisDatas:
    print(data.tm, data.ms,  data.val)

#读取历史INT数据示例
print("*******************历史INT*****************")
startTm = int(time.time()) - 500000
endTm = int(time.time())
retHisDatas = client.readIntHisData(0, 1, '', startTm, 0, endTm, 0, 0, 0)
print("Int hisDataCount", len(retHisDatas))
for data in retHisDatas:
    print(data.tm, data.ms,  data.val)


#getPointIdAll示例
print("*******************getPointIdAll示例*****************")
retPoints = client.getPointIdAll(0)
print("getPointIdAll retPointsCount", len(retPoints))
for data in retPoints:
    print(data)

#getPointInfos
print("*******************getPointInfos示例*****************")
retPoints = client.getPointInfos(0, ids)
print("getPointInfos retPointsCount", len(retPoints))
for point in retPoints:
    print(point.tag)


#readPointHisData示例
print("*******************readPointHisData示例*****************")
hisQuery = HisQuery(0, 1, ''.encode('utf-8'), startTm, 0, endTm, 0, 0, 0)
retPoints = client.readPointHisData(hisQuery)
print("readPointHisData retPointsCount", len(retPoints))
for data in retPoints:
    print(data.fVal)


#readPointHisDatas示例
print("*******************readPointHisDatas示例*****************")
hisQuery1 = HisQuery(0, 1, ''.encode('utf-8'), startTm, 0, endTm, 0, 0, 0)
hisQuery2 = HisQuery(0, 2, ''.encode('utf-8'), startTm, 0, endTm, 0, 0, 0)
hisQueryList = []
hisQueryList.append(hisQuery1)
hisQueryList.append(hisQuery2)
retDataLists = client.readPointHisDatas(hisQueryList)
print("readPointHisDatas retDataListsCount", len(retDataLists))
for data in retDataLists:
    print(len(data))



#writeCtrlDataById


#订阅示例1
#int(*ptr)(stPointRealData *pData, int cnt)
def subscribePointRealDataCallback (realDataArr, cnt):
    print("subscribePointRealDataCallback:", cnt)
    realDataList = [realDataArr[i] for i in range(cnt)]
    for data in realDataList:
        print(data.tm, data.ms, data.fVal)
    
    return 1;
    
ret = client.evtConnect(30223)
print("evtConnect:", ret)

callbackFunc = CFUNCTYPE(c_int, POINTER(PointRealData), c_int)
callback_ptr = callbackFunc(subscribePointRealDataCallback)
ret = client.subscribePointRealData(callback_ptr)
print("subscribcePointRealData ret:" ,ret)



#订阅示例2
#subscribeBlobRealData(int handle, int(*ptr)(stBlobDataInfo *pData, int cnt));
def subscribeBlobRealDataCallback (blobDataArr, cnt):
    print("subscribeBlobRealDataCallback:", cnt)
    blobDataList = [blobDataArr[i] for i in range(cnt)]
    for data in blobDataList:
        print(data.tm, data.ms, data.c_int)
    
    return 1;
    
ret = client.evtConnect(30223)
print("evtConnect:", ret)

callbackFunc = CFUNCTYPE(c_int, POINTER(PointRealData), c_int)
callback_ptr = callbackFunc(subscribePointRealDataCallback)
ret = client.subscribePointRealData(callback_ptr)
print("subscribcePointRealData ret:" ,ret)


name = input("任意字符回车结束：")

# 断开连接
client.disconnect()
print("Close Over!")