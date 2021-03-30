import re

STAGE = r'1(?P<stage>\d{4}|/{4})'
CHANGE_STAGE = r'2(?P<change_stage>\d{3}|/{3})(?P<change_stage_sign>\d|/)'
PREVIOUS_STAGE = r'3(?P<prev_stage>\d{4}|/{4})'
TEMPERATURE = r'4(?P<water_temp>\d{2})(?P<air_temp>\d{2}|/{2})'
ICE = r'5(?P<ice>\d{4})'
WATER = r'6(?P<water_condition>\d{4})'
ICE_THICKNESS = r'7(?P<ice_thickness>\d{3})(?P<snow_depth>\d)'
DISCHARGE = r'8(?P<discharge_integer_part>\d)(?P<discharge>\d{3})'
PRECIPITATION_HALF_DAY = r'9(?P<precip_amount_half>\d{3}|/{3})(?P<precip_duration_half>\d|/)'
PRECIPITATION_DAY = r'0(?P<precip_amount>\d{3}|/{3})(?P<precip_duration>\d|/)'

STANDARD_OBSERVATION = f'^({STAGE})?(\s{CHANGE_STAGE})?(\s{PREVIOUS_STAGE})?(\s{TEMPERATURE})?(\s{ICE})*\
(\s{WATER})*(\s{ICE_THICKNESS})?(\s{DISCHARGE})?(\s{PRECIPITATION_HALF_DAY})?(\s{PRECIPITATION_DAY})?'

SNOW_DEPTH_SCALE = [
    "На льду снега нет",
    "менее 5 см",
    "5-10 см",
    "11-15 см",
    "16-20 см",
    "21-25 см",
    "26-35 см",
    "36-50 см",
    "51-70 см",
    "больше 70 см"
]

PRECIPITATION_DURATION_SCALE = [
    "менее 1 ч",
    "от 1 до 3 ч",
    "от 3 до 6 ч",
    "от 6 до 12 ч",
    "более 12 ч"
]

ICE_CONDITIONS = {
    11: 'Сало',
    12: 'Снежура',
    13: 'Забереги (первичные; наносные); припай шириной менее 100 м - для озер,водохранилищ',
    14: 'Припай шириной более 100 м - для озер, водохранилищ',
    15: 'Забереги нависшие',
    16: 'Ледоход; для озер, водохранилищ - дрейф льда; снегоход - для пересыхающих рек',
    17: 'Ледоход, лед из притока, озера, водохранилища',
    18: 'Ледоход поверх ледяного покрова',
    19: 'Шугоход',
    20: 'Внутриводный лед (донный; глубинный)',
    21: 'Пятры',
    22: 'Осевший лед (на береговой отмели после понижения уровня)',
    23: 'Навалы льда на берегах (ледяные валы)',
    24: 'Ледяная перемычка в створе поста',
    25: 'Ледяная перемычка выше поста',
    26: 'Ледяная перемычка ниже поста',
    30: 'Затор льда выше поста',
    31: 'Затор льда ниже поста',
    32: 'Затор льда искусственно разрушается',
    34: 'Зажор льда выше поста',
    35: 'Зажор льда ниже поста',
    36: 'Зажор льда искусственно разрушается',
    37: 'Вода на льду',
    38: 'Вода течет поверх льда (после промерзания реки; при наличии воды подо льдом)',
    39: 'Закраины',
    40: 'Лед потемнел',
    41: 'Снежница',
    42: 'Лед подняло (вспучило)',
    43: 'Подвижка льда',
    44: 'Разводья',
    45: 'Лед тает на месте',
    46: 'Забереги остаточные',
    47: 'Наслуд',
    48: 'Битый лед - для озер, водохранилищ, устьевых участков рек',
    49: 'Блинчатый лед - для озер, водохранилищ, устьевых участков рек',
    50: 'Ледяные поля - для озер, водохранилищ, устьевых участков рек',
    51: 'Ледяная каша - для озер, водохранилищ, устьевых участков рек',
    52: 'Стамуха',
    53: 'Лед относит (отнесло) от берега - для озер, водохранилищ',
    54: 'Лед прижимает (прижало) к берегу - для озер, водохранилищ',
    63: 'Ледостав неполный',
    64: 'Ледяной покров с полыньями (промоинами, пропаринами)',
    65: 'Ледостав, ровный ледяной покров',
    66: 'Ледостав, ледяной покров с торосами',
    67: 'Ледяной покров с грядами торосов - для водохранилищ',
    68: 'Шуговая дорожка',
    69: 'Подо льдом шуга',
    70: 'Трещины в ледяном покрове',
    71: 'Наледь',
    72: 'Лед нависший(ледяной мост)',
    73: 'Лед ярусный (ледяной покров состоит из отдельных слоев,между которыми находится вода или воздушная п',
    74: 'Лед на дне (осевший или вследствие предшествующего промерзания реки)',
    75: 'Река (озеро) промерзла',
    76: 'Лед искусственно разрушен (ледоколом, взрыванием и др.техническими средствами',
    77: 'Наледная вода'
}
WATER_CONDITIONS ={
    0: 'Чисто',
    11: 'Лесосплав',
    14: 'Залом леса выше поста',
    15: 'Залом леса ниже поста',
    22: 'Растительность у берега',
    23: 'Растительность по всему сечению потока',
    24: 'Растительность по сечению потока пятнами',
    25: 'Растительность стелется по дну',
    26: 'Растительность на гидростворе выкошена',
    27: 'Растительность легла на дно (осенью)',
    28: 'Растительность занесена илом (во время спуска рыбных прудов и т.д.).',
    29: 'Растительность погибла в результате загрязнения реки',
    35: 'Обвал (оползень) берега в створе поста',
    36: 'Обвал (оползень) берега выше поста',
    37: 'Обвал (оползень) берега ниже поста',
    38: 'Дноуглубительные работы в русле',
    39: 'Намывные работы в русле',
    40: 'Проведена расчистка русла',
    41: 'Русло реки сужено на гидростворе для измерения расхода воды',
    42: 'Образовалась коса',
    43: 'Коса',
    44: 'Образовался осередок',
    45: 'Осередок',
    46: 'Образовался остров',
    47: 'Остров',
    48: 'Смещение русла в плане',
    52: 'Снежный завал в створе поста',
    53: 'Снежный завал выше поста',
    54: 'Снежный завал ниже поста',
    55: 'Прорыв снежного завала',
    56: 'Прохождение селя',
    57: 'Течение реки изменилось на противоположное',
    58: 'Сгон воды - для устьевых участков рек, озер, водохранилищ',
    59: 'Нагон воды - для устьевых участков рек, озер, водохранилищ',
    60: 'Река пересохла',
    61: 'Волнение слабое, 1 балл - для больших рек, озер, водохранилищ',
    62: 'Волнение умеренное, 2-3 балла - для больших рек, озер, водохранилищ',
    63: 'Волнение сильное, более 4 баллов - для больших рек, озер, водохранилищ',
    64: 'Стоячая вода (перемерз или пересох расположенный выше или ниже перекат)',
    65: 'Стоячая вода подо льдом',
    66: 'Прекратилась лодочная переправа',
    67: 'Прекратилось пешее сообщение',
    68: 'Началось пешее сообщение',
    69: 'Началось движение транспорта по льду',
    70: 'Прекратилось движение транспорта по льду',
    71: 'Началась лодочная переправа',
    72: 'Подпор от озера, реки',
    73: 'Начало навигации',
    74: 'Конец навигации',
    77: 'Забор воды выше поста',
    78: 'Забор воды ниже поста',
    79: 'Забор воды выше поста прекратился',
    80: 'Забор воды ниже поста прекратился',
    81: 'Сброс воды выше поста',
    82: 'Сброс воды ниже поста',
    83: 'Сброс воды выше поста прекратился',
    84: 'Сброс воды ниже поста прекратился',
    85: 'Плотина (перемычка, запруда, дамба) выше поста',
    86: 'Плотина (перемычка, запруда, дамба) ниже поста',
    87: 'Разрушена плотина (перемычка, запруда, дамба) выше поста',
    88: 'Разрушена плотина (перемычка, запруда, дамба) ниже поста',
    89: 'Подпор от засорения русла',
    90: 'Подпор от мостовых переправ',
    91: 'Пропуски воды из озера, водохранилищ'
}

class Error(Exception):
    """Class for exceptions raised when parsing report string"""
    pass

class StandardObservation():

    def __init__(self, report):
        self._report = report
        self._YY = None
        self._stage = None
        self._change_stage = None
        self._change_stage_sign = None
        self._prev_stage = None
        self._water_temp = None
        self._air_temp = None
        self._ice_conditions = []
        self._water_conditions = []
        self._ice_thickness = None
        self._snow_depth = None
        self._discharge_integer_part = None
        self._flow = None
        self._precip_amount_half = None
        self._precip_duration_half = None
        self._precip_amount = None
        self._precip_duration = None
        self._parse()

    def _parse(self):
        report = self._report
        if re.match(r'922(\d{2})(\s.*)', self._report):
           self._YY = self._report[3:5]
           report = self._report[6:]
        match = re.match(STANDARD_OBSERVATION, report)
        if match is None:
            raise KN15Error("Couldn't parse report string with regular expression")
        parsed = match.groupdict()
        self._stage = parsed.get('stage')
        self._change_stage = parsed.get('change_stage')
        self._change_stage_sign = parsed.get('change_stage_sign')
        self._prev_stage = parsed.get('prev_stage')
        self._water_temp = parsed.get('water_temp')
        self._air_temp = parsed.get('air_temp')
        self._ice_conditions = re.findall(ICE, report)
        self._water_conditions = re.findall(WATER, report)
        self._ice_thickness = parsed.get('ice_thickness')
        self._snow_depth = parsed.get('snow_depth')
        self._flow_integer_part = parsed.get('discharge_integer_part')
        self._flow = parsed.get('discharge')
        self._precip_amount_half = parsed.get('precip_amount_half')
        self._precip_duration_half = parsed.get('precip_duration_half')
        self._precip_amount = parsed.get('precip_amount')
        self._precip_duration = parsed.get('precip_duration')


    @staticmethod
    def is_not_empty(param):
        """Return True if the attribute is not empty"""
        if param is not None:
            param = str(param)
            if param.isdigit():
                return True
            if not param.isdigit() and param != len(param) * '/':
                raise Error(f'Impossible to parse content in block: {param}')

    @staticmethod
    def key_in_dict(key, dict):
        """Return True if key is in dictionary"""
        if key in dict.keys():
            return True
        else:
            raise Error(f'Dictionary does not contain match for element code {key}')

    @staticmethod
    def get_conditions(conditions, dict, verbose=False):
        """Parse conditions with conditions dictionary.
         Use 'verbose=True' to return conditions title."""
        out = []
        for condition in conditions:
            if StandardObservation.is_not_empty(condition):
                l_part = int(condition[:2])
                r_part = int(condition[2:])
                if StandardObservation.key_in_dict(l_part, dict):
                    if 0 < r_part < 11:
                        if verbose:
                            out.append({
                                'title': dict[l_part],
                                'intensity': r_part * 10
                            })
                        else:
                            out.append({
                                'code': l_part,
                                'intensity': r_part * 10
                            })
                    else:
                        if verbose:
                            out.append({'title': dict[l_part]})
                        else:
                            out.append({'code': l_part})
                        if l_part != r_part and StandardObservation.key_in_dict(r_part, dict):
                            if verbose:
                                out.append({'title': dict[r_part]})
                            else:
                                out.append({'code': r_part})
        return out

    @staticmethod
    def get_amount(precip_amount, verbose=False):
        if verbose:
            if precip_amount == '000':
                return 'осадков не было'
            if precip_amount == '989':
                return '989 и более'
            if precip_amount == '990':
                return '0,0 следы осадков'
            if int(precip_amount) > 991:
                return f'0,{precip_amount[2]}'
            else:
                return precip_amount
        else:
            precip_amount = float(precip_amount)
            return precip_amount if precip_amount < 990 else (precip_amount - 990) / 10

    @staticmethod
    def get_duration(duration, verbose=False):
        duration = int(duration)
        if 0<=duration<len(PRECIPITATION_DURATION_SCALE):
            if verbose:
                return PRECIPITATION_DURATION_SCALE[duration]
            else:
                return duration
        else:
            raise Error(f'Array does not contain match for element code {duration}')

    @staticmethod
    def get_stage(stage):
        """Use to return 'stage' from Group_1 and Group_3"""
        stage = int(stage)
        return stage if stage < 5000 else (5000 - stage)

    @property
    def stage(self):
        """Return 'stage' from Group_1"""
        if self.is_not_empty(self._stage):
            return self.get_stage(self._stage)
        else:
            return None

    @property
    def change_stage(self):
        if self.is_not_empty(self._change_stage_sign):
            sing = int(self._change_stage_sign)
            if sing == 0:
                return 0
            if self.is_not_empty(self._change_stage) and sing == 1:
                return int(self._change_stage)
            if self.is_not_empty(self._change_stage) and sing == 2:
                return int(self._change_stage) * -1
            else:
                raise Error(f'Incorrect format in block: 2{self._change_stage}{sing}')
        else:
            return None

    @property
    def previous_stage(self):
        """Return 'stage' from Group_3 """
        if self.is_not_empty(self._prev_stage):
            return self.get_stage(self._prev_stage)
        else:
            return None

    @property
    def water_temperature(self):
        """Work incorrect. Instruction does not explain different between 1 and 10 in code '10'"""
        if self._water_temp is not None:
            if self._air_temp is not None and self._air_temp == '99':
                return int(self._water_temp)
            else:
                return int(self._water_temp) / 10
        else:
            return None

    @property
    def air_temperature(self):
        if self._air_temp is not None and self._air_temp not in ('//', '99'):
            air_temp = int(self._air_temp)
            return air_temp if air_temp < 50 else (50 - air_temp)
        else:
            return None

    @property
    def ice_conditions(self, verbose=True):
        if len(self._ice_conditions) == 0:
            return None
        conditions = self.get_conditions(self._ice_conditions, ICE_CONDITIONS, verbose=verbose)
        return conditions if len(conditions) > 0 else None

    @property
    def water_conditions(self, verbose=True):
        if len(self._water_conditions) == 0:
            return None
        conditions = self.get_conditions(self._water_conditions, WATER_CONDITIONS, verbose=verbose)
        return conditions if len(conditions) > 0 else None

    @property
    def ice_thickness(self):
        if self.is_not_empty(self._ice_thickness):
            return int(self._ice_thickness)
        else:
            return None

    @property
    def snow_depth(self, verbose=True):
        """No check element in list"""
        if self.is_not_empty(self._snow_depth):
            if verbose:
                return SNOW_DEPTH_SCALE[int(self._snow_depth)]
            else:
                return int(self._snow_depth)
        else:
            return None

    @property
    def daily_flow(self):
        if self.is_not_empty(self._flow):
            return float(self._flow) * pow(10, int(self._flow_integer_part) - 3)
        else:
            return None

    @property
    def precipitation_duration_half(self, verbose=True):
        if self.is_not_empty(self._precip_duration_half):
            return self.get_duration(self._precip_duration_half, verbose=verbose)
        else:
            return None

    @property
    def precipitation_amount_half(self, verbose=False):
        if self.is_not_empty(self._precip_amount_half):
            return self.get_amount(self._precip_amount_half, verbose=verbose)
        else:
            return None

    @property
    def precipitation_duration(self, verbose=True):
        if self.is_not_empty(self._precip_duration):
            return self.get_duration(self._precip_duration, verbose=verbose)
        else:
            return None

    @property
    def precipitation_amount(self, verbose=False):
        if self.is_not_empty(self._precip_amount):
            return self.get_amount(self._precip_amount, verbose=verbose)
        else:
            return None

    def decode(self):
        output = {}
        if self.stage is not None:
            output['stage'] = self.stage
        if self.change_stage is not None:
            output['change_stage'] = self.change_stage
        if self.previous_stage is not None:
            output['previous_stage'] = self.previous_stage
        if self.water_temperature is not None:
            output['water_temperature'] = self.water_temperature
        if self.air_temperature is not None:
            output['air_temperature'] = self.air_temperature
        if self.ice_conditions is not None:
            output['ice_conditions'] = self.ice_conditions
        if self.water_conditions is not None:
            output['water_conditions'] = self.water_conditions
        if self.ice_thickness is not None:
            output['ice_thickness'] = self.ice_thickness
        if self.snow_depth is not None:
            output['snow_depth'] = self.snow_depth
        if self.daily_flow is not None:
            output['discharge'] = self.daily_flow
        if self.precipitation_duration_half is not None:
            output['precipitation_duration_by_half_day'] = self.precipitation_duration_half
        if self.precipitation_amount_half is not None:
            output['precipitation_amount_by_half_day'] = self.precipitation_amount_half
        if self.precipitation_duration is not None:
            output['precipitation_duration'] = self.precipitation_duration
        if self.precipitation_amount is not None:
            output['precipitation_amount'] = self.precipitation_amount

        return output, self._YY
