import os
import hashlib
import zipfile
import time
import json
import shutil

'''
libBigBrother version 0.0.1
By icbmicbm
libBigBrother is the library needed by Project BigBrother.
'''


def getFile(path, rlist):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            getFile(os.path.join(path, file), rlist)
        else:
            rlist.append(os.path.join(path, file))
    return rlist


def getFileList(path):
    rlist = []
    getFile(path, rlist)
    return rlist


def md5Sum(file):
    fp = open(file, 'rb')
    content = fp.read()
    fp.close()
    m = hashlib.md5(content)
    file_md5 = m.hexdigest()
    return file_md5


def getmd5List(rlist):
    md5list = {}
    for i in rlist:
        md5list[i] = md5Sum(i)
    return md5list


def savemd5List(md5list):
    dump = json.dumps(md5list)
    try:
        md5file = open(".md5list.txt", "a")
        md5file.write(dump)
        md5file.close()
    except:
        print("error saving md5 list")


def readmd5List(file):
    try:
        md5list = open(file, "r")
        md5list = json.loads(md5list)
        return md5list
    except:
        print("error reading md5 list")


def getCompressed(rlist):
    for i in rlist:
        i = os.path.basename(i)

    compressed = zipfile.ZipFile(str(time.time()) + ".zip", mode="w")
    for i in rlist:
        try:
            compressed.write(i, compress_type=zipfile.ZIP_DEFLATED)
        except:
            print("error handling " + i)
            break
    compressed.close()


def md5Check(md5list, path):
    rlist = []
    checklist = getFileList(path)
    originlist = md5list
    newlist = getmd5List(checklist)
    for i in checklist:
        if originlist[i] == newlist[i]:
            continue
        elif originlist[i] != newlist[i]:
            rlist.append(i)
    return rlist


def getExtracted(file,outpath):
    compressed = zipfile.ZipFile(file,"r")
    try:
        for i in compressed.namelist():
            compressed.extract(i,outpath)
    except:
        print("error extracting")


def deleteNewFile(md5list,rlist):
    deleted = []
    for i in rlist:
        if i not in md5list.keys():
            os.remove(i)
            deleted.append(i)
    return deleted


def recovery(inpath,outpath):
    for i,j in getFileList(inpath),getFileList(outpath):
        try:
            shutil.move(i,j)
        except:
            print("error recovering file")
            continue

def accurateRecovery(rlist,inpath,outpath):
    for i,j in getFileList(inpath),getFileList(outpath):
        if j in rlist:
            try:
                shutil.move(i,j)
            except:
                print("error recovering file")
        else:
            continue
