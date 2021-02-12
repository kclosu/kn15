import unittest
import kn15


class TestBulletinSplitMethods(unittest.TestCase):
  def test_split(self):
    with open('samples/6474.hydra', 'r') as f:
      s = f.read()
      self.assertEqual(len(list(kn15.decode(s))), 19)

  def test_multiline_report(self):
    with open('samples/3146.hydra', 'r') as f:
      s = f.read()
      reports = list(kn15.decode(s))
      self.assertEqual(len(reports), 1)
      self.assertEqual(reports[0], '79403 04081 10177 20000 30177 411// 62307 80640 00063 98803 00063')


class TestStage(unittest.TestCase):
  def test_positive(self):
    s = '79033 04081 10027 20041 30025 41299 62201 82768'
    self.assertEqual(kn15.KN15(s).stage, 27)
    self.assertEqual(kn15.KN15('79033 04081 10005').stage, 5)
    self.assertEqual(kn15.KN15('79033 04081 10012').stage, 12)
    self.assertEqual(kn15.KN15('79033 04081 10131').stage, 131)
    self.assertEqual(kn15.KN15('79033 04081 11011').stage, 1011)

  def test_negative(self):
    s = '41001 04081 15009 48303'
    self.assertEqual(kn15.KN15(s).stage, -9)
    self.assertEqual(kn15.KN15('41001 04081 15036').stage, -36)
    self.assertEqual(kn15.KN15('41001 04081 15223').stage, 223)

class TestIdentifier(unittest.TestCase):
  def test_identifier(self):
    s = '11085 94411 10503 20508 40193 73145 95511 24115 44265 74254'
    self.assertEqual(kn15.KN15(s).identifier, '11085')
    s = '41001 04081 15009 48303'
    self.assertEqual(kn15.KN15(s).identifier, '41001')


class TestTemperatures(unittest.TestCase):
  def test_positive(self):
    s = '41010 04081 10139 20131 49904'
    report = kn15.KN15(s)
    self.assertEqual(report.water_temperature, 9.9)
    self.assertEqual(report.air_temperature, 4)
  
  def test_negative(self):
    s = '79432 10081 10303 20021 30302 41099 62203 81385 90021 00052'
    report = kn15.KN15(s)
    self.assertEqual(report.water_temperature, 10)
    self.assertEqual(report.air_temperature, None)
  
  def test_missing_value(self):
    s = '79403 04081 10177 20000 30177 411// 62307 80640 00063'
    report = kn15.KN15(s)
    self.assertEqual(report.air_temperature, None)
    self.assertEqual(report.water_temperature, 1.1)
  

class TestDischarge(unittest.TestCase):
  def test_discharge(self):
    s = '81017 10081 10179 20022 30180 40910 81320 00041 98809 00031'
    report = kn15.KN15(s)
    self.assertEqual(report.discharge, 3.2)

class TestPrecipitation(unittest.TestCase):
  def test_precipitation(self):
    s = '81017 10081 10179 20022 30180 40910 81320 00041 98809 00031'
    report = kn15.KN15(s)
    self.assertEqual(report.precipitation_amount, 4)

class TestsSnow(unittest.TestCase):
  def test_snow_zero(self):
    s = '70844 20081 10276 20071 70120'
    report = kn15.KN15(s)
    self.assertEqual(report.snow_depth, "На льду снега нет")

class TestDateAndTime(unittest.TestCase):
  def test_day_of_month(self):
    s = '05001 29081 10202 20212 30210 44103'
    report = kn15.KN15(s)
    self.assertEqual(report.measure_day, '29')

class TestDecode(unittest.TestCase):
  def test_decode(self):
    pass


class TestIce(unittest.TestCase):
  def test_intensity(self):
    s = '08945 21081 10501 20021 412// 53901='
    report = kn15.KN15(s)
    self.assertEqual(report.ice_conditions[0]['intensity'], 10)


if __name__ == '__main__':
  unittest.main()
