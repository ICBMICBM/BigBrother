import os
import hashlib
import tarfile
import time
import json

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


def getCompressed(rlist, outpath):
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


def getExtracted(file, outpath):
    compressed = tarfile.open(file)
    try:
        compressed.extractall(path=outpath)
    except:
        print("error extracting")


def deleteNewFile(md5list, rlist):
    deleted = []
    for i in rlist:
        if i not in md5list.keys():
            os.remove(i)
            deleted.append(i)
    return deleted


def accurateRecovery(rlist, inpath, outpath):
    inlist = getFileList(inpath)
    outlist = getFileList(outpath)
    for i in range(len(rlist)):
        rlist[i] = os.path.join(inpath,rlist[i][1:])
    for j in range(min(len(inlist), len(outlist))):
        if inlist[j] in rlist:
            os.replace(inlist[j], os.path.join(outpath,os.path.basename(inlist[j])))
