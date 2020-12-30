import BigBrother2
import unittest
import os


class MyTestCase(unittest.TestCase):
    testPath = "/Users/icbm/Desktop/TestFolder"
    testOutPath = "/Users/icbm/Desktop/TestOutPath"
    outPath = "/Users/icbm/Desktop"
    DBPath = "./testdb"

    def test1(self):
        BigBrother2.getFileList(self.testPath)

    def test2(self):
        BigBrother2.connectDB(self.DBPath)

    def test3(self):
        BigBrother2.saveMD5(self.DBPath,BigBrother2.getFileList(self.testPath))
        missing, toremove, toreplace = BigBrother2.md5check(self.DBPath,BigBrother2.getFileList(self.testPath))
        print(missing, toremove, toreplace)

    def test4(self):
        files = BigBrother2.getFileList(self.testPath)
        BigBrother2.getCompressed(files,self.outPath)

    def test5(self):
        BigBrother2.saveMD5(self.DBPath, BigBrother2.getFileList(self.testPath))
        with open(os.path.join("/Users/icbm/Desktop/TestFolder/a.txt"),"w") as f:
            f.write("appending")
            f.close()
        missing, toremove, toreplace = BigBrother2.md5check(self.DBPath, BigBrother2.getFileList(self.testPath))
        print(missing, toremove, toreplace)

    def test6(self):
        print(BigBrother2.getCompressed(BigBrother2.getFileList(self.testPath),self.testOutPath))


if __name__ == '__main__':
    unittest.main()
