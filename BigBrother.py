import os
import hashlib
import zipfile
import time

def getFile(path,rlist):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(os.path.join(path,file)):
            getFile(os.path.join(path,file),rlist)
        else:
            rlist.append(os.path.join(path,file))
    return rlist


def getFileList(path):
    rlist = []
    getFile(path,rlist)
    return rlist


def md5Sum(file):
    fp = open(file, 'rb')
    content = fp.read()
    fp.close()
    m = hashlib.md5(content)
    file_md5 = m.hexdigest()
    return file_md5


def getMD5List(rlist):
    md5list = {}
    for i in rlist:
        md5list[i]=md5Sum(i)
    return md5list


def getCompressed(rlist):
    for i in rlist:
        i = os.path.basename(i)

    compressed = zipfile.ZipFile(str(time.time())+".zip",mode="w")
    for i in rlist:
        try:
            compressed.write(i,compress_type=zipfile.ZIP_DEFLATED)
        except:
            print("error handling "+i)
            break
    compressed.close()
print(getMD5List(getFileList("/Users/icbm/Desktop/BigBrother")))
