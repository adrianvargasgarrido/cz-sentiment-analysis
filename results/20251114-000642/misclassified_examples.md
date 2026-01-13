# Misclassification Report

## Most Frequent Errors

| True Label | Predicted Label | Count |
|------------|-----------------|-------|
| Neutral | Negative | 72 |
| Negative | Neutral | 67 |
| Neutral | Positive | 46 |
| Positive | Neutral | 37 |
| Negative | Positive | 9 |

## Sample Misclassified Comments (50)

### Example 1
**True:** `Neutral` (24.0%) | **Predicted:** `Positive` (71.5%)

Confidence interval (top-2 probs): [24.0%, 71.5%] | Gap: 47.6%

````
clara - smoulinka uz nebude , byla prvni tyden a hned vyprodana! : )
````

### Example 2
**True:** `Negative` (37.0%) | **Predicted:** `Neutral` (59.2%)

Confidence interval (top-2 probs): [37.0%, 59.2%] | Gap: 22.3%

````
to radši dělaj mrtvý ani neodepíšou ; )
````

### Example 3
**True:** `Neutral` (47.1%) | **Predicted:** `Negative` (49.9%)

Confidence interval (top-2 probs): [47.1%, 49.9%] | Gap: 2.8%

````
lampárna je malá místnost na každém nádraží , kam se ukládají lampy . <repeat> tam se klidně můžete zeptat na cokoli a nikdo vám stejně neodpoví . <repeat>
````

### Example 4
**True:** `Negative` (17.6%) | **Predicted:** `Neutral` (75.1%)

Confidence interval (top-2 probs): [17.6%, 75.1%] | Gap: 57.4%

````
jaká bude kompenzace ? <repeat>
````

### Example 5
**True:** `Negative` (18.4%) | **Predicted:** `Neutral` (70.8%)

Confidence interval (top-2 probs): [18.4%, 70.8%] | Gap: 52.4%

````
zrovna chci napsat . <repeat> neumím si představit toto do sebe cpát teď na snídani. au , můj žaludek . <repeat> : -)
````

### Example 6
**True:** `Positive` (8.1%) | **Predicted:** `Neutral` (66.2%)

Confidence interval (top-2 probs): [25.7%, 66.2%] | Gap: 40.5%

````
dle mě je krevetový wrap lepší než byl beef , ale můj názor je jasný - crispy je lepší : d
````

### Example 7
**True:** `Neutral` (45.2%) | **Predicted:** `Negative` (49.3%)

Confidence interval (top-2 probs): [45.2%, 49.3%] | Gap: 4.1%

````
stopovala směr mnichov , večer jsem jí zahlédl ! <repeat> nechybí vám tam taky medvěd? ten totiž stopoval s ní ! <repeat> láska je láska
````

### Example 8
**True:** `Neutral` (32.8%) | **Predicted:** `Negative` (63.6%)

Confidence interval (top-2 probs): [32.8%, 63.6%] | Gap: 30.8%

````
dobry dem mam dotaz chtela jsem si nastavit internet v mobilu a nejak mi to nejde
````

### Example 9
**True:** `Neutral` (43.8%) | **Predicted:** `Negative` (53.1%)

Confidence interval (top-2 probs): [43.8%, 53.1%] | Gap: 9.3%

````
slevy na fesťáky by nebyly k zahození.
````

### Example 10
**True:** `Negative` (30.2%) | **Predicted:** `Neutral` (66.0%)

Confidence interval (top-2 probs): [30.2%, 66.0%] | Gap: 35.8%

````
když mi nenačtou body tak nestihnu asi nic
````

### Example 11
**True:** `Negative` (32.6%) | **Predicted:** `Neutral` (63.8%)

Confidence interval (top-2 probs): [32.6%, 63.8%] | Gap: 31.2%

````
prosím o smazání příspěvku od wenca konopnik!
````

### Example 12
**True:** `Negative` (45.7%) | **Predicted:** `Neutral` (51.4%)

Confidence interval (top-2 probs): [45.7%, 51.4%] | Gap: 5.8%

````
4tý den a pořád žádná odpověď od vás
````

### Example 13
**True:** `Positive` (12.4%) | **Predicted:** `Neutral` (66.7%)

Confidence interval (top-2 probs): [20.9%, 66.7%] | Gap: 45.8%

````
ááá vojta dělá žraloka . <repeat> : ddddddd
````

### Example 14
**True:** `Negative` (11.9%) | **Predicted:** `Neutral` (67.5%)

Confidence interval (top-2 probs): [20.6%, 67.5%] | Gap: 46.9%

````
snad se odpovědi dočkám i já. včera tři cheese za 75 , -. no fuj velebnosti!
````

### Example 15
**True:** `Neutral` (44.2%) | **Predicted:** `Negative` (53.2%)

Confidence interval (top-2 probs): [44.2%, 53.2%] | Gap: 9.0%

````
je nám líto , ale momentálně nemůžeme vyřešit váš požadavek. služba je dočasně nedostupná , prosíme opakujte akci později. kód chyby : g 502
````

### Example 16
**True:** `Negative` (16.7%) | **Predicted:** `Neutral` (68.3%)

Confidence interval (top-2 probs): [16.7%, 68.3%] | Gap: 51.6%

````
to je opravdu vybornej vysmech : -) chces zpet sve penize? zaplat : -)
````

### Example 17
**True:** `Negative` (26.7%) | **Predicted:** `Neutral` (68.5%)

Confidence interval (top-2 probs): [26.7%, 68.5%] | Gap: 41.9%

````
na co tohle všechno? akorát pak ženská ve 25 vypadá na 40 protože jí to ničí pleť ; )
````

### Example 18
**True:** `Positive` (16.5%) | **Predicted:** `Neutral` (72.1%)

Confidence interval (top-2 probs): [16.5%, 72.1%] | Gap: 55.6%

````
já bych zájem určitě měl - jestli ho ještě pořád máš tak se mi prosím ozvi : -)
````

### Example 19
**True:** `Neutral` (28.4%) | **Predicted:** `Positive` (66.4%)

Confidence interval (top-2 probs): [28.4%, 66.4%] | Gap: 38.0%

````
neni to fotka z obchodu asi tezko by tam mohl byt parfem harem z lr , moc hezka skrinka!
````

### Example 20
**True:** `Neutral` (23.9%) | **Predicted:** `Positive` (71.3%)

Confidence interval (top-2 probs): [23.9%, 71.3%] | Gap: 47.4%

````
přesně to se sem hodí . <repeat> never say no to panda . <repeat> a místo sýra kofola : d
````

### Example 21
**True:** `Positive` (7.0%) | **Predicted:** `Neutral` (62.5%)

Confidence interval (top-2 probs): [30.5%, 62.5%] | Gap: 32.0%

````
naprosto boží : o) tak mě napadá , že v kindervajíčkách už bylo lecjaký zvířátko , ale kolekce medojedů ještě ne : o)
````

### Example 22
**True:** `Negative` (29.1%) | **Predicted:** `Neutral` (65.9%)

Confidence interval (top-2 probs): [29.1%, 65.9%] | Gap: 36.8%

````
stále sem se nedočkal odpovědi : )
````

### Example 23
**True:** `Neutral` (34.4%) | **Predicted:** `Negative` (59.6%)

Confidence interval (top-2 probs): [34.4%, 59.6%] | Gap: 25.2%

````
toto co je za nastup zimy , velmi , velmi trpim , asi sa zakuklim a do velkej noci nevyjdem z kukly von
````

### Example 24
**True:** `Neutral` (43.6%) | **Predicted:** `Negative` (53.7%)

Confidence interval (top-2 probs): [43.6%, 53.7%] | Gap: 10.0%

````
dobrý den , a nějakou soutěž o něco menšího neplánujete ? <repeat> něco kde bude mít šanci i víc lidí s méně přáteli ? <repeat>
````

### Example 25
**True:** `Positive` (29.3%) | **Predicted:** `Neutral` (59.6%)

Confidence interval (top-2 probs): [29.3%, 59.6%] | Gap: 30.3%

````
dorazili mi čepice a penály pro děti , dostanou je k mikuláši , tak douvám , že je nadchnou tak jako mě. m
````

### Example 26
**True:** `Neutral` (45.8%) | **Predicted:** `Negative` (50.2%)

Confidence interval (top-2 probs): [45.8%, 50.2%] | Gap: 4.5%

````
tak je fakt ze ja ji využívam jen na vyučtovani většinou a co se týče smsek o sdosažení limitu mi chodej tak tezko rict
````

### Example 27
**True:** `Neutral` (44.1%) | **Predicted:** `Negative` (53.2%)

Confidence interval (top-2 probs): [44.1%, 53.2%] | Gap: 9.1%

````
kočky , fuj já radši pejsky
````

### Example 28
**True:** `Neutral` (48.2%) | **Predicted:** `Negative` (49.0%)

Confidence interval (top-2 probs): [48.2%, 49.0%] | Gap: 0.8%

````
ne , stále ta stejná jména
````

### Example 29
**True:** `Negative` (42.7%) | **Predicted:** `Neutral` (52.1%)

Confidence interval (top-2 probs): [42.7%, 52.1%] | Gap: 9.5%

````
kačenka kačenková nováková : já musím být vostrá když lžou
````

### Example 30
**True:** `Positive` (3.5%) | **Predicted:** `Neutral` (53.7%)

Confidence interval (top-2 probs): [42.8%, 53.7%] | Gap: 10.9%

````
opravdu? to mi spadl kámen ze srdce , snad to bude tak jak říkáte . <repeat> děkuji.
````

### Example 31
**True:** `Neutral` (17.4%) | **Predicted:** `Positive` (78.1%)

Confidence interval (top-2 probs): [17.4%, 78.1%] | Gap: 60.7%

````
ja prosííím
````

### Example 32
**True:** `Negative` (19.0%) | **Predicted:** `Neutral` (71.2%)

Confidence interval (top-2 probs): [18.9%, 71.2%] | Gap: 52.2%

````
laskavě si to papouškování strčte někam!
````

### Example 33
**True:** `Neutral` (39.2%) | **Predicted:** `Negative` (57.7%)

Confidence interval (top-2 probs): [39.2%, 57.7%] | Gap: 18.5%

````
nejde mi o mobilní net . <repeat> já chci levné volání a to je se slevou 75 % . <repeat>
````

### Example 34
**True:** `Negative` (20.3%) | **Predicted:** `Neutral` (68.4%)

Confidence interval (top-2 probs): [20.3%, 68.4%] | Gap: 48.0%

````
ja sem to mel take a je to docela male nato jak to vypada na obrazku a stoji 75kč lol
````

### Example 35
**True:** `Negative` (40.5%) | **Predicted:** `Neutral` (49.5%)

Confidence interval (top-2 probs): [40.5%, 49.5%] | Gap: 8.9%

````
pěkne hnusnej : d
````

### Example 36
**True:** `Positive` (11.6%) | **Predicted:** `Neutral` (69.2%)

Confidence interval (top-2 probs): [19.1%, 69.2%] | Gap: 50.1%

````
jj , dobré je máte , sice jsem to jedl studené , protože byly nestíhačky , ale good : d : d : d
````

### Example 37
**True:** `Negative` (48.0%) | **Predicted:** `Neutral` (49.1%)

Confidence interval (top-2 probs): [48.0%, 49.1%] | Gap: 1.1%

````
to mě taky. jedinou smsku se mi podařilo odeslat v době , kdy mi na pouhou minutu naskočila brána a dotyčná čeká na druhou část smsky. marně.
````

### Example 38
**True:** `Neutral` (34.1%) | **Predicted:** `Positive` (60.3%)

Confidence interval (top-2 probs): [34.1%, 60.3%] | Gap: 26.2%

````
: d : d : d : d a zrovna v sobotu se urcite stavím . <repeat> : d
````

### Example 39
**True:** `Neutral` (25.8%) | **Predicted:** `Positive` (69.5%)

Confidence interval (top-2 probs): [25.8%, 69.5%] | Gap: 43.7%

````
mám všechny : )
````

### Example 40
**True:** `Negative` (4.9%) | **Predicted:** `Positive` (76.1%)

Confidence interval (top-2 probs): [19.0%, 76.1%] | Gap: 57.1%

````
je mi lito , zkusenosti rikaji ze neváží.
````

### Example 41
**True:** `Negative` (19.0%) | **Predicted:** `Neutral` (74.4%)

Confidence interval (top-2 probs): [18.9%, 74.4%] | Gap: 55.5%

````
mohla byt aspon zadara
````

### Example 42
**True:** `Neutral` (18.0%) | **Predicted:** `Positive` (77.8%)

Confidence interval (top-2 probs): [18.0%, 77.8%] | Gap: 59.9%

````
jen si hezky zabesídkujte , práce ještě bude habakuk : )
````

### Example 43
**True:** `Negative` (27.1%) | **Predicted:** `Neutral` (68.4%)

Confidence interval (top-2 probs): [27.1%, 68.5%] | Gap: 41.4%

````
přišel jsem 26. června v úterý . <repeat> jak je psáno na vašich stránkách . <repeat> a nic o.o
````

### Example 44
**True:** `Negative` (30.5%) | **Predicted:** `Neutral` (63.6%)

Confidence interval (top-2 probs): [30.5%, 63.6%] | Gap: 33.1%

````
kubajs šindelář : : d já tě alespoň nazývám celým jménem : ) a nebuď drzý na jednom pískovišti jsme spolu bábovky nedělali
````

### Example 45
**True:** `Negative` (45.7%) | **Predicted:** `Neutral` (51.1%)

Confidence interval (top-2 probs): [45.7%, 51.0%] | Gap: 5.3%

````
každopádně má ode dneška vodafone co žehlit . <repeat>
````

### Example 46
**True:** `Neutral` (36.3%) | **Predicted:** `Negative` (60.8%)

Confidence interval (top-2 probs): [36.3%, 60.8%] | Gap: 24.5%

````
prosím pěkně , proč nefrčí web? chci změnit tarif a doufám , že jsem si in-kartu nepořizoval zbytečně. <url>
````

### Example 47
**True:** `Neutral` (36.8%) | **Predicted:** `Negative` (60.0%)

Confidence interval (top-2 probs): [36.8%, 60.0%] | Gap: 23.2%

````
mám s3 z volného prodeje , a jb taky nemám. a ani mně to netrápí.
````

### Example 48
**True:** `Neutral` (36.0%) | **Predicted:** `Positive` (58.7%)

Confidence interval (top-2 probs): [36.0%, 58.7%] | Gap: 22.7%

````
už mám objednáno =)
````

### Example 49
**True:** `Negative` (45.3%) | **Predicted:** `Neutral` (51.7%)

Confidence interval (top-2 probs): [45.3%, 51.7%] | Gap: 6.4%

````
já taky objednala jsem asi před měs.a taky nic a vše bylo správné
````

### Example 50
**True:** `Negative` (4.5%) | **Predicted:** `Positive` (74.0%)

Confidence interval (top-2 probs): [21.5%, 74.0%] | Gap: 52.5%

````
taky jsem se nachytala : -) minuly mesic jsem platila skoro 2000 , - kvuli zmenam : -)
````

