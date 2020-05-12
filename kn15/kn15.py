import re
import click

report_bounds = re.compile(r'^(.*?)=', re.DOTALL | re.MULTILINE)

identifier = '(?P<basin>\d{2})(?P<station_id>\d{3})'
measure_time = '(?P<YY>\d{2})(?P<GG>\d{2})(?P<n>\d)'
stage = '1(?P<stage>\d{4})'
change_stage = '2(?P<change_stage>\d{3}(?P<change_stage_sign>\d))'
previous_stage = '3(?P<prev_stage>\d{4})'
temperature = '4(?P<water_temp>\d{2})(?P<air_temp>\d{2})'
ice = '5(?P<ice>\d{4})'
water_condition = '6(?P<water_condition>\d{4})'
ice_thickness = '7(?P<ice_thickness>\d{3})(?P<snow_depth>\d)'
discharge = '8(?P<integer_part>\d)(?P<discharge>\d{3})'
precipitation = '0(?P<precip_amount>\d{3})(?P<precip_duration>\d)'

NullValue = 'NIL'
report_pattern = f'^({identifier})\s({measure_time})(\s{stage})?(\s{change_stage})?(\s{previous_stage})?(\s{temperature})?(\s{ice})?(\s{water_condition})?(\s{ice_thickness})?(\s{discharge})?(\s{precipitation})?.*'

previous_days = '922(\d{2})(\s{stage})?(\s{change_stage})?(\s{previous_stage})?(\s{temperature})?(\s{ice})?(\s{water_condition})?(\s{ice_thickness})?(\s{discharge})?(\s{precipitation})?'
flow = '933(\d{2})(\s.*)'
pool_stage = '944(\d{2})(\s.*)'
pool_flow = '955(\d{2})(\s.*)'
flow_detail = '966(\d{2})(\s.*)'
disasters = '97701(\s.*)97702(\s.*)97703(\s.*)97704(\s.*)97705(\s.*)97706(\s.*)97707(\s.*)'


snow_depth_scale = [
  "На льду снега нет.",
  "менее 5 см.",
  "5-10 см.",
  "11-15 см.",
  "16-20 см.",
  "21-25 см.",
  "26-35 см.",
  "36-50 см.",
  "51-70 см.",
  "больше 70 см."
]

precipitation_duration_scale = [
  "менее 1 ч.",
  "от 1 до 3 ч.",
  "от 3 до 6 ч.",
  "от 6 до 12 ч.",
  "более 12 ч."
]

class KN15Error(Exception):
    """Class for exceptions raised when parsing report string"""
    pass

class KN15():
  def __init__(self, report):
    super().__init__()
    self._report = report
    self._basin = None
    self._station_id = None
    self._YY = None
    self._GG = None
    self._n = None
    self._stage = None
    self._change_stage = None
    self._change_stage_sign = None
    self._prev_stage = None
    self._water_temp = None
    self._air_temp = None
    self._ice = None
    self._water_condition = None
    self._ice_thickness = None
    self._snow_depth = None
    self._integer_part = None
    self._discharge = None
    self._precip_amount = None
    self._precip_duration = None
    self._parse()

  def _parse(self):
    match = re.match(report_pattern, self._report)
    if match is None:
      raise KN15Error("Couldn't parse report string with regular expression")
    parsed = match.groupdict()
    self._basin = parsed.get('basin')
    self._station_id = parsed.get('station_id')
    self._YY = parsed.get('YY')
    self._GG = parsed.get('GG')
    self._n = parsed.get('n')
    self._stage = parsed.get('stage')
    self._change_stage = parsed.get('change_stage')
    self._change_stage_sign = parsed.get('change_stage_sign')
    self._prev_stage = parsed.get('prev_stage')
    self._water_temp = parsed.get('water_temp')
    self._air_temp = parsed.get('air_temp')
    self._ice = parsed.get('ice')
    self._water_condition = parsed.get('water_condition')
    self._ice_thickness = parsed.get('ice_thickness')
    self._snow_depth = parsed.get('snow_depth')
    self._integer_part = parsed.get('integer_part')
    self._discharge = parsed.get('discharge')
    self._precip_amount = parsed.get('precip_amount')
    self._precip_duration = parsed.get('precip_duration')

    return parsed

  @property
  def identifier(self):
    return f'{self._basin}{self._station_id}'

  @property
  def basin(self):
    return self._basin

  @property
  def measure_time(self):
    return self._GG
  
  @property
  def measure_day(self):
    """
    measure day of month
    """
    assert 1 <= int(self._YY) <= 31, f'Day of month ${self._YY} is not between 1 and 31'
    return self._YY

  @property
  def stage(self):
    if self._stage is not None:
      stage = int(self._stage)
      return stage if stage < 5000 else (5000 - stage)
    else:
      return None

  @property
  def discharge(self):
    if self._discharge is not None:
      return int(self._discharge) * pow(10, int(self._integer_part) - 3)
    else:
      return None

  @property
  def ice_thickness(self):
    if self._ice_thickness:
      return int(self._ice_thickness)
    else:
      return None

  @property
  def snow_depth(self):
    if self._snow_depth is not None:
      return snow_depth_scale[int(self._snow_depth)]
    else:
      return None

  @property
  def water_temperature(self):
    if self._water_temp is not None:
      return int(self._water_temp) / 10
    else:
      return None

  @property
  def air_temperature(self):
    if self._air_temp is not None:
      air_temp = int(self._air_temp)
      return air_temp if air_temp < 50 else (50 - air_temp)
    else:
      return None

  @property
  def precipation_duration(self):
    if self._precip_duration is not None:
      return precipitation_duration_scale[int(self._precip_duration)]
    else:
      return None

  @property
  def precipation_amount(self):
    if self._precip_amount is not None:
      precip_amount = float(self._precip_amount)
      return precip_amount if precip_amount < 990 else (precip_amount - 990)/10
    else:
      return None

  def decode(self):
    return {
      'stage': self.stage,
      'discharge': self.discharge,
      'ice_thickness': self.ice_thickness,
      'snow_depth': self.snow_depth,
      'precipation_duration': self.precipation_duration,
      'precipation_amount': self.precipation_amount,
      'air_temperature': self.air_temperature,
      'water_temperature': self.water_temperature,
      'identifier': self.identifier,
      'basin': self.basin,
      'day_of_month': self.measure_day,
      'synophour': self.measure_time 
    }


def bulletin_reports(bulletin):
  """
    each report in bulletin start with new line and ended with '='
    return iterator for reports in bulletin  
  """
  return map(lambda m: re.sub(r"\s+", ' ', m.group(1)).strip(), re.finditer(report_bounds, bulletin))


def decode(bulletin):
  if bulletin.split()[0].upper() != 'HHZZ':
    raise TypeError("Report does not contain HHZZ in first line")
  return bulletin_reports(bulletin[4:])


@click.command()
@click.option('--filename', prompt='Bulletin file', help='path to file')
def parse(filename):
  with open(filename, 'r') as f:
    bulletin = f.read()
    for report in decode(bulletin):
      print(report)
      try:
        print(KN15(report).decode())
      except Exception as ex:
        print(ex)


if __name__ == "__main__":
  # parse()
  s = '10950 31082 10161 20042 30163 56565 70530 //053 94431 20165 45046 95531 43695 74109 94430 20168 45046 95530 43655 74109 94429 20172 45036 95529 43607 74105 94428 20177 45043 95528 43565 73995'
  report = KN15(s)
  print(report._parse())
  print(report.decode())

    
