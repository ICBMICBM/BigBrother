import BigBrother2
import unittest


class MyTestCase(unittest.TestCase):
    testPath = "/Users/icbm/Desktop/TestFolder"
    DBPath = "./testdb"

    def test1(self):
        BigBrother2.getFileList(self.testPath)

    def test2(self):
        BigBrother2.connectDB(self.DBPath)


if __name__ == '__main__':
    unittest.main()
