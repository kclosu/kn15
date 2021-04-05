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
```
__GROUP_0__

  'identifier' - индекс гидрологического поста <int>
  'basin' - номер бассейна реки, в котором расположен пост <int>
  'day_of_month' - дата наблюдений <int>
  'synophour' - срок наблюдений <int>
  
  Дата и срок наблюдений, данные которых передаются в разделах, следующих за разделом 0. Если в телеграмме после 
раздела 0 передаются только дополнительные разделы указывается дата и время передачи телеграммы с поста. 

__GROUP_1__

  'stage' - уровень воды над нулем поста в срок наблюдения, см <int>
  'change_stage' - изменение уровня воды: разница между уровнем воды, передаваемым в настоящей телеграмме, и уровнем 
воды в предшествующий 08-часовой срок, см <int>
  'previous_stage' - уровень воды над нулем поста за 20-часовой срок наблюдений предшествующих суток, см <int>
  'water_temperature' - температура воды с точностью до десятых долей, °C <float>
  'air_temperature' -  температура воздуха с точностью до целого градуса, °C <int>
  'ice_conditions' - характеристика и интенсивность ледового явления, характеризующего степень покрытия реки или видимой
акватории водоема наблюдаемым ледовым явлением, %  [{'title': string}, {'title': string, 'intensity': int}]
  'water_conditions' - характеристика состояния водного объекта и интенсивность явления, характеризующего состояние 
водного объекта, как степень  покрытия акватории водоема наблюдаемым водным явлением, % 
                                                                [{'title': string}, {'title': string, 'intensity': int}]
  'ice_thickness' - толщина льда, см <int>
  'snow_depth' - высота снега на льду, см <string>
  'discharge' - ежедневный расход воды относительно уровня, указанного в поле 'stage', м3/с <float>
  'precipitation_duration_by_half_day' - количество осадков, выпавших за половину суток (от 08 ч до 20 ч местного 
времени предыдущего дня подачи телеграммы), мм <int>
  'precipitation_amount_by_half_day' - общая продолжительность выпадения осадков за половину суток (от 08ч до 20ч 
местного времени предыдущего дня подачи телеграммы), час <string>
  'precipitation_duration' -количество осадков в миллиметрах, выпавших за сутки (от 08ч местного времени предыдущего 
дня до 08 ч дня подачи телеграммы), мм <int>
  'precipitation_amount' -общая продолжительность выпадения осадков за сутки (от 08ч местного времени предыдущего дня 
до 08ч дня подачи телеграммы), час <string>
  'cross-sectional_area' - площадь живого сечения реки, м2 <float> 
  'max_water_depth' - максимальная глубина на гидростворе, см <int> 

__GROUP_2__

  'period' - <string> период, за который приводятся в телеграмме сведения о средних и экстремальных значениях:
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

  'reservoir_upstream_stage' - уровень воды верхнего бьефа водохранилища над нулем поста в срок наблюдений, см <int> 
  'reservoir_avg_stage' - средний (по площади) уровень водохранилища над нулем поста в срок наблюдений, см <int>
  'reservoir_previous_avg_stage' - средний (по площади) уровень водохранилища над нулем поста на конец предшествующих
календарных суток, см <int>
  'reservoir_downstream_stage' - уровень воды нижнего бьефа над нулем поста в срок наблюдений, см <int>
  'reservoir_max_downstream_stage' - высший за предшествующие сутки уровень воды нижнего бьефа над нулем поста, см <int> 
  'reservoir_min_downstream_stage' - низший за предшествующие сутки уровень воды нижнего бьефа над нулем поста, см <int> 
  'reservoir_volume' - объем воды в водохранилище по среднему уровню в срок наблюдений, млн м3, <float> 
  'reservoir_previous_volume' - объем воды в водохранилище по среднему уровню на конец предшествующих календарных 
суток, млн м3, <float> 
  'reservoir_total_inflow' - общий приток воды в срок наблюдений, м3/с <float>
  'reservoir_side_inflow' - боковой приток воды в срок наблюдений, м3/с <float>
  'reservoir_water_area_inflow' - приток воды к акватории водохранилища в срок наблюдений, м3/с <float>
  'reservoir_sum_previous_total_inflow' - средний общий приток воды за предшествующие сутки, м3/с <float>
  'reservoir_sum_previous_side_inflow' - средний боковой приток воды за предшествующие сутки, м3/с <float>
  'reservoir_sum_previous_water_area_inflow' - средний приток к акватории за предшествующие сутки, м3/с <float> 
  'reservoir_water_discharge' - средний сброс воды за предшествующие сутки, м3/с <float>  
  'reservoir_wind_direction' - направление ветра <string> 
  'reservoir_wind_speed' - скорость ветра, м/с <int>
  'reservoir_wave_direction' - направление волнения (откуда идет волна) <string>
  'reservoir_wave_depth' - высота ветровых волн, дм <int>
  'reservoir_water_surface_condition' - характеристика состояния поверхности водоема в баллах <int>
  
__GROUP_4__

  'measure_month' - месяц, к которому относятся данные об измеренных расходах воды или состоянии поверхности озера 
(водохранилища) <int>
  'measure_day' - число месяца, к которому относятся данные об измеренных расходах воды или состоянии поверхности озера 
(водохранилища) <int>
  'measure_synophour' - час по местному времени, к которому относятся данные об измеренных расходах воды или состоянии 
поверхности озера (водохранилища) <int>

__GROUP_5__

  'disaster_type' - <string> вид стихийного явления: 
      высокие уровни воды,
      низкие уровни воды,
      раннее образование ледостава и появление льда,
      очень большие или очень малые расходы воды, приток, сброс,
      очень сильный дождь
      сели,
      лавины
  'special_marks': <string> текстовая часть сообщения с информацией о причинах, последствиях, прекращении или 
  продолжении стихийного явления 
```

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
python kn15/kn15.py --report "75317 31081 15233 20191 35242 41899="
{
  'stage': -233,
  'discharge': None,
  'ice_thickness': None,
  'snow_depth': None,
  'precipation_duration': None,
  'precipation_amount': None,
  'air_temperature': -49,
  'water_temperature': 1.8,
  'identifier': '75317',
  'basin': '75',
  'day_of_month': '31',
  'synophour': '08',
  'ice_conditions': None
}
```

```
python kn15/kn15.py --report "10950 31082 10161 20042 30163 56565 70530 //053 94431 20165 45046 95531 43695 74109 94430 20168 45046 95530 43655 74109 94429 20172 45036 95529 43607 74105 94428 20177 45043 95528 43565 73995"
{
  'stage': 161,
  'discharge': None,
  'ice_thickness': 53,
  'snow_depth': 'На льду снега нет',
  'precipation_duration': None,
  'precipation_amount': None,
  'air_temperature': None,
  'water_temperature': None,
  'identifier': '10950',
  'basin': '10',
  'day_of_month': '31',
  'synophour': '08',
  'ice_conditions': [{'title': 'Наледная вода', 'intensity': None}, {'title': 'Наледная вода', 'intensity': None}]}
```
На данный момент анализируется только Раздел 1 стандартных наблюдений на гидрологических постах за основной срок наблюдений 08 ч.
```
python kn15/kn15.py --report "11085 94411 10503 20508 40193 73145 95511 24115 44265 74254"
{
  'stage': None,
  'discharge': None,
  'ice_thickness': None,
  'snow_depth': None,
  'precipation_duration': None,
  'precipation_amount': None,
  'air_temperature': None,
  'water_temperature': None,
  'identifier': '11085',
  'basin': '11',
  'day_of_month': None,
  'synophour': None,
  'ice_conditions': None
}
```
Из файла
```
python kn15/kn15.py --filename samples/40.hydra
{'stage': 189, 'discharge': None, 'ice_thickness': None, 'snow_depth': None, 'precipation_duration': 'менее 1 ч', 'precipation_amount': 0.0, 'air_temperature': None, 'water_temperature': None, 'identifier': '49904', 'basin': '49', 'day_of_month': '28', 'synophour': '08', 'ice_conditions': None}
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