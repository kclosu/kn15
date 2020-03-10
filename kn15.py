import re

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
print(report_pattern)


# weatherreports = 

# groupidentifiers = (re.compile(''))
# additionalgroupidentifiers = ()

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
    self.properties = [
      'basin', 'station_id',
      'YY', 'GG', 'n',
      'stage',
      'change_stage', 'change_stage_sign',
      'prev_stage',
      'water_temp', 'air_temp',
      'ice',
      'water_condition',
      'ice_thickness', 'snow_depth',
      'integer_part', 'discharge',
      'precip_amount', 'precip_duration'
    ]
    self._parse()

  def _parse(self):
    match = re.match(report_pattern, self._report)
    self._basin = match.group('basin')
    self._station_id = match.group('station_id')
    self._YY = match.group('YY')
    self._GG = match.group('GG')
    self._n = match.group('n')
    self._stage = match.group('stage')
    self._change_stage = match.group('change_stage')
    self._change_stage_sign = match.group('change_stage_sign')
    self._prev_stage = match.group('prev_stage')
    self._water_temp = match.group('water_temp')
    self._air_temp = match.group('air_temp')
    self._ice = match.group('ice')
    self._water_condition = match.group('water_condition')
    self._ice_thickness = match.group('ice_thickness')
    self._snow_depth = match.group('snow_depth')
    self._integer_part = match.group('integer_part')
    self._discharge = match.group('discharge')
    self._precip_amount = match.group('precip_amount')
    self._precip_duration = match.group('precip_duration')
    parsed = {}
    for group in self.properties:
      parsed[group] = match.group(group)
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
    return self._YY

  @property
  def stage(self):
    return self._stage

  @property
  def discharge(self):
    return self._discharge

  @property
  def ice_thickness(self):
    return self._ice_thickness

  @property
  def snow_depth(self):
    return self._snow_depth

  @property
  def air_temperature(self):
    return self._air_temp

  @property
  def water_temperature(self):
    return self._water_temp

  @property
  def precipation_duration(self):
    return self._precip_duration

  @property
  def precipation_amount(self):
    return self._precip_amount

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
      'basin': self.basin
    }


def bulletin_reports(bulletin):
  """
    each report in bulletin start with new line and ended with '='
    return iterator for reports in bulletin  
  """
  return map(lambda m: re.sub(r"\s+", ' ', m.group(1)).strip(), re.finditer(report_bounds, bulletin))


def decode(bulletin):
  if bulletin.split()[0].upper() != 'HHZZ':
    raise TypeError("")
  return bulletin_reports(bulletin[4:])


if __name__ == "__main__":
  text = open('samples/20191010_SRUR44 UKMS 100500.hydra', 'r').read()
  for report in decode(text):
    print(report)
    print(KN15(report).decode())
    
