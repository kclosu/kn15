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


class TestStage(unittest.TestCase):
  def test_positive(self):
    s = '79033 04081 10027 20041 30025 41299 62201 82768'
    self.assertEqual(kn15.KN15(s).stage, 27)

  def test_negative(self):
    s = '41001 04081 15009 48303'
    self.assertEqual(kn15.KN15(s).stage, -9)


class TestTemperatures(unittest.TestCase):
  def test_positive(self):
    s = '41010 04081 10139 20131 49904'
    report = kn15.KN15(s)
    self.assertEqual(report.water_temperature, 9.9)
    self.assertEqual(report.air_temperature, 4)
  
  def test_negative(self):
    s = '79432 10081 10303 20021 30302 41099 62203 81385 90021 00052'
    report = kn15.KN15(s)
    self.assertEqual(report.water_temperature, 1)
    self.assertEqual(report.air_temperature, -49)
  

class TestDischarge(unittest.TestCase):
  def test_discharge(self):
    s = '81017 10081 10179 20022 30180 40910 81320 00041 98809 00031'
    report = kn15.KN15(s)
    self.assertEqual(report.discharge, 3.2)


class TestPrecipation(unittest.TestCase):
  def test_precipation(self):
    s = '81017 10081 10179 20022 30180 40910 81320 00041 98809 00031'
    report = kn15.KN15(s)
    self.assertEqual(report.precipation_amount, 4)


if __name__ == '__main__':
  unittest.main()
