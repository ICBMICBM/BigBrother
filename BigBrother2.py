import os
import plyvel
import hashlib

'''
libBigBrother version 2.0.0
By icbmicbm
libBigBrother is the library needed by Project BigBrother.
'''

def getFileList(path: str):
    fileList = []
    for dirPath,dirNames,fileNames in os.walk(path):
        for f in fileNames:
            fileList.append(os.path.join(dirPath,f))
    return fileList


def saveMD5(host: str,fileList: list):
    db = plyvel.DB(host, create_if_missing=True)
    with db.write_batch() as wb:
        for i in fileList:
            wb.put(i,md5Sum(i))
    wb.write()
    db.close()

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
