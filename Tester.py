import time
import unittest
import BigBrother


class MyTestCase(unittest.TestCase):
    def test1(self):
        file = "/Users/icbm/Desktop/1582099474.301064.tar.gz"
        BigBrother.getExtracted(file,"/Users/icbm/Desktop")


if __name__ == '__main__':
    unittest.main()
