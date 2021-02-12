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

## Фомат и типы данных
```
  identifier: String
, basin: String
, stage: Option[Int]
, discharge: Option[Float]
, ice_thickness: Option[Int]
, snow_depth: Option[String]
, precipation_duration: Option[String]
, precipation_amount: Option[Float]
, air_temperature: Option[Int]
, water_temperature: Option[Float]
, day_of_month: String
, synophour: String
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