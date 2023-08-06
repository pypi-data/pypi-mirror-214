import pickle
import gzip

def ReadPickleFile(filePathNm, gzipInd=True):
    try:
        if gzipInd:
            with gzip.open(filePathNm, 'rb') as f:
                retVal = pickle.load(f)      
        else:
            with open(filePathNm, 'rb') as f:
                retVal = pickle.load(f)      
    except:
        retVal = {}
    
    return retVal

def WritePickleFile(filePathNm, currData, gzipInd=True):
    if gzipInd:
        with gzip.open(filePathNm, 'wb') as f:
            pickle.dump(currData, f)       
    else:
        with open(filePathNm, 'wb') as f:
            pickle.dump(currData, f)           

def MergeData(currData, newData):
    # 기존 데이터의 우선순위는 2, 신규 데이터는 우선순위 1로 병합 후 sort
    totList = [[x[0], 2] + x[1:] for x in currData ] \
            + [[x[0], 1] + x[1:] for x in newData ]
    totList.sort()

    # 중복데이터 제거 및 임시 우선순위 삭제
    noDupList = [ [data[0]] + data[2:] for idx, data in enumerate(totList) if idx == 0 or data[0] > totList[idx-1][0] ] 

    return noDupList