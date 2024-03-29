# Парсер телеграмм в коде КН-15
Код КН-15 предназначен для передачи данных наблюдений на гидрологических постах, расположенных на реках, озерах и водохранилищах.

Состоит из разделов, каждый из которых предназначен для кодирования определенного вида данных.

Раздел 0 является обязательным для каждой телеграммы, включает буквенный опознаватель кода **HHZZ**, индекс гидрологического поста, дату и срок проведения наблюдений.

Раздел 1 – основной, предназначен для кодирования данных стандартных наблюдений на гидрологических постах за основной срок наблюдений 08 ч местного времени и за дополнительные сроки в периоды учащенных наблюдений.

Разделы 2-6 – дополнительные, предназначены для кодирования данных об измеренных расходах воды, о ветре и волнении на озерах и водохранилищах, об уровнях воды в бьефе водохранилищ и о притоке воды в водохранилища, о средних и экстремальных уровнях и расходах воды за периоды и т. д.

Раздел 7 предназначен для кодирования информации об опасных явлениях.

Каждый раздел состоит из пятизначных кодовых групп. Кодовые группы в разделе имеют свои постоянные отличительные номера, которые определяют содержание группы в данном разделе. Для указания отсутствия данных в группе, обязательных для помещения в телеграмме, используется знак дроби (/).
Разделам 2-7 присвоена постоянная опознавательная группа, которая обязательно передается впереди групп данных, предусмотренных этим разделом. Опознавательная пятизначная группа раздела включается всегда, когда за ней следует хотя бы одна кодовая группа данного раздела.

Составление и передача информации об опасных явлениях осуществляется в соответствии с разделом 7.

Содержание телеграммы не является стандартным. Пропуск групп и разделов разрешен в случае отсутствия наблюдений на посту.

## Фомат и типы данных

Каждое сообщение содержит json co следующими полями:

```
__GROUP_0__

  'identifier' - индекс гидрологического поста <string>
  'basin' - номер бассейна реки, в котором расположен пост <string>
  'day_of_month' - дата наблюдений <string>
  'synophour' - срок наблюдений <string>
  
__GROUP_1__

  'stage' - уровень воды над нулем поста в срок наблюдения, см <int>
  'change_stage' - изменение уровня воды: разница между уровнем воды, передаваемым в настоящей 
телеграмме, и уровнем воды в предшествующий 08-часовой срок, см <int>
  'previous_stage' - уровень воды над нулем поста за 20-часовой срок наблюдений предшествующих 
суток, см <int>
  'water_temperature' - температура воды с точностью до десятых долей, °C <float>
  'air_temperature' -  температура воздуха с точностью до целого градуса, °C <int>
  'ice_conditions' - характеристика и интенсивность ледового явления, характеризующего степень 
покрытия реки или видимой акватории водоема наблюдаемым ледовым явлением, %  
                [{'title': <string>}, {'title': <string>, 'intensity': <int>}]
  'water_conditions' - характеристика состояния водного объекта и интенсивность явления, 
характеризующего степень  покрытия акватории водоема наблюдаемым водным явлением, % 
                [{'title': <string>}, {'title': <string>, 'intensity': <int>}]
  'ice_thickness' - толщина льда, см <int>
  'snow_depth' - высота снега на льду, см <string>
  'discharge' - ежедневный расход воды относительно уровня, указанного в поле 'stage', 
м3/с <float>
  'precipitation_duration_by_half_day' - количество осадков, выпавших за половину суток 
(от 08 ч до 20 ч местного времени предыдущего дня подачи телеграммы), мм <int>
  'precipitation_amount_by_half_day' - общая продолжительность выпадения осадков за половину 
суток (от 08ч до 20ч местного времени предыдущего дня подачи телеграммы), час <string>
  'precipitation_duration' - количество осадков в миллиметрах, выпавших за сутки (от 08ч 
местного времени предыдущего дня до 08 ч дня подачи телеграммы), мм <int>
  'precipitation_amount' - общая продолжительность выпадения осадков за сутки (от 08ч местного 
времени предыдущего дня до 08ч дня подачи телеграммы), час <string>
  'water_code_status' - номер режимной  группы явлений (в соответствии с характеристиками
ледовых явлений и состоянием водного объекта), [<int>] 
  'cross_sectional_area' - площадь живого сечения реки, м2 <float> 
  'max_water_depth' - максимальная глубина на гидростворе, см <int> 

__GROUP_2__

  'period' - <string> период, за который приводятся в телеграмме сведения о средних и 
экстремальных значениях:
      за прошедшие сутки,
      за первую декаду,
      за вторую декаду,
      за третью декаду,
      за 20 дней, с 1 по 20 число,
      за 25 дней, с 1 по 25 число,
      за месяц, независимо от продолжительности месяца в днях,
      за дождевой паводок,
      за половодье 
  'avg_stage' - средний уровень воды за период, см <int>
  'max_stage' - высший уровень воды за период, см <int>
  'min_stage' - низший уровень воды за период, см <int>
  'avg_discharge' - средний расход (приток) воды за период, м3/с <float> 
  'max_discharge' - высший расход (приток) воды за период, м3/с <float> 
  'min_discharge' - низший расход (приток) воды за период, м3/с <float> 
  'day_of_max' - дата (число месяца) прохождение наивысшего уровня (расхода) воды <int>
  'hour_of_max' - час местного времени прохождение наивысшего уровня (расхода) воды <int>
  
__GROUP_3__ 

  'reservoir_upstream_stage' - уровень воды верхнего бьефа водохранилища над нулем поста в срок 
наблюдений, см <int> 
  'reservoir_avg_stage' - средний (по площади) уровень водохранилища над нулем поста в срок 
наблюдений, см <int>
  'reservoir_previous_avg_stage' - средний (по площади) уровень водохранилища над нулем поста на 
конец предшествующих календарных суток, см <int>
  'reservoir_downstream_stage' - уровень воды нижнего бьефа над нулем поста в срок наблюдений, 
см <int>
  'reservoir_max_downstream_stage' - высший за предшествующие сутки уровень воды нижнего бьефа над 
нулем поста, см <int> 
  'reservoir_min_downstream_stage' - низший за предшествующие сутки уровень воды нижнего бьефа над 
нулем поста, см <int> 
  'reservoir_volume' - объем воды в водохранилище по среднему уровню в срок наблюдений, 
млн м3, <float> 
  'reservoir_previous_volume' - объем воды в водохранилище по среднему уровню на конец 
предшествующих календарных суток, млн м3, <float> 
  'reservoir_total_inflow' - общий приток воды в срок наблюдений, м3/с <float>
  'reservoir_side_inflow' - боковой приток воды в срок наблюдений, м3/с <float>
  'reservoir_water_area_inflow' - приток воды к акватории водохранилища в срок наблюдений, 
м3/с <float>
  'reservoir_sum_previous_total_inflow' - средний общий приток воды за предшествующие сутки, 
м3/с <float>
  'reservoir_sum_previous_side_inflow' - средний боковой приток воды за предшествующие сутки, 
м3/с <float>
  'reservoir_sum_previous_water_area_inflow' - средний приток к акватории за предшествующие 
сутки, м3/с <float> 
  'reservoir_water_discharge' - средний сброс воды за предшествующие сутки, м3/с <float>  
  'reservoir_wind_direction' - направление ветра <string> 
  'reservoir_wind_speed' - скорость ветра, м/с <int>
  'reservoir_wave_direction' - направление волнения (откуда идет волна) <string>
  'reservoir_wave_depth' - высота ветровых волн, дм <int>
  'reservoir_water_surface_condition' - характеристика состояния поверхности водоема в баллах <int>
  
__GROUP_4__

  'measure_month' - месяц, к которому относятся данные об измеренных расходах воды или состоянии 
поверхности озера (водохранилища) <int>
  'measure_day' - число месяца, к которому относятся данные об измеренных расходах воды или 
состоянии поверхности озера (водохранилища) <int>
  'measure_synophour' - час по местному времени, к которому относятся данные об измеренных расходах 
воды или состоянии поверхности озера (водохранилища) <int>

__GROUP_5__

  'disaster_type' - <string> вид стихийного явления: 
      высокие уровни воды,
      низкие уровни воды,
      раннее образование ледостава и появление льда,
      очень большие или очень малые расходы воды, приток, сброс,
      очень сильный дождь
      сели,
      лавины
  'special_marks' - <string> текстовая часть сообщения содержащая время начала,усиления или 
окончания явления, количественную характеристику явления, а также имеющиеся сведения о 
причинах возникновения или усиления опасного явления, сопутствующих обстоятельствах,
тенденции развития, нанесенном ущербе и мерах по уменьшению ущерба. 
```

Поля из GROUP0 включаются в каждое сообщение. Дата и срок наблюдений, данные которых передаются в разделе 1, 
заполняются из данных раздела 0.
Для передаваемых данных каждого дополнительного раздела формируется отдельное сообщение. 
В этом случае указывается дата и время из соответствующего раздела. 
Для передаваемых данных из раздела 6 указывается дата и время из раздела 0 в GROUP0, 
 так же указывается месяц, дата, и время к которому относятся данные об измеренных расходах воды или 
состоянии поверхности озера (водохранилища) в GROUP5. 

GROUP1 формируется из данных, передаваемых в разделах 1, 2 и 6 (часть 1) и содержит данные ежедневных стандартных 
наблюдений или данные об измеренных расходах воды, площади сечения водоема, глубины.

GROUP2 формируется из данных, передаваемых в разделе 3 и содержит данные средних, высших, и низших значений уровня
и расхода за период.

GROUP3 формируется из данных, передаваемых в разделах 4, 5, 6 (часть 2) и содержит данные об уровнях, объемах, притоке, 
состоянии поверхности водохранилища.

Данные об стихийном явлении обычно передаются отдельным сообщение (раздел 7) и формируют поля GROUP5 и GROUP1 при этом
GROUP5 заполняется обязательно.

Формат сообщения стандартный, значения полей не передаваемых в телеграмме заполняются 'None'. 
Если в сообщении присутствуют несколько дополнительных групп, то для каждой группы формируется отдельное сообщение.

При передаче телеграммы в разделе 0 передается параметр n, ограничивающий содержание (наличие разделов) телеграммы,
 ~~учитываемый только при формировании сообщения для телеграмм, которые должны включать только раздел 1 
(для корректного разбора блока '9RRRd'), в остальных случаях~~ игнорируется, т.е. вне зависимости от значения n 
будет предпринята попытка разбора всех возможных разделов вне зависимости от того, могут они присутствовать в данной телеграмме.

Текстовые поля добавляются при возможности выделения текстовой части
~~только к сообщениям о стихийных явлениях, остальные будут проигнорированы~~.

## Ссылки
* [Наставление гидрометеорологическим станциям и постам](http://docs.cntd.ru/document/1200108241) Описаны правила и методики проведения наблюдений на гидрологических постах
* [Руководящий документ по подготовка ежегодной информационной продукции водного кадастра](https://docplan.ru/Data2/1/4293792/4293792185.htm)
  Описаны правила усреднения
* https://pdf.standartgost.ru/catalog/Data2/1/4293775/4293775610.pdf

## Установка

##### Выполнить тесты
```
python -m unittest tests.py
```

## Использование
```
python parse.py --report "10950 31081 16161 20142 30175 499// 56563 56401 61105 61541 70511 80001 99993 09094"
    [
       {
          'identifier': 10950, 
          'basin': 10, 
          'day_of_month': 31, 
          'synophour': 8, 
          'special_marks': None
          'stage': -1161, 
          'change_stage': -14,
          'previous_stage': 175, 
          'water_temperature': 9.9, 
          'air_temperature': None,
          'ice_conditions': [{'title': 'Ледостав, ровный ледяной покров'}, 
                             {'title': 'Ледостав неполный'},
                             {'title': 'Ледяной покров с полыньями (промоинами, пропаринами)', 'intensity': 10}],
          'water_conditions': [{'title': 'Лесосплав', 'intensity': 50}, 
                               {'title': 'Залом леса ниже поста'},
                               {'title': 'Русло реки сужено на гидростворе для измерения расхода воды'}],
          'ice_thickness': 51, 
          'snow_depth': 'менее 5 см', 
          'discharge': 0.001,
          'precipitation_duration_by_half_day': 'от 6 до 12 ч', 
          'precipitation_amount_by_half_day': 0.9,
          'precipitation_duration': 'более 12 ч', 
          'precipitation_amount': 909.0, 
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
          'disaster_type': None,
       }
    ]
```

Из файла
```
python parse.py --filename samples/40.hydra
[{'identifier': 49904, 'basin': 49, 'day_of_month': 28, 'synophour': 8, 'special_marks': None, 'stage': 189, 'change_stage': 2, 'previous_stage': None, 'water_temperature': None, 'air_temperature': None, 'ice_conditions': None, 'water_conditions': [{'title': 'Чисто'}], 'ice_thickness': None, 'snow_depth': None, 'discharge': None, 'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None, 'precipitation_duration': 'менее 1 ч', 'precipitation_amount': 0.0, 'cross-sectional_area': None, 'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None}]
[{'identifier': 49907, 'basin': 49, 'day_of_month': 28, 'synophour': 8, 'special_marks': None, 'stage': 187, 'change_stage': 4, 'previous_stage': None, 'water_temperature': 2.4, 'air_temperature': 8, 'ice_conditions': [{'title': 'Лед относит (отнесло) от берега - для озер, водохранилищ'}], 'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None, 'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None, 'precipitation_duration': 'от 6 до 12 ч', 'precipitation_amount': 1.0, 'cross-sectional_area': None, 'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None}]
[{'identifier': 49001, 'basin': 49, 'day_of_month': 28, 'synophour': 8, 'special_marks': None, 'stage': 194, 'change_stage': 1, 'previous_stage': None, 'water_temperature': 6.8, 'air_temperature': None, 'ice_conditions': None, 'water_conditions': None, 'ice_thickness': None, 'snow_depth': None, 'discharge': None, 'precipitation_duration_by_half_day': None, 'precipitation_amount_by_half_day': None, 'precipitation_duration': 'от 1 до 3 ч', 'precipitation_amount': 0.0, 'cross-sectional_area': None, 'max_water_depth': None, 'period': None, 'avg_stage': None, 'max_stage': None, 'min_stage': None, 'avg_discharge': None, 'max_discharge': None, 'min_discharge': None, 'day_of_max': None, 'hour_of_max': None, 'reservoir_upstream_stage': None, 'reservoir_avg_stage': None, 'reservoir_previous_avg_stage': None, 'reservoir_downstream_stage': None, 'reservoir_max_downstream_stage': None, 'reservoir_min_downstream_stage': None, 'reservoir_volume': None, 'reservoir_previous_volume': None, 'reservoir_total_inflow': None, 'reservoir_side_inflow': None, 'reservoir_water_area_inflow': None, 'reservoir_sum_previous_total_inflow': None, 'reservoir_sum_previous_side_inflow': None, 'reservoir_sum_previous_water_area_inflow': None, 'reservoir_water_discharge': None, 'reservoir_wind_direction': None, 'reservoir_wind_speed': None, 'reservoir_wave_direction': None, 'reservoir_wave_depth': None, 'reservoir_water_surface_condition': None, 'measure_month': None, 'measure_day': None, 'measure_synophour': None, 'disaster_type': None}]

```
Из кода
```
from kn15 import decode, KN15

with open(filename, 'r') as f:
  bulletin = f.read()
  for report in decode(bulletin):
    try:
      print(KN15(report).decode())
    except Exception as ex:
      print(ex)
```
## TODO:
*explaine how to differenciate water temeprature 2 and 20, how about water under 10C

*if value of group 9RRRd (amount and duration of precipitation, for half a day from 08 to 20 local time 
on the previous day) starts with 922xx, 933xx, 944xx, 955xx, 966xx, 9770x then the parser views, it as the 
beginning of a new additional section 
