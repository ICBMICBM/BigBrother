import time
import unittest
import BigBrother


class MyTestCase(unittest.TestCase):
    def test1(self):
        targetfile = BigBrother.getFileList("/Users/icbm/Desktop/Test Folder")
        md5list = BigBrother.getmd5List(targetfile)
        print(md5list)
        path = BigBrother.getCompressed(targetfile,"/Users/icbm/Desktop/")
        file = open("/Users/icbm/Desktop/Test Folder/sample.txt","w")
        file.write("an input")
        file.close()
        print(BigBrother.md5Sum("/Users/icbm/Desktop/Test Folder/sample.txt"))
        BigBrother.getExtracted(path,"/Users/icbm/Desktop")
        targetlist = BigBrother.md5Check(md5list,"/Users/icbm/Desktop/Test Folder")
        print(targetlist)
        BigBrother.accurateRecovery(targetlist,"/Users/icbm/Desktop","/Users/icbm/Desktop/Test Folder")

if __name__ == '__main__':
    unittest.main()
