import unittest
import BigBrother


class MyTestCase(unittest.TestCase):
    def test1(self):
        return BigBrother.saveMD5list(BigBrother.getMD5List(BigBrother.getFileList("/Users/icbm/Desktop")))


if __name__ == '__main__':
    unittest.main()
