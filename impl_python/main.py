import BigBrother
import os


def main():
    workingpath = os.getcwd()
    backup, md5list = init(workingpath)
    while True:
        try:
            newmd5list = BigBrother.getmd5List(BigBrother.getFileList(workingpath))
            # BigBrother.accurateRecovery()
        except:
            print("")


def init(workingpath):
    parentdir = os.path.abspath(os.path.dirname(os.getcwd()))
    filelist = BigBrother.getFileList(workingpath)
    md5list = BigBrother.getmd5List(filelist)
    BigBrother.savemd5List(parentdir, md5list)
    backupfile = BigBrother.getCompressed(filelist, parentdir)
    return backupfile,md5list
