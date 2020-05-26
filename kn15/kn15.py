import re
import click

report_bounds = re.compile(r'^(.*?)=', re.DOTALL | re.MULTILINE)

identifier = r'(?P<basin>\d{2})(?P<station_id>\d{3})'
measure_time = r'(?P<YY>\d{2})(?P<GG>\d{2})(?P<n>[1-5,7])'
stage = r'1(?P<stage>\d{4}|/{4})'
change_stage = r'2(?P<change_stage>\d{3}|/{3})(?P<change_stage_sign>\d|/)'
previous_stage = r'3(?P<prev_stage>\d{4}|/{4})'
temperature = r'4(?P<water_temp>\d{2})(?P<air_temp>\d{2}|/{2})'
ice = r'5(?P<ice>\d{4})'
water_condition = r'6(?P<water_condition>\d{4})'
ice_thickness = r'7(?P<ice_thickness>\d{3})(?P<snow_depth>\d)'
discharge = r'8(?P<discharge_integer_part>\d)(?P<discharge>\d{3})'
precipitation = r'0(?P<precip_amount>\d{3}|/{2})(?P<precip_duration>\d|/{2})'

standart_observation = f'(\s{stage})?(\s{change_stage})?(\s{previous_stage})?(\s{temperature})?(\s{ice})*(\s{water_condition})?(\s{ice_thickness})?(\s{discharge})?(\s{precipitation})?'

report_pattern = f'^{measure_time}{standart_observation}'

# print(report_pattern)

additional_sections_tags = r'9[22|33|44|55|66|77|88]\d{2}'

previous_days = r'922(\d{2})'
flow = r'933(\d{2})(\s.*)'
pool_stage = r'944(\d{2})(\s.*)'
pool_flow = r'955(\d{2})(\s.*)'
flow_detail = r'966(\d{2})(\s.*)'
disasters = r'97701(\s.*)97702(\s.*)97703(\s.*)97704(\s.*)97705(\s.*)97706(\s.*)97707(\s.*)'

NullValue = 'NIL'


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
  @staticmethod
  def parse():
    pass

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
    self._discharge_integer_part = None
    self._discharge = None
    self._precip_amount = None
    self._precip_duration = None
    self._parse()

  def _parse(self):
    identifier = self._report[:5]
    self._basin = identifier[:2]
    self._station_id = identifier[2:]
    parts = re.split(fr'\s(?={additional_sections_tags})', self._report[6:])
    if not re.match(additional_sections_tags, parts[0]):
      match = re.match(report_pattern, parts[0])
      if match is None:
        raise KN15Error("Couldn't parse report string with regular expression")
      parsed = match.groupdict()
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
      self._discharge_integer_part = parsed.get('discharge_integer_part')
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
    if self._GG and not 0 <= int(self._GG) <= 23: raise KN15Error(f'Time of measure {self._GG} is not between 00 and 23')
    return self._GG
  
  @property
  def ice_conditions(self):
    if not self._ice:
      return None
    conditions = [{
      'title': ice_conditions[int(self._ice[:2])-11],
      'intensity': None
    }]
    second2digits = int(self._ice[2:])
    if second2digits < 11:
      conditions[0]['intensity'] = second2digits * 10
    else:
      conditions.append({
        'title': ice_conditions[second2digits-11],
        'intensity': None
      })
    return conditions

  @property
  def measure_day(self):
    """
    measure day of month
    """
    if self._YY and not 1 <= int(self._YY) <= 31: raise KN15Error(f'Day of month {self._YY} is not between 1 and 31')
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
      return float(self._discharge) * pow(10, int(self._discharge_integer_part) - 3)
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
    if self._air_temp is not None and self._air_temp != '//':
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
      # try:
        # print(KN15(report).decode())
      # except Exception as ex:
        # print(ex)


if __name__ == "__main__":
  # parse()
  # s = '10950 31082 10161 20042 30163 56565 70530 //053 94431 20165 45046 95531 43695 74109 94430 20168 45046 95530 43655 74109 94429 20172 45036 95529 43607 74105 94428 20177 45043 95528 43565 73995'
  s = '11085 94411 10503 20508 40193 73145 95511 24115 44265 74254'
  report = KN15(s)
  # # print(report._parse())
  print(report.decode())

    
ice_conditions = [
  'Сало',
  'Снежура',
  'Забереги (первичные; наносные); припай шириной менее 100 м - для озер,водохранилищ',
  'Припай шириной более 100 м - для озер, водохранилищ',
  'Забереги нависшие',
  '*Ледоход; для озер, водохранилищ - дрейф льда; снегоход - для пересыхающих рек',
  '*Ледоход, лед из притока, озера, водохранилища',
  '*Ледоход поверх ледяного покрова',
  '*Шугоход',
  'Внутриводный лед (донный; глубинный)',
  'Пятры',
  'Осевший лед (на береговой отмели после понижения уровня)',
  'Навалы льда на берегах (ледяные валы)',
  'Ледяная перемычка в створе поста',
  'Ледяная перемычка выше поста',
  'Ледяная перемычка ниже поста',
  'Затор льда выше поста',
  'Затор льда ниже поста',
  'Затор льда искусственно разрушается',
  'Зажор льда выше поста',
  'Зажор льда ниже поста',
  'Зажор льда искусственно разрушается',
  'Вода на льду',
  'Вода течет поверх льда (после промерзания реки; при наличии воды подо льдом)',
  '*Закраины',
  'Лед потемнел',
  'Снежница',
  'Лед подняло (вспучило)',
  'Подвижка льда',
  'Разводья',
  'Лед тает на месте',
  '*Забереги остаточные',
  'Наслуд',
  '*Битый лед - для озер, водохранилищ, устьевых участков рек',
  '*Блинчатый лед - для озер, водохранилищ, устьевых участков рек',
  '*Ледяные поля - для озер, водохранилищ, устьевых участков рек',
  '*Ледяная каша - для озер, водохранилищ, устьевых участков рек',
  'Стамуха',
  'Лед относит (отнесло) от берега - для озер, водохранилищ',
  'Лед прижимает (прижало) к берегу - для озер, водохранилищ',
  '*Ледостав неполный',
  '*Ледяной покров с полыньями (промоинами, пропаринами)',
  'Ледостав, ровный ледяной покров',
  'Ледостав, ледяной покров с торосами',
  'Ледяной покров с грядами торосов - для водохранилищ',
  'Шуговая дорожка',
  'Подо льдом шуга',
  'Трещины в ледяном покрове',
  'Наледь',
  'Лед нависший(ледяной мост)',
  'Лед ярусный (ледяной покров состоит из отдельных слоев,между которыми находится вода или воздушная п',
  'Лед на дне (осевший или вследствие предшествующего промерзания реки)',
  'Река (озеро) промерзла',
  'Лед искусственно разрушен (ледоколом, взрыванием и др.техническими средствами',
  'Наледная вода',
  'Чисто',
  '*Лесосплав',
  'Залом леса выше поста',
  'Залом леса ниже поста',
  '*Растительность у берега',
  '*Растительность по всему сечению потока',
  '*Растительность по сечению потока пятнами',
  'Растительность стелется по дну',
  'Растительность на гидростворе выкошена',
  'Растительность легла на дно (осенью)',
  'Растительность занесена илом (во время спуска рыбных прудов и т.д.).',
  'Растительность погибла в результате загрязнения реки',
  'Обвал (оползень) берега в створе поста',
  'Обвал (оползень) берега выше поста',
  'Обвал (оползень) берега ниже поста',
  'Дноуглубительные работы в русле',
  'Намывные работы в русле',
  'Проведена расчистка русла',
  'Русло реки сужено на гидростворе для измерения расхода воды',
  'Образовалась коса',
  'Коса',
  'Образовался осередок',
  'Осередок',
  'Образовался остров',
  'Остров',
  'Смещение русла в плане',
  'Снежный завал в створе поста',
  'Снежный завал выше поста',
  'Снежный завал ниже поста',
  'Прорыв снежного завала',
  'Прохождение селя',
  'Течение реки изменилось на противоположное',
  'Сгон воды - для устьевых участков рек, озер, водохранилищ',
  'Нагон воды - для устьевых участков рек, озер, водохранилищ',
  'Река пересохла',
  'Волнение слабое, 1 балл - для больших рек, озер, водохранилищ',
  'Волнение умеренное, 2-3 балла - для больших рек, озер, водохранилищ',
  'Волнение сильное, более 4 баллов - для больших рек, озер, водохранилищ',
  'Стоячая вода (перемерз или пересох расположенный выше или ниже перекат)',
  'Стоячая вода подо льдом',
  'Прекратилась лодочная переправа',
  'Прекратилось пешее сообщение',
  'Началось пешее сообщение',
  'Началось движение транспорта по льду',
  'Прекратилось движение транспорта по льду',
  'Началась лодочная переправа',
  'Подпор от озера, реки',
  'Начало навигации',
  'Конец навигации',
  'Забор воды выше поста',
  'Забор воды ниже поста',
  'Забор воды выше поста прекратился',
  'Забор воды ниже поста прекратился',
  'Сброс воды выше поста',
  'Сброс воды ниже поста',
  'Сброс воды выше поста прекратился',
  'Сброс воды ниже поста прекратился',
  'Плотина (перемычка, запруда, дамба) выше поста',
  'Плотина (перемычка, запруда, дамба) ниже поста',
  'Разрушена плотина (перемычка, запруда, дамба) выше поста',
  'Разрушена плотина (перемычка, запруда, дамба) ниже поста',
  'Подпор от засорения русла',
  'Подпор от мостовых переправ',
  'Пропуски воды из озера, водохранилищ'
]
