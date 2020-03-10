import unittest
import kn15


class TestBulletinSplitMethods(unittest.TestCase):
  def test_split(self):
    s = open('samples/20191010_SRUR44 UKMS 100500.hydra', 'r').read()
    self.assertEqual(len(list(kn15.decode(s))), 23)

  def test_multiline_report(self):
    s = open('samples/20191004_SRUR42 UKMS 040500 CCC.hydra', 'r').read()
    reports = list(kn15.decode(s))
    self.assertEqual(len(reports), 1)
    self.assertEqual(reports[0], '79403 04081 10177 20000 30177 411// 62307 80640 00063 98803 00063')

if __name__ == '__main__':
  unittest.main()
