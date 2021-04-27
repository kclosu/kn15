import unittest
from kn15.kn15 import KN15, decode
from kn15.hydra import StandardObservation

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
    s = '16161 20142 30175 499// 56563 56401 61105 61541'
    self.assertEqual(StandardObservation(s).ice_conditions, [{'title': 'Ледостав, ровный ледяной покров'},
                                                             {'title': 'Ледостав неполный'},
                                                             {'title': 'Ледяной покров с полыньями (промоинами, пропаринами)',
                                                              'intensity': 10}])

    self.assertEqual(StandardObservation(s).water_conditions, [{'title': 'Лесосплав', 'intensity': 50},
                                                               {'title': 'Залом леса ниже поста'},
                                                               {'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}])

    s = '92222 16161 20142 30175 499// 56563 56401 61105 61541'
    self.assertEqual(StandardObservation(s).ice_conditions, [{'title': 'Ледостав, ровный ледяной покров'},
                                                             {'title': 'Ледостав неполный'},
                                                             {
                                                               'title': 'Ледяной покров с полыньями (промоинами, пропаринами)',
                                                               'intensity': 10}])

    self.assertEqual(StandardObservation(s).water_conditions, [{'title': 'Лесосплав', 'intensity': 50},
                                                             {'title': 'Залом леса ниже поста'},
                                                             {
                                                               'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}])
    self.assertEqual(StandardObservation(s).water_status, {'water_status_code': [16, 15, 36, 37, 38]})
    s = '51113 51903 51904 54854 66222 63545'
    self.assertEqual(StandardObservation(s).water_status, {'water_status_code': [1, 2, 4, 5, 13, 30, 31, 38]})

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

class TestReport(unittest.TestCase):
  def test_standard(self):
    s = '10950 31081 16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99993 09094'
    self.assertEqual(KN15(s).decode(), [
      {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
       'special_marks': None, 'stage': -1161, 'change_stage': -14,
       'previous_stage': 175, 'water_temperature': 9.9, 'air_temperature': None,
       'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, {'title': 'Ледостав неполный'},
                          {'title': 'Ледяной покров с полыньями (промоинами, пропаринами)', 'intensity': 10}],
       'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}, {'title': 'Залом леса ниже поста'},
                            {'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}],
       'ice_thickness': 51, 'snow_depth': 'менее 5 см', 'discharge': 0.001,
       'precipitation_duration_by_half_day': 'от 6 до 12 ч', 'precipitation_amount_by_half_day': 0.9,
       'precipitation_duration': 'более 12 ч', 'precipitation_amount': 909.0, 
       'water_status_code': [16, 15, 36, 37, 38], 'cross-sectional_area': None,
       'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
       'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
       'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
       'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
       'reservoir_min_downstream_stage': None,
       'reservoir_volume': None, 'reservoir_previous_volume': None, 'reservoir_total_inflow': None,
       'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
       'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
       'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
       'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
       'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None}])

    '''below was a telegram that checked the "correct" pars of the group 9RRRd = 92203 with n = 1, 
    but it does not work now '''

    s = '10950 31081 11161 20141 35175 46405 51112 60000 70999 89999 90203 03304'
    self.assertEqual(KN15(s).decode(), [
      {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None, 'stage': 1161,
       'change_stage': 14, 'previous_stage': -175, 'water_temperature': 6.4, 'air_temperature': 5,
       'ice_conditions': [{'title': 'Сало'}, {'title': 'Снежура'}], 'water_conditions': [{'title': 'Чисто'}],
       'ice_thickness': 99, 'snow_depth': 'больше 70 см', 'discharge': 999000000.0,
       'precipitation_duration_by_half_day': 'от 6 до 12 ч', 'precipitation_amount_by_half_day': 20.0,
       'precipitation_duration': 'более 12 ч', 'precipitation_amount': 330.0, 
       'water_status_code': [1, 7, 29], 'cross-sectional_area': None,
       'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
       'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
       'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
       'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
       'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
       'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
       'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
       'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
       'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
       'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
       'measure_day': None, 'measure_synophour': None, 'disaster_type': None}])

    s = '10950 31082\
 92230 10101 20142 30175 42099 56563 61105 70511 80001 99893 09090\
 92229 10101 20142 30175 42099 56563 61105 70511 80001 99893 09090\
 92228 15140 20142 30175 42099 56563 61105 70511 80001 99893 09090\
 92227 15140 20142 30175 42099 56563 61105 70511 80001 99893 09090\
 93330 10140 20142 30175 42099 52163 62105 71211\
 94431 11200 21300 31250 41345 51234 61345 73500 83600\
 94430 11200 21300 31250 41345 51234 61345 73500 83600\
 94429 11200 21300 31250 41345 51234 61345 73500 83600\
 95531 11200 21300 31250 41345 51234 61345 73500\
 95530 11200 21300 31250 41345 51234 61345 73500\
 95529 11200 21300 31250 41345 51234 61345 73500\
 96603 11200 21300 31250 41345 53008 60000 70001 82908'

    self.assertEqual(KN15(s).decode(), [
        {'identifier': 10950, 'basin': 10, 'day_of_month': 30, 'synophour': 8, 'special_marks': None,
         'stage': 101, 'change_stage': -14,
         'previous_stage': 175, 'water_temperature': 20, 'air_temperature': None,
         'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, {'title': 'Ледостав неполный'}],
         'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}], 'ice_thickness': 51, 'snow_depth': 'менее 5 см',
         'discharge': 0.001, 'precipitation_duration_by_half_day': 'от 6 до 12 ч',
         'precipitation_amount_by_half_day': 989.0, 'precipitation_duration': 'менее 1 ч',
         'precipitation_amount': 909.0, 'water_status_code': [16, 15, 36], 'cross-sectional_area': None, 
         'max_water_depth': None, 'period': None,
         'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None,
         'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None,
         'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
         'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
         'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
         'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
         'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
         'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
         'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
         'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None
         },
        {'identifier': 10950, 'basin': 10, 'day_of_month': 29, 'synophour': 8, 'special_marks': None,
         'stage': 101, 'change_stage': -14,
         'previous_stage': 175, 'water_temperature': 20, 'air_temperature': None,
         'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, {'title': 'Ледостав неполный'}],
         'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}], 'ice_thickness': 51, 'snow_depth': 'менее 5 см',
         'discharge': 0.001, 'precipitation_duration_by_half_day': 'от 6 до 12 ч',
         'precipitation_amount_by_half_day': 989.0, 'precipitation_duration': 'менее 1 ч',
         'precipitation_amount': 909.0, 'water_status_code': [16, 15, 36], 'cross-sectional_area': None, 
         'max_water_depth': None, 'period': None,
         'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None,
         'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None,
         'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
         'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
         'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
         'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
         'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
         'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
         'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
         'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None
         },
        {'identifier': 10950, 'basin': 10, 'day_of_month': 28, 'synophour': 8,
         'special_marks': None, 'stage': -140, 'change_stage': -14,
         'previous_stage': 175, 'water_temperature': 20, 'air_temperature': None,
         'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, {'title': 'Ледостав неполный'}],
         'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}], 'ice_thickness': 51, 'snow_depth': 'менее 5 см',
         'discharge': 0.001, 'precipitation_duration_by_half_day': 'от 6 до 12 ч',
         'precipitation_amount_by_half_day': 989.0, 'precipitation_duration': 'менее 1 ч',
         'precipitation_amount': 909.0, 'water_status_code': [16, 15, 36], 'cross-sectional_area': None, 
         'max_water_depth': None, 'period': None,
         'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None,
         'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None,
         'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
         'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
         'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
         'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
         'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
         'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
         'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
         'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 27, 'synophour': 8,
         'special_marks': None, 'stage': -140, 'change_stage': -14,
         'previous_stage': 175, 'water_temperature': 20, 'air_temperature': None,
         'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, {'title': 'Ледостав неполный'}],
         'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}], 'ice_thickness': 51, 'snow_depth': 'менее 5 см',
         'discharge': 0.001, 'precipitation_duration_by_half_day': 'от 6 до 12 ч',
         'precipitation_amount_by_half_day': 989.0, 'precipitation_duration': 'менее 1 ч',
         'precipitation_amount': 909.0, 'water_status_code': [16, 15, 36], 'cross-sectional_area': None, 
         'max_water_depth': None, 'period': None,
         'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None,
         'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None,
         'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
         'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
         'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
         'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
         'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
         'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
         'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
         'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': 'за месяц', 'avg_stage': 140, 'max_stage': 142, 'min_stage': 175,
         'avg_discharge': 9.9, 'max_discharge': 16.3, 'min_discharge': 10.5, 'day_of_max': 12, 'hour_of_max': 11,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': 1200, 'reservoir_avg_stage': 1300, 'reservoir_previous_avg_stage': 1250,
         'reservoir_downstream_stage': 1345, 'reservoir_max_downstream_stage': 1234,
         'reservoir_min_downstream_stage': 1345, 'reservoir_volume': 500.0, 'reservoir_previous_volume': 600.0,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 30, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': 1200, 'reservoir_avg_stage': 1300, 'reservoir_previous_avg_stage': 1250,
         'reservoir_downstream_stage': 1345, 'reservoir_max_downstream_stage': 1234,
         'reservoir_min_downstream_stage': 1345, 'reservoir_volume': 500.0, 'reservoir_previous_volume': 600.0,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 29, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': 1200, 'reservoir_avg_stage': 1300, 'reservoir_previous_avg_stage': 1250,
         'reservoir_downstream_stage': 1345, 'reservoir_max_downstream_stage': 1234,
         'reservoir_min_downstream_stage': 1345, 'reservoir_volume': 500.0, 'reservoir_previous_volume': 600.0,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': 2.0, 'reservoir_side_inflow': 3.0, 'reservoir_water_area_inflow': 2.5,
         'reservoir_sum_previous_total_inflow': 3.45, 'reservoir_sum_previous_side_inflow': 2.34,
         'reservoir_sum_previous_water_area_inflow': 3.45, 'reservoir_water_discharge': 500.0,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 30, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': 2.0, 'reservoir_side_inflow': 3.0, 'reservoir_water_area_inflow': 2.5,
         'reservoir_sum_previous_total_inflow': 3.45, 'reservoir_sum_previous_side_inflow': 2.34,
         'reservoir_sum_previous_water_area_inflow': 3.45, 'reservoir_water_discharge': 500.0,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 29, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': 2.0, 'reservoir_side_inflow': 3.0, 'reservoir_water_area_inflow': 2.5,
         'reservoir_sum_previous_total_inflow': 3.45, 'reservoir_sum_previous_side_inflow': 2.34,
         'reservoir_sum_previous_water_area_inflow': 3.45, 'reservoir_water_discharge': 500.0,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
         'measure_day': None, 'measure_synophour': None, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None,
         'stage': 1200, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': 3.0,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': 2.5,
         'max_water_depth': 1345, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
         'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': 3, 'measure_day': 30,
         'measure_synophour': 8, 'disaster_type': None},
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': None,
         'stage': None, 'change_stage': None,
         'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
         'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
         'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
         'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
         'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
         'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None,
         'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
         'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
         'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
         'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
         'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
         'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
         'reservoir_wind_direction': 'ветра нет, штиль', 'reservoir_wind_speed': 0,
         'reservoir_wave_direction': 'волнения нет', 'reservoir_wave_depth': 0, 'reservoir_water_surface_condition': 0,
         'measure_month': 3, 'measure_day': 29, 'measure_synophour': 8, 'disaster_type': None}]
          )

    s = '10950 31082 97701 11000 22002 51606 61105 РАЗМЫТА НАСЫПЬ ПОДЪЕМ ПРОДОЛЖАЕТСЯ 97702 15200 22001 66064 ЗАСУХА 97703 10600 56565 ОПАСНОСТЬ ДЛЯ СУДОВ 97704 89100 ПРОРЫВ ПЛОТИНЫ 97705 02004 СИЛЬНЫЙ ДОЖДЬ 97706 ПРОШЕЛ СЕЛЬ 97707 ОЖИДАЕТСЯ СХОД ЛАВИН'

    self.assertEqual(KN15(s).decode(), [
        {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
        'special_marks': 'РАЗМЫТА НАСЫПЬ ПОДЪЕМ ПРОДОЛЖАЕТСЯ', 'stage': 1000, 'change_stage': -200,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': [
              {'title': 'Ледоход; для озер, водохранилищ - дрейф льда; снегоход - для пересыхающих рек',
               'intensity': 60}],
        'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}], 'ice_thickness': None, 'snow_depth': None,
        'discharge': None, 'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
        'precipitation_duration': None, 'precipitation_amount': None, 
         'water_status_code': [9, 36], 'cross-sectional_area': None,
        'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
        'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None,
        'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
        'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
        'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
        'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
        'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
        'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
        'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
        'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
        'measure_day': None, 'measure_synophour': None, 'disaster_type': 'высокие уровни воды'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
        'special_marks': 'ЗАСУХА', 'stage': -200, 'change_stage': 200,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
        'water_conditions': [{'title': 'Река пересохла'},
                             {'title': 'Стоячая вода (перемерз или пересох расположенный выше или ниже перекат)'}],
        'ice_thickness': None, 'snow_depth': None, 'discharge': None, 'precipitation_duration_by_half_day': None,
        'precipitation_amount_by_half_day': None, 'precipitation_duration': None, 'precipitation_amount': None,
        'water_status_code': [39, 33], 'cross-sectional_area': None, 'max_water_depth': None, 
        'period': None, 'avg_stage': None, 'max_stage': None,
        'min_stage': None, 'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None, 'reservoir_upstream_stage': None, 'reservoir_avg_stage': None,
        'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
        'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
        'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
        'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
        'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
        'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
        'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
        'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': 'низкие уровни воды'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': 'ОПАСНОСТЬ ДЛЯ СУДОВ',
        'stage': 600, 'change_stage': None,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None,
        'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}], 'water_conditions': None,
        'ice_thickness': None, 'snow_depth': None, 'discharge': None, 'precipitation_duration_by_half_day': None,
        'precipitation_amount_by_half_day': None, 'precipitation_duration': None, 'precipitation_amount': None,
        'water_status_code': [16], 'cross-sectional_area': None, 'max_water_depth': None, 
        'period': None, 'avg_stage': None, 'max_stage': None,
        'min_stage': None, 'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None, 'reservoir_upstream_stage': None, 'reservoir_avg_stage': None,
        'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None,
        'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None,
        'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None,
        'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None,
        'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None,
        'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None,
        'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None,
        'measure_month': None, 'measure_day': None, 'measure_synophour': None,
        'disaster_type': 'раннее образование ледостава и появление льда'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
        'special_marks': 'ПРОРЫВ ПЛОТИНЫ', 'stage': None, 'change_stage': None,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
        'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': 100000000.0,
        'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
        'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
        'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
        'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None,
        'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
        'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
        'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
        'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
        'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
        'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
        'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
        'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
        'measure_day': None, 'measure_synophour': None,
        'disaster_type': 'очень большие или очень малые расходы воды, приток, сброс'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
        'special_marks': 'СИЛЬНЫЙ ДОЖДЬ', 'stage': None, 'change_stage': None,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
        'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
        'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
        'precipitation_duration': 'более 12 ч', 'precipitation_amount': 200.0, 'water_status_code': None, 'cross-sectional_area': None,
        'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
        'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None,
        'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
        'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
        'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
        'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
        'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
        'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
        'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
        'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
        'measure_day': None, 'measure_synophour': None, 'disaster_type': 'сильный дождь'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8, 'special_marks': 'ПРОШЕЛ СЕЛЬ',
        'stage': None, 'change_stage': None,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
        'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
        'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
        'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
        'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
        'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None,
        'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
        'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
        'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
        'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
        'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
        'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
        'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
        'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
        'measure_day': None, 'measure_synophour': None, 'disaster_type': 'сели'},
       {'identifier': 10950, 'basin': 10, 'day_of_month': 31, 'synophour': 8,
        'special_marks': 'ОЖИДАЕТСЯ СХОД ЛАВИН', 'stage': None, 'change_stage': None,
        'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None,
        'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None,
        'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None,
        'precipitation_duration': None, 'precipitation_amount': None, 'water_status_code': None, 'cross-sectional_area': None,
        'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None,
        'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None,
        'hour_of_max': None,
        'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None,
        'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None,
        'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None,
        'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None,
        'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None,
        'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None,
        'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None,
        'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None,
        'measure_day': None, 'measure_synophour': None, 'disaster_type': 'лавины'}]
          )



if __name__ == '__main__':
  unittest.main()
