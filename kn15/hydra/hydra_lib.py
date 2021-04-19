
EMPTY_OUTPUT = {
    'stage': None,
    'change_stage': None,
    'previous_stage': None,
    'water_temperature': None,
    'air_temperature': None,
    'ice_conditions': None,
    'water_conditions': None,
    'ice_thickness': None,
    'snow_depth': None,
    'discharge': None,
    'precipitation_duration_by_half_day': None,
    'precipitation_amount_by_half_day': None,
    'precipitation_duration': None,
    'precipitation_amount': None,
    'cross-sectional_area': None,
    'max_water_depth': None,
    'period': None,
    'avg_stage': None,
    'max_stage': None,
    'min_stage': None,
    'avg_discharge': None,
    'max_discharge': None,
    'min_discharge': None,
    'day_of_max': None,
    'hour_of_max': None,
    'reservoir_upstream_stage': None,
    'reservoir_avg_stage': None,
    'reservoir_previous_avg_stage': None,
    'reservoir_downstream_stage': None,
    'reservoir_max_downstream_stage': None,
    'reservoir_min_downstream_stage': None,
    'reservoir_volume': None,
    'reservoir_previous_volume': None,
    'reservoir_total_inflow': None,
    'reservoir_side_inflow': None,
    'reservoir_water_area_inflow': None,
    'reservoir_sum_previous_total_inflow': None,
    'reservoir_sum_previous_side_inflow': None,
    'reservoir_sum_previous_water_area_inflow': None,
    'reservoir_water_discharge': None,
    'reservoir_wind_direction': None,
    'reservoir_wind_speed': None,
    'reservoir_wave_direction': None,
    'reservoir_wave_depth': None,
    'reservoir_water_surface_condition': None,
    'measure_month': None,
    'measure_day': None,
    'measure_synophour': None,
    'disaster_type': None
}

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

"""Section 3 Group 3"""
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

"""Section 6 Group 6"""
WIND_DIRECTION_SCALE = [
    'ветра нет, штиль',
    'с северо-востока',
    'с востока',
    'с юго-востока',
    'с юга',
    'с юго-запада',
    'с запада',
    'с северо-запада',
    'с севера',
    'установить невозможно'
]

"""Section 6 Group 7"""
WAVE_DIRECTION_SCALE = [
    'волнения нет',
    'с северо-востока',
    'с востока',
    'с юго-востока',
    'с юга',
    'с юго-запада',
    'с запада',
    'с северо-запада',
    'с севера',
    'толчея'
]

"""Section 6 Group 7"""
WATER_SURFACE_SCALE = [
    'Зеркально-гладкая поверхность.',
    'Рябь, появляются небольшие гребни волн.',
    'Небольшие гребни волн начинают опрокидываться, но пена не белая, а стекловидная.',
    'Хорошо заметные небольшие волны, гребни некоторых из них опрокидываются, \
    образуя местами белую клубящуюся пену — «барашки».',
    'Волны принимают хорошо выраженную форму, повсюду образуются «барашки».',
    'Появляются гребни большой высоты, их пенящиеся вершины занимают большие площади, \
    ветер начинает срывать пену с гребней волн.',
    'Гребни очерчивают длинные волны ветровых волн; \
    пена, срываемая с гребней ветром начинает вытягиваться полосами по склонам волн.',
    'Длинные полосы пены, срываемые ветром, покрывают склоны волн, а местами, сливаясь, достигают их подошв.',
    'Пена широкими, плотными, сливающимися полосами покрывает склоны волн, отчего вся поверхность становится белой; \
    только местами, во впадинах волн, видны свободные от пены участки.',
    'Поверхность воды покрыта плотным слоем пены, воздух наполнен водяной пылью и брызгами, \
    видимость значительно уменьшена.'
]

"""Section 7 Group 0"""
disaster_types = {
    1: 'Высокие уровни воды (при половодьях, дождевых паводках, заторах, \
зажорах, ветровых нагонах), при которых наблюдается затопление \
пониженных частей городов, населенных пунктов, посевов \
сельскохозяйственных культур, автомобильных дорог или повреждение \
хозяйственных объектов.',
    2: 'Низкие уровни воды — ниже проектных отметок водозаборных \
сооружений крупных городов, промышленных районов и оросительных \
систем, навигационных уровней на судоходных реках.',
    3: 'Раннее (октябрь) образование ледостава и появление льда на \
судоходных реках, повторяющееся не чаще чем 1 раз в 10 лет.',
    4: 'Очень большие или очень малые расходы воды, приток в водохранилище, \
сброс воды через гидроузел, нарушающие нормальные условия работы \
оросительных систем, гидротехнических сооруженный других \
хозяйственных объектов.',
    5: 'Очень сильный дождь - количество осадков не менее 50 мм за период \
не более 12 часов; продолжительный очень сильный дождь – количество \
осадков не менее 100 мм за период более 12 часов, но менее 48 часов.'
}

"""Section 7 Group 0 (short)"""
DISASTER_TYPES_SHORT = {
    1: 'высокие уровни воды',
    2: 'низкие уровни воды',
    3: 'раннее образование ледостава и появление льда',
    4: 'очень большие или очень малые расходы воды, приток, сброс',
    5: 'сильный дождь',
    6: 'сели',
    7: 'лавины'
}

class Error(Exception):
    """Class for exceptions raised when parsing report string"""
    pass


def valid_date(yy):
    if is_not_empty(yy) and not 1 <= int(yy) <= 31:
        raise Error(f'Day of month {yy} is not between 1 and 31')
    if yy is None:
        return None
    else:
        return int(yy)


def valid_time(gg, lim=23):
    if is_not_empty(gg) and not 0 <= int(gg) <= lim:
        raise Error(f'Time of measure {gg} is not between 00 and {lim}')
    if gg is None:
        return None
    else:
        return int(gg)


def valid_month(mm):
    if is_not_empty(mm) and not 1 <= int(mm) <= 12:
        raise Error(f'Month {mm} is not between 1 and 12')
    if mm is None:
        return None
    else:
        return int(mm)


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


def get_flow(flow):
    """Return 'flow' according to 'Section 1 Group 8' rules.
    Use the same to return 'volume' from 'Section 4 Group 7 (and 8)'
    and 'area' from 'Section 6 Group 3'."""
    return float(flow[1:]) * pow(10, int(flow[0]) - 3)


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


def get_scale(param, scale, verbose=False):
    """Parse 'precipitation_duration' with duration array according to 'Section 1 Group 9 (and 0)' rules.
    Use the same to return 'wind_direction', 'wave_direction', 'surface_condition' from 'Section 6 Group 6 (and 7)'
    Use 'verbose=True' to return conditions title."""
    param = int(param)
    if 0 <= param < len(scale):
        if verbose:
            return scale[param]
        else:
            return param
    else:
        raise Error(f'Array does not contain match for element code {param}')


def get_identify_param(param, dict, verbose=False):
    """Parse 'period' and 'disaster_type', with dictionary.
    Raise error if param is empty.
    Use 'verbose=True' to return conditions title."""
    param = int(param)
    if key_in_dict(param, dict):
        if verbose:
            return dict[param]
        else:
            return param
    else:
        raise Error(f'Identify parameter is empty')
