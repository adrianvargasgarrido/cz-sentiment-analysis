# Misclassification Report

## Most Frequent Errors

| True Label | Predicted Label | Count |
|------------|-----------------|-------|
| Negative | Neutral | 70 |
| Neutral | Negative | 67 |
| Neutral | Positive | 45 |
| Positive | Neutral | 38 |
| Negative | Positive | 10 |

## Sample Misclassified Comments (50)

### Example 1
**True:** `Positive` (4.1%) | **Predicted:** `Negative` (58.5%)

Confidence interval (top-2 probs): [37.4%, 58.5%] | Gap: 21.1%

````
právě v tuto chvíli signál naskočil.hurá ! <repeat>
````

### Example 2
**True:** `Neutral` (33.3%) | **Predicted:** `Negative` (63.0%)

Confidence interval (top-2 probs): [33.3%, 63.0%] | Gap: 29.7%

````
no prý chyba , prý je to tahle : <url> je to o pár příspěvků níže . <repeat>
````

### Example 3
**True:** `Positive` (3.6%) | **Predicted:** `Neutral` (63.1%)

Confidence interval (top-2 probs): [33.3%, 63.1%] | Gap: 29.7%

````
takže : samoobsluha funguje! teda mně , nevím , jak ostatním. děkuji.
````

### Example 4
**True:** `Negative` (11.5%) | **Predicted:** `Neutral` (69.8%)

Confidence interval (top-2 probs): [18.7%, 69.8%] | Gap: 51.1%

````
snad se odpovědi dočkám i já. včera tři cheese za 75 , -. no fuj velebnosti!
````

### Example 5
**True:** `Negative` (4.4%) | **Predicted:** `Positive` (74.4%)

Confidence interval (top-2 probs): [21.2%, 74.4%] | Gap: 53.1%

````
taky jsem se nachytala : -) minuly mesic jsem platila skoro 2000 , - kvuli zmenam : -)
````

### Example 6
**True:** `Positive` (8.1%) | **Predicted:** `Neutral` (76.3%)

Confidence interval (top-2 probs): [15.5%, 76.3%] | Gap: 60.8%

````
škoad že se to nedá poslat poštou : d hned bych si koupil 3 plata : ) : d
````

### Example 7
**True:** `Positive` (41.2%) | **Predicted:** `Neutral` (51.8%)

Confidence interval (top-2 probs): [41.2%, 51.8%] | Gap: 10.6%

````
jestli jsem před chvílí dostala bodíky pro školku od vás tak mooc děkuji .
````

### Example 8
**True:** `Neutral` (21.9%) | **Predicted:** `Positive` (73.5%)

Confidence interval (top-2 probs): [21.9%, 73.5%] | Gap: 51.6%

````
no a ještě jsou fidorky od milky. v rakousku jsme je kupovali (s minies a dalšími novinkami) už v létě 2010.
````

### Example 9
**True:** `Negative` (25.7%) | **Predicted:** `Positive` (40.9%)

Confidence interval (top-2 probs): [33.4%, 40.9%] | Gap: 7.4%

````
paráda.sice prý jakoýe spuštěno , ale do muj t mobile se neprihlasim . <repeat>
````

### Example 10
**True:** `Negative` (27.9%) | **Predicted:** `Neutral` (68.1%)

Confidence interval (top-2 probs): [27.9%, 68.1%] | Gap: 40.3%

````
když mi nenačtou body tak nestihnu asi nic
````

### Example 11
**True:** `Neutral` (43.6%) | **Predicted:** `Negative` (53.5%)

Confidence interval (top-2 probs): [43.6%, 53.5%] | Gap: 9.9%

````
kočky , fuj já radši pejsky
````

### Example 12
**True:** `Neutral` (35.7%) | **Predicted:** `Negative` (60.5%)

Confidence interval (top-2 probs): [35.7%, 60.5%] | Gap: 24.8%

````
matěj : joo , svět je krutej
````

### Example 13
**True:** `Negative` (25.2%) | **Predicted:** `Neutral` (70.3%)

Confidence interval (top-2 probs): [25.2%, 70.3%] | Gap: 45.1%

````
přišel jsem 26. června v úterý . <repeat> jak je psáno na vašich stránkách . <repeat> a nic o.o
````

### Example 14
**True:** `Negative` (46.3%) | **Predicted:** `Neutral` (50.6%)

Confidence interval (top-2 probs): [46.3%, 50.6%] | Gap: 4.3%

````
to mě taky. jedinou smsku se mi podařilo odeslat v době , kdy mi na pouhou minutu naskočila brána a dotyčná čeká na druhou část smsky. marně.
````

### Example 15
**True:** `Neutral` (33.2%) | **Predicted:** `Negative` (62.9%)

Confidence interval (top-2 probs): [33.2%, 62.9%] | Gap: 29.7%

````
dobry dem mam dotaz chtela jsem si nastavit internet v mobilu a nejak mi to nejde
````

### Example 16
**True:** `Neutral` (37.2%) | **Predicted:** `Negative` (58.7%)

Confidence interval (top-2 probs): [37.2%, 58.7%] | Gap: 21.6%

````
jo leda bez lidi podel steny , jinak je to leda na hromadne cvachtani.
````

### Example 17
**True:** `Negative` (31.2%) | **Predicted:** `Neutral` (65.1%)

Confidence interval (top-2 probs): [31.2%, 65.1%] | Gap: 33.9%

````
ve vejprtech (okres chomutov) už asi 6 hodin nemáme signál v mobilu.kam tuto skutečnost máme nahlásit.
````

### Example 18
**True:** `Positive` (32.1%) | **Predicted:** `Neutral` (59.7%)

Confidence interval (top-2 probs): [32.1%, 59.7%] | Gap: 27.6%

````
no me se prave to volání hodí . <repeat> a sms do jiných sítí mám vyřešeno jinak : ))
````

### Example 19
**True:** `Neutral` (28.3%) | **Predicted:** `Positive` (66.6%)

Confidence interval (top-2 probs): [28.3%, 66.6%] | Gap: 38.4%

````
neni to fotka z obchodu asi tezko by tam mohl byt parfem harem z lr , moc hezka skrinka!
````

### Example 20
**True:** `Negative` (41.8%) | **Predicted:** `Neutral` (53.8%)

Confidence interval (top-2 probs): [41.8%, 53.8%] | Gap: 12.0%

````
u xperie mám problém s dílenskím zpracováním plastů , které rádi praskají. takže po krátké úvaze co k vánocům se podívám na lepší : )
````

### Example 21
**True:** `Negative` (15.4%) | **Predicted:** `Neutral` (73.0%)

Confidence interval (top-2 probs): [15.4%, 73.0%] | Gap: 57.5%

````
laskavě si to papouškování strčte někam!
````

### Example 22
**True:** `Negative` (34.0%) | **Predicted:** `Neutral` (61.6%)

Confidence interval (top-2 probs): [34.0%, 61.6%] | Gap: 27.6%

````
a bude uz jenom hur. je potreba jeste zdrazit co zdrazit jde , pripadne prodlouzit uvazky na 5let a bude
````

### Example 23
**True:** `Positive` (16.0%) | **Predicted:** `Neutral` (73.7%)

Confidence interval (top-2 probs): [16.0%, 73.7%] | Gap: 57.8%

````
já bych zájem určitě měl - jestli ho ještě pořád máš tak se mi prosím ozvi : -)
````

### Example 24
**True:** `Neutral` (45.7%) | **Predicted:** `Negative` (48.9%)

Confidence interval (top-2 probs): [45.7%, 48.9%] | Gap: 3.2%

````
stopovala směr mnichov , večer jsem jí zahlédl ! <repeat> nechybí vám tam taky medvěd? ten totiž stopoval s ní ! <repeat> láska je láska
````

### Example 25
**True:** `Neutral` (38.8%) | **Predicted:** `Negative` (57.9%)

Confidence interval (top-2 probs): [38.8%, 57.9%] | Gap: 19.1%

````
to aby nám to nebylo líto
````

### Example 26
**True:** `Negative` (27.1%) | **Predicted:** `Neutral` (66.7%)

Confidence interval (top-2 probs): [27.1%, 66.7%] | Gap: 39.6%

````
kubajs šindelář : : d já tě alespoň nazývám celým jménem : ) a nebuď drzý na jednom pískovišti jsme spolu bábovky nedělali
````

### Example 27
**True:** `Neutral` (38.3%) | **Predicted:** `Negative` (58.8%)

Confidence interval (top-2 probs): [38.3%, 58.8%] | Gap: 20.5%

````
pravděpodobně některá z oponentních žen , co se jim nelíbí focení žirafy mne blokla , tudíž nemohu diskutovat
````

### Example 28
**True:** `Neutral` (41.7%) | **Predicted:** `Positive` (52.8%)

Confidence interval (top-2 probs): [41.7%, 52.8%] | Gap: 11.1%

````
nokia 5110 , ještě ji tu mám : -)
````

### Example 29
**True:** `Neutral` (33.3%) | **Predicted:** `Negative` (63.4%)

Confidence interval (top-2 probs): [33.3%, 63.4%] | Gap: 30.1%

````
furt nemate žadny informace nebo jste zapoměli ? <repeat>
````

### Example 30
**True:** `Positive` (24.5%) | **Predicted:** `Neutral` (64.3%)

Confidence interval (top-2 probs): [24.5%, 64.3%] | Gap: 39.8%

````
dorazili mi čepice a penály pro děti , dostanou je k mikuláši , tak douvám , že je nadchnou tak jako mě. m
````

### Example 31
**True:** `Positive` (11.6%) | **Predicted:** `Neutral` (71.3%)

Confidence interval (top-2 probs): [17.2%, 71.3%] | Gap: 54.1%

````
jj , dobré je máte , sice jsem to jedl studené , protože byly nestíhačky , ale good : d : d : d
````

### Example 32
**True:** `Neutral` (44.4%) | **Predicted:** `Negative` (50.8%)

Confidence interval (top-2 probs): [44.4%, 50.8%] | Gap: 6.4%

````
pokušeni ! <repeat>
````

### Example 33
**True:** `Negative` (11.3%) | **Predicted:** `Neutral` (74.9%)

Confidence interval (top-2 probs): [13.7%, 74.9%] | Gap: 61.2%

````
kristýna floková : než něco vypustíš , tak si to ověř ; -)
````

### Example 34
**True:** `Neutral` (46.2%) | **Predicted:** `Negative` (50.7%)

Confidence interval (top-2 probs): [46.2%, 50.7%] | Gap: 4.5%

````
volal jsem kolegyni taky na t-mobile z jineho tel a jí sem se dovolal , tak to asi nebude úplně plošné
````

### Example 35
**True:** `Neutral` (21.9%) | **Predicted:** `Positive` (73.1%)

Confidence interval (top-2 probs): [21.9%, 73.1%] | Gap: 51.2%

````
facebookale nic , no : ) jen k vám nemůžu tak často! ale pěkná akcička to je!
````

### Example 36
**True:** `Negative` (44.9%) | **Predicted:** `Neutral` (51.7%)

Confidence interval (top-2 probs): [44.9%, 51.7%] | Gap: 6.8%

````
každopádně má ode dneška vodafone co žehlit . <repeat>
````

### Example 37
**True:** `Negative` (37.2%) | **Predicted:** `Neutral` (59.3%)

Confidence interval (top-2 probs): [37.2%, 59.3%] | Gap: 22.1%

````
asi zapomněli připsat vzkaz ve stylu "tady za 10 let zprovozníme signál , který už dnes mají v pákistánu" . <repeat>
````

### Example 38
**True:** `Neutral` (28.5%) | **Predicted:** `Positive` (66.9%)

Confidence interval (top-2 probs): [28.5%, 66.9%] | Gap: 38.4%

````
naše kofolácká rodinka : d . <repeat> v jinolicích : )
````

### Example 39
**True:** `Negative` (15.5%) | **Predicted:** `Neutral` (70.2%)

Confidence interval (top-2 probs): [15.5%, 70.2%] | Gap: 54.7%

````
ja sem to mel take a je to docela male nato jak to vypada na obrazku a stoji 75kč lol
````

### Example 40
**True:** `Negative` (40.8%) | **Predicted:** `Neutral` (47.0%)

Confidence interval (top-2 probs): [40.8%, 47.0%] | Gap: 6.2%

````
pěkne hnusnej : d
````

### Example 41
**True:** `Negative` (42.8%) | **Predicted:** `Neutral` (54.1%)

Confidence interval (top-2 probs): [42.8%, 54.1%] | Gap: 11.2%

````
nesnáším když dojdu do hospody a oni mi oznámí že nemají kofolu
````

### Example 42
**True:** `Neutral` (42.4%) | **Predicted:** `Negative` (54.0%)

Confidence interval (top-2 probs): [42.4%, 54.0%] | Gap: 11.7%

````
tak tohle žádný slogan nepotřebuje . <repeat> to bude fungovat samo . <repeat> : ddd
````

### Example 43
**True:** `Positive` (3.6%) | **Predicted:** `Neutral` (54.0%)

Confidence interval (top-2 probs): [42.5%, 54.0%] | Gap: 11.5%

````
opravdu? to mi spadl kámen ze srdce , snad to bude tak jak říkáte . <repeat> děkuji.
````

### Example 44
**True:** `Neutral` (17.4%) | **Predicted:** `Positive` (78.3%)

Confidence interval (top-2 probs): [17.4%, 78.3%] | Gap: 61.0%

````
dávám si . <repeat> ale z petky . <repeat> : ( čep je nej : )
````

### Example 45
**True:** `Neutral` (40.8%) | **Predicted:** `Negative` (55.9%)

Confidence interval (top-2 probs): [40.8%, 55.9%] | Gap: 15.1%

````
nejde mi o mobilní net . <repeat> já chci levné volání a to je se slevou 75 % . <repeat>
````

### Example 46
**True:** `Neutral` (34.6%) | **Predicted:** `Negative` (58.6%)

Confidence interval (top-2 probs): [34.6%, 58.6%] | Gap: 24.0%

````
toto co je za nastup zimy , velmi , velmi trpim , asi sa zakuklim a do velkej noci nevyjdem z kukly von
````

### Example 47
**True:** `Negative` (35.5%) | **Predicted:** `Neutral` (60.1%)

Confidence interval (top-2 probs): [35.5%, 60.1%] | Gap: 24.5%

````
ani náhodou . <repeat>
````

### Example 48
**True:** `Neutral` (37.5%) | **Predicted:** `Positive` (57.3%)

Confidence interval (top-2 probs): [37.5%, 57.3%] | Gap: 19.8%

````
už mám objednáno =)
````

### Example 49
**True:** `Neutral` (34.2%) | **Predicted:** `Negative` (61.9%)

Confidence interval (top-2 probs): [34.2%, 61.9%] | Gap: 27.6%

````
panežo myslíte , že jím stojí za to tam dát o hambrugra míń ? <repeat> stjene z toho nic nemaj
````

### Example 50
**True:** `Negative` (15.9%) | **Predicted:** `Neutral` (75.8%)

Confidence interval (top-2 probs): [15.9%, 75.8%] | Gap: 59.9%

````
kdy opravíte ty sms z netu? už je to docela voser ; )
````

