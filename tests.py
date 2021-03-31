import unittest
from kn15.kn15 import KN15, decode
from kn15.hydra.daily_standard import StandardObservation

class TestBulletinSplitMethods(unittest.TestCase):
  def test_split(self):
    with open('samples/6474.hydra', 'r') as f:
      s = f.read()
      self.assertEqual(len(list(decode(s))), 19)

  def test_multiline_report(self):
    with open('samples/3146.hydra', 'r') as f:
      s = f.read()
      reports = list(decode(s))
      self.assertEqual(len(reports), 1)
      self.assertEqual(reports[0], '79403 04081 10177 20000 30177 411// 62307 80640 00063 98803 00063')

class KN15Match(unittest.TestCase):
  def test(self):
    s = '10950 31082 16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99994 09090\
 92230 10101 20142 30175 499// 56563 56401 61105 61541 705V11 80001 99894 09090\
 92229 10101 20142 30175 499// 56563 56401 61105 61541 70511 80001 99894 09090\
 92228 15140 20142 30175 499// 56563 56401 61105 61541 70511 80001 99894 09090'
    self.assertEqual(KN15(s).identifier, 10950)
    self.assertEqual(KN15(s).standard_daily, '16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99994 09090')
    self.assertEqual(KN15(s).previous_standard_daily, [
      '92230 10101 20142 30175 499// 56563 56401 61105 61541 705V11 80001 99894 09090',
      '92229 10101 20142 30175 499// 56563 56401 61105 61541 70511 80001 99894 09090',
      '92228 15140 20142 30175 499// 56563 56401 61105 61541 70511 80001 99894 09090'
    ])
    day_from_second_group = StandardObservation(KN15(s).previous_standard_daily[0]).decode()[1]
    self.assertEqual(day_from_second_group, 30)

class TestDateAndTime(unittest.TestCase):
  def test_day_of_month(self):
    s = '05001 29081 10202 20212 30210 44103'
    report = KN15(s)
    self.assertEqual(report.measure_day, 29)

class TestIdentifier(unittest.TestCase):
  def test_identifier(self):
    s = '11085 94411 10503 20508 40193 73145 95511 24115 44265 74254'
    self.assertEqual(KN15(s).identifier, 11085)
    s = '41001 04081 15009 48303'
    self.assertEqual(KN15(s).identifier, 41001)


class TestDecode(unittest.TestCase):
  def test_decode(self):
    pass

class TestStage(unittest.TestCase):
  def test_positive(self):
    s = '10027 20041 30025 41299 62201 82768'
    self.assertEqual(StandardObservation(s).stage, 27)
    self.assertEqual(StandardObservation('10005').stage, 5)
    self.assertEqual(StandardObservation('10012').stage, 12)
    self.assertEqual(StandardObservation('10131').stage, 131)
    self.assertEqual(StandardObservation('11011').stage, 1011)
    s = '92230 10027 20041 30025 41299 62201 82768'
    self.assertEqual(StandardObservation(s).stage, 27)

  def test_negative(self):
    self.assertEqual(StandardObservation('15009 48303').stage, -9)
    self.assertEqual(StandardObservation('15036').stage, -36)
    self.assertEqual(StandardObservation('15223').stage, -223)
    s = '92230 15027 20041 30025 41299 62201 82768'
    self.assertEqual(StandardObservation(s).stage, -27)


class TestTemperatures(unittest.TestCase):
  def test_positive(self):
    s = '10139 20131 49904'
    self.assertEqual(StandardObservation(s).water_temperature, 9.9)
    self.assertEqual(StandardObservation(s).air_temperature, 4)
    s = '92230 15027 20041 30025 41212 62201 82768'
    self.assertEqual(StandardObservation(s).water_temperature, 1.2)
    self.assertEqual(StandardObservation(s).air_temperature, 12)

  def test_negative(self):
    s = '10303 20021 30302 41099 62203 81385 90021 00052'
    self.assertEqual(StandardObservation(s).water_temperature, 10)
    self.assertEqual(StandardObservation(s).air_temperature, None)
    s = '92230 15027 20041 30025 41299 62201 82768'
    self.assertEqual(StandardObservation(s).water_temperature, 12)
    self.assertEqual(StandardObservation(s).air_temperature, None)

  def test_missing_value(self):
    s = '10177 20000 30177 411// 62307 80640 00063'
    self.assertEqual(StandardObservation(s).air_temperature, None)
    self.assertEqual(StandardObservation(s).water_temperature, 1.1)
  

class TestDischarge(unittest.TestCase):
  def test_discharge(self):
    s = '92222 10179 20022 30180 40910 81320 00041 98809 00031'
    self.assertEqual(StandardObservation(s).daily_flow, 3.2)
    self.assertEqual(StandardObservation('10001 89500').daily_flow, 500000000)
    self.assertEqual(StandardObservation('10001 83500').daily_flow, 500)
    self.assertEqual(StandardObservation('10001 80500').daily_flow, 0.5)
    self.assertEqual(StandardObservation('10001 80005').daily_flow, 0.005)

class TestPrecipitation(unittest.TestCase):
  def test_precipitation(self):
    s = '10179 20022 30180 40910 81320 99940 00041'
    report = StandardObservation(s)
    self.assertEqual(report.precipitation_amount, 4)
    self.assertEqual(report.precipitation_amount_half, 0.4)
    self.assertEqual(report.precipitation_duration, 'от 1 до 3 ч')
    self.assertEqual(report.precipitation_duration_half, 'менее 1 ч')

class TestsSnow(unittest.TestCase):
  def test_snow_zero(self):
    s = '10276 20071 70120'
    self.assertEqual(StandardObservation(s).snow_depth, "На льду снега нет")
    s = '92222 10276 20071 70121'
    self.assertEqual(StandardObservation(s).snow_depth, "менее 5 см")



class TestCondition(unittest.TestCase):
  def test(self):
    s = '16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99994 09090'
    self.assertEqual(StandardObservation(s).ice_conditions, [{'title': 'Ледостав, ровный ледяной покров'},
                                                             {'title': 'Ледостав неполный'},
                                                             {'title': 'Ледяной покров с полыньями (промоинами, пропаринами)',
                                                              'intensity': 10}])

    self.assertEqual(StandardObservation(s).water_conditions, [{'title': 'Лесосплав', 'intensity': 50},
                                                               {'title': 'Залом леса ниже поста'},
                                                               {'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}])

    s = '92222 16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99994 09090'
    self.assertEqual(StandardObservation(s).ice_conditions, [{'title': 'Ледостав, ровный ледяной покров'},
                                                             {'title': 'Ледостав неполный'},
                                                             {
                                                               'title': 'Ледяной покров с полыньями (промоинами, пропаринами)',
                                                               'intensity': 10}])

    self.assertEqual(StandardObservation(s).water_conditions, [{'title': 'Лесосплав', 'intensity': 50},
                                                             {'title': 'Залом леса ниже поста'},
                                                             {
                                                               'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}])

  def test_exception(self):
    s = '92222 52727'
    with self.assertRaises(Exception) as context:
      StandardObservation(s).decode()
    self.assertTrue("Dictionary does not contain match for element code" in str(context.exception))
    s = '92222 61230'
    with self.assertRaises(Exception) as context:
      StandardObservation(s).decode()
    self.assertTrue("Dictionary does not contain match for element code" in str(context.exception))

  def test_intensity(self):
    s = '10501 20021 412// 53901='
    report = StandardObservation(s)
    self.assertEqual(report.ice_conditions[0]['intensity'], 10)


if __name__ == '__main__':
  unittest.main()
