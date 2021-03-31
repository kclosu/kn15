"""Section 1 Group 5"""
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

"""Section 1 Group 6"""
WATER_CONDITIONS = {
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

"""Section 1 Group 7"""
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

"""Section 1 Group 0"""
PRECIPITATION_DURATION_SCALE = [
    "менее 1 ч",
    "от 1 до 3 ч",
    "от 3 до 6 ч",
    "от 6 до 12 ч",
    "более 12 ч"
]

"""Section 3 Group 933"""
PERIODS = {
    1: 'за прошедшие сутки',
    11: 'за первую декаду',
    22: 'за вторую декаду',
    33: 'за третью декаду',
    20: 'за 20 дней',
    25: 'за 25 дней',
    30: 'за месяц',
    4: 'за дождевой паводок',
    5: 'за половодье'
}


class Error(Exception):
    """Class for exceptions raised when parsing report string"""
    pass


def valid_date(date):
    if is_not_empty(date) and not 1 <= int(date) <= 31:
        raise Error(f'Day of month {date} is not between 1 and 31')
    if date is None:
        return None
    else:
        return int(date)


def valid_time(time, lim=23):
    if is_not_empty(time) and not 0 <= int(time) <= lim:
        raise Error(f'Time of measure {time} is not between 00 and {lim}')
    return int(time)


def is_not_empty(param):
    """Return True if the attribute is not empty"""
    if param is not None:
        param = str(param)
        if param.isdigit():
            return True
        if not param.isdigit() and param != len(param) * '/':
            raise Error(f'Impossible to parse content in block: {param}')


def key_in_dict(key, dict):
    """Return True if key is in dictionary"""
    if key in dict.keys():
        return True
    else:
        raise Error(f'Dictionary does not contain match for element code {key}')


def get_stage(stage):
    """Return 'stage' according to 'Section 1 Group 1' rules"""
    stage = int(stage)
    return stage if stage < 5000 else (5000 - stage)


def get_flow(flow, int_part):
    """Return 'flow' according to 'Section 1 Group 8' rules"""
    return float(flow) * pow(10, int(int_part) - 3)


def get_conditions(conditions, dict, verbose=False):
    """Parse 'conditions' with conditions dictionary according to 'Section 1 Group 5 (and 6)' rules.
     Use 'verbose=True' to return conditions title."""
    out = []
    for condition in conditions:
        if is_not_empty(condition):
            l_part = int(condition[:2])
            r_part = int(condition[2:])
            if key_in_dict(l_part, dict):
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
                    if l_part != r_part and key_in_dict(r_part, dict):
                        if verbose:
                            out.append({'title': dict[r_part]})
                        else:
                            out.append({'code': r_part})
    return out


def get_amount(precip_amount, verbose=False):
    """Parse 'precipitation_amount' according to 'Section 1 Group 9 (and 0)' rules.
     Use 'verbose=True' to return conditions title."""
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


def get_duration(duration, arr, verbose=False):
    """Parse 'precipitation_duration' with duration array according to 'Section 1 Group 9 (and 0)' rules.
     Use 'verbose=True' to return conditions title."""
    duration = int(duration)
    if 0 <= duration < len(arr):
        if verbose:
            return arr[duration]
        else:
            return duration
    else:
        raise Error(f'Array does not contain match for element code {duration}')
