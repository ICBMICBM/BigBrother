import os
import plyvel
import hashlib
import json
import tarfile
import time

'''
libBigBrother version 2.0.0
By icbmicbm
libBigBrother is the library needed by Project BigBrother.
'''

# tested
def getFileList(path: str):
    fileList = []
    for dirPath,dirNames,fileNames in os.walk(path):
        for f in fileNames:
            fileList.append(os.path.join(dirPath,f))
    return fileList

# not tested
def saveMD5(host: str,fileList: list):
    db = plyvel.DB(host, create_if_missing=True)
    with db.write_batch() as wb:
        for i in fileList:
            key = i.encode(encoding="utf-8")
            value = json.dumps({"sum":md5Sum(i),"locked":True}).encode(encoding="utf-8")
            wb.put(key,value)
    wb.write()
    db.close()

# tested
def md5Sum(file):
    """
    计算一个文件的md5值
    :param file: 需要处理的文件
    :return: 返回一个文件的md5值
    """
    fp = open(file, 'rb')
    content = fp.read()
    fp.close()
    m = hashlib.md5(content)
    file_md5 = m.hexdigest()
    return file_md5

# tested
def getCompressed(fileList, outpath):
    """
    压缩fileList内的所有文件
    :param fileList: 文件列表
    :param outpath: 压缩文件储存位置
    :return: 储存路径
    """
    for i in fileList:
        i = os.path.basename(i)
    filepath = os.path.join(outpath,str(time.time()) + ".tar.gz")
    compressed = tarfile.open(filepath, "x:gz")
    for i in fileList:
        try:
            compressed.add(i)
        except Exception as e:
            print(e)
            break
    compressed.close()
    return filepath

# tested
def md5check(host: str,fileList: list):
    missing = []
    toremove = []
    toreplace = []
    db = plyvel.DB(host, create_if_missing=False)
    oldfile = db.iterator(include_value=False)
    for j in oldfile:
        j = str(j,encoding="utf-8")
        if j not in fileList:
            missing.append(j)
    for i in fileList:
        nowsum = md5Sum(i)
        oldsum = db.get(i.encode(encoding="utf-8"))
        if oldsum is None:
            toremove.append(i)
        else:
            oldsum = json.loads(str(oldsum,encoding="utf-8"))["sum"]
            print(i," ",nowsum," ",oldsum)
            if nowsum != oldsum:
                print("appending",i)
                toreplace.append(i)
    db.close()
    return missing, toremove, toreplace

# not tested
def getCompressed(rlist, outpath):
    """
    压缩rlist内的所有文件
    :param rlist: 文件列表
    :param outpath: 压缩文件储存位置
    :return: 储存路径
    """
    for i in rlist:
        i = os.path.basename(i)
    filepath = os.path.join(outpath,str(time.time()) + ".tar.gz")
    compressed = tarfile.open(filepath, "x:gz")
    for i in rlist:
        try:
            compressed.add(i)
        except Exception as e:
            print(e)
            break
    compressed.close()
    return filepath
