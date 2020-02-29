import os
import hashlib
import tarfile
import time
import json

'''
libBigBrother version 1.0.0
By icbmicbm
libBigBrother is the library needed by Project BigBrother.
'''


def getFile(path, rlist):
    """
    获取单个目录下的文件，此函数仅被getFileList调用
    :param path: 路径
    :param rlist: 未完成的文件列表
    :return: 返回一个文件列表
    """
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            getFile(os.path.join(path, file), rlist)
        else:
            rlist.append(os.path.join(path, file))
    return rlist


def getFileList(path):
    """
    递归地获取一路径下的所有文件
    :param path: 需要扫描的路径
    :return: 该路径下所有文件的列表
    """
    rlist = []
    getFile(path, rlist)
    return rlist


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


def getmd5List(rlist):
    """
    计算一个rlist内所有文件的md5
    :param rlist: 文件列表
    :return: md5列表
    """
    md5list = {}
    for i in rlist:
        md5list[i] = md5Sum(i)
    return md5list


def savemd5List(outpath, md5list):
    """
    储存一个md5list
    :param outpath: 输出目录
    :param md5list: 需要储存的md5list
    :return: 保存路径
    """
    dump = json.dumps(md5list)
    try:
        savepath = os.path.join(outpath,"md5list.txt")
        md5file = open(savepath, "a")
        md5file.write(dump)
        md5file.close()
        return savepath
    except:
        print("error saving md5 list")


def readmd5List(file):
    """
    读取一个md5列表
    :param file: md5列表路径
    :return: 返回读取的md5列表
    """
    try:
        md5list = open(file, "r")
        md5list = json.loads(md5list)
        return md5list
    except:
        print("error reading md5 list")


def getCompressed(rlist, outpath):
    """
    压缩rlist内的所有文件
    :param rlist: 文件列表
    :param outpath: 压缩文件储存位置
    :return: 储存路径
    """
    for i in rlist:
        i = os.path.basename(i)
    filepath = outpath + str(time.time()) + ".tar.gz"
    compressed = tarfile.open(filepath, "x:gz")
    for i in rlist:
        try:
            compressed.add(i)
        except:
            print("error handling " + i)
            break
    compressed.close()
    return filepath


# TODO need rework
def md5Check(md5list:dict, path:str):
    """
    将一个目录下的文件与md5list中的文件对比，返回md5值改变的文件
    :param md5list: getMd5list生成的字典
    :param path: 需要进行对比的路径
    :return: 被更改的文件列表 新增文件列表
    """
    changed = []
    new = []
    checklist = getFileList(path)
    originlist = md5list
    newlist = getmd5List(checklist)
    for i in checklist:
        if originlist[i] == newlist[i]:
            continue
        elif originlist[i] != newlist[i] and newlist[i] in originlist.keys():
            changed.append(i)
        elif newlist[i] not in originlist.keys():
            new.append(i)
    return changed, new


def getExtracted(file, outpath):
    """
    解压一个压缩文件
    :param file: 压缩文件
    :param outpath: 输出路径
    :return: 无返回值
    """
    compressed = tarfile.open(file)
    try:
        compressed.extractall(path=outpath)
    except:
        print("error extracting")

# 将在下个版本移除deleteNewFile
def deleteNewFile(md5list, rlist):
    """
    删除不在md5list中的文件
    :param md5list: 已计算的md5list
    :param rlist: 当前的所有文件列表
    :return: 被删除文件列表
    """
    deleted = []
    for i in rlist:
        if i not in md5list.keys():
            os.remove(i)
            deleted.append(i)
    return deleted


def accurateRecovery(rlist, inpath, outpath):
    """
    从备份恢复文件
    :param rlist: 需要还原的文件
    :param inpath: 备份文件路径
    :param outpath: 被还原文件路径
    :return: 无返回值
    """
    inlist = getFileList(inpath)
    outlist = getFileList(outpath)
    for i in range(len(rlist)):
        rlist[i] = os.path.join(inpath, rlist[i][1:])
    for j in range(min(len(inlist), len(outlist))):
        if inlist[j] in rlist:
            os.replace(inlist[j], os.path.join(outpath, os.path.basename(inlist[j])))
