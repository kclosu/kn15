http://docs.cntd.ru/document/1200108241
https://docplan.ru/Data2/1/4293792/4293792185.htm
https://pdf.standartgost.ru/catalog/Data2/1/4293775/4293775610.pdf

```
  identifier: String
, basin: String
, stage: Option[Int]
, discharge: Option[Float]
, ice_thickness: Option[Int]
, snow_depth: Option[String]
, precipation_duration: Option[String]
, precipation_amount: Option[Int]
, air_temperature: Option[Float]
, water_temperature: Option[Float]
, day_of_month: String
, synophour: String
```

### Примеры сообщений о неблагоприятных явлениях
1. 22 февраля на посту 82013 в 08 час уровень воды был 557 см.; к 18 час уровень поднялся до 996 см над нулем поста. В результате подъема река вышла из берегов и размыла железнодорожную насыпь. Подъем уровня продолжается. Штормовое сообщение имеет вид:

```ННZZ 82013 22187 97701 10996 24391 СНЕГОТАЯНИЕ ЛИВЕНЬ РАЗМЫТА НАСЫПЬ ЖЕЛЕЗНОЙ ДОРОГИ ПОДЪЕМ ПРОДОЛЖАЕТСЯ```

2. Пост с индексом 84065 подает сообщение 12 июня о резком увеличении расхода воды вследствие прорыва вышерасположенной плотины. Расход, измеренный в 14 час, был равен 1260 м3/с. Сообщение имеет вид:

```ННZZ 84065 12147 97704 84126 ПРОРЫВ ВЫШЕРАСПОЛОЖЕННОЙ ПЛОТИНЫ```

3. Пост с индексом 07176 сообщает 12 февраля сведения о наледи, представляющей угрозу для объектов экономики. Указывается размер наледи, тенденция роста. Сообщение имеет вид:

```ННZZ 07176 12087 97703 НАЛЕДЬ 2000 НА 100 НА 1.6 М ВЫХОДЫ НАЛЕДНЫХ ВОД ЗНАЧИТЕЛЬНОЙ ПЛОЩАДИ УГРОЖАЮТ ПОЛОТНУ ЖЕЛЕЗНОЙ ДОРОГИ```

4. Пост с индексом 84233 сообщает 13 марта о возможном сходе лавин:

```HHZZ 84233 13087 97707 ОЖИДАЕТСЯ СХОД ЛАВИН ДОЛИНУ РЕКИ ЧЕГЕМ 13 14 15 ВТОРОЙ ПОЛОВИНЕ ДНЯ ВЫСОКИЕ ТЕМПЕРАТУРЫ ВОЗДУХА БОЛЬШИЕ СНЕГОЗАПАСЫ```

5. Пост с индексом 11314 сообщает 3 июля о значительном обрушении берега реки. В сообщении указывается местоположение, размер, характер обрушения и его последствия:

```ННZZ 11314 3 ИЮЛЯ УТРОМ ОБРУШИЛСЯ БЕРЕГ 2 КМ НИЖЕ ПОСТА РАЗРУШЕНЫ ВРЕМЕННЫЕ ПОСТРОЙКИ ЛЕТНЕГО ВЫГУЛА СКОТА```