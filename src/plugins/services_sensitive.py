# coding=utf-8 
'''
Created on Sep 15, 2014

@author: ivan
'''

from forbidden_words import ForbiddenWords

phrases=["Best Efforts",
"Best Endeavors",
"Best Practices",
"Technology Transfer",
"Knowledge Transfer",
"Knowledge Sharing",
"Guarantee",
"Warrant",
"Partner",
"Partnership",
"Will meet your needs",
"Will meet your requirements",
"Will meet your expectations",
"Will exceed your needs",
"Will exceed your requirements",
"Will exceed your expectations",
"Satisfy",
"to customer.?s satisfaction",
"successfully",
"subject to customer.?s satisfaction",
"nejlepší úsilí",
"Technologický převod",
"Garantovat",
"Partner",
"Vynaložíme veškeré úsílí na to, abychom",

"beste Leistungen",
"nach besten Kräften",
"Technologietransfer",
"Wissensvermittlung",
"Wissenstransfer",
"Wissensaustausch",
"Garantie",
"Gewährleistung",
"Partner",
"Partnerschaft",
"Bedürfnisse erfüllen",
"Anforderungen erfüllen",
"Erwartungen erfüllen",
"Bedürfnisse überschreiten",
"Anforderungen überschreiten",
"Erwartungen überschreiten",
"erfüllen",
"Kundenzufriedenheit",
"abhängig von der Kundenzufriedenheit",
"vorbehaltlich der Kundenzufriedenheit",

"Los mejores Esfuerzos",
"Los mejores Empeños",
"Buenas Practicas",
"Traspaso",
"transferencia de tecnologia",
"traspaso de conocimientos",
"intercambio de conocimientos",
"garantía",
"garantizar",
"socio",
"asociación",
"Vamos a cumplir con sus necesidades",     
"Vamos a superar sus necesidades",
"Vamos a cumplir con sus requisitos",    
"Vamos a superar sus requisitos",
"Vamos a cumplir con sus expectativas",
"Vamos a superar sus expectativas",
"Satisfacer",
"para la satisfacción del cliente",
"exitosamente",
"sujeto a la satisfacción del cliente",

"legnagyobb erőfeszítés",
"legjobb törekvések",
"legjobb gyakorlatok",
"technológia átruházása",
"tudás átadása",
"tapasztalat megosztása",
"jótállás",
"szavatosság",
"társ",
"társulás",
"Partnerség",
"megfelelnek az ön igényeit",
"megfelelnek az ön elvárásait",
"megfelelnek az ön várakozásait",
"meghaladják az ön igényeit",
"meghaladják az ön elvárásait",
"meghaladják az ön várakozásait",
"eleget tesz",
"az ügyfél elégedettségére",
"sikeresen",
"az ügyfél elégedettségétől függően",

"Migliori effort",
"migliore impegno",
"migliori pratiche",
"Trasferimento Tecnologico",
"Trasferimento di conoscenze",
"Condivisione di conoscenze",
"Garanzia",
"Associazione",
"Sodisfare le vostre esigenze",
"Sodisfare le vostre richieste",
"Sodisfare le vostre aspettative",
"superare le vostre esigenze",
"superare le vostre richieste",
"superare le vostre aspettative",
"soddisfare",
"alla soddisfazione del cliente",
"con successo",
"sottomesso alla soddisfazione del cliente",
"soggetto alla soddisfazione del cliente",

"Najlepsze praktyki",
"Najlepsze starania",
"Najlepsze wysilki",
"Transfer technologii",
"Transfer wiedzy się wiedzą",
"Transfer dzielenie się wiedzą",
"upoważnienie",
"pełnomocnictwo",
"poręczenie",
"gwarancja",
"partnerstwo",
"współpraca",
"spółka",
"Spełni",
"przekroczy potrzeby",
"wymagania",
"oczekiwania Klienta",  
"Zadowoli",
"dla zadowolenia Klienta",
"Skutecznie",

"melhores esforços",
"transferência de tecnologia",
"garantir",
"sócio",
"Vai exceder as expectativas",
"Vai corresponder as expectativas",
"cumprir",
"satisfação do cliente",

"cele mai mari eforturi",
"toate eforturile",
"cele mai bune practici",
"transfer de tehnologie",
"transfer de cunoştinţe",
"schimb de cunoştinţe",
"garanţie",
"chezăşie",
"Partener",
"parteneriat",
"Va satisface nevoile dumneavoastra",
"va depăși nevoile dumneavoastră",
"depăși cerințele dumneavoastră",
"depăși așteptările dumneavoastră",
"Va satisface cerințele dumneavoastră",
"Va satisface așteptările dumneavoastră",
"Satisface",
"pentru satisfacția clientului",
"cu succes",
"depinde de satisfacţia clientului",
"Out of the box",

"bästa ansträngningar",
"bästa bemödande",
"bästa metoder",
"tekniköverföring",
"kunskapsöverföring",
"kunskapsspridning",
"garantera",
"försäkra",
"kompanjon",
"kompanjonskap",
"samverkan",
"kommer att tillgodose dina behover",
"kommer att överstiga dina behover",
"kommer att tillgodose dina krav",
"kommer att överstiga dina krav",
"kommer att tillgodose dina förväntningar",
"kommer att överstiga dina förväntningar",
"tillfredsställa",
"för kundens nöjdhet",
"framgångsrikt",
"utsatta för kundens nöjdhet",

"En iyi çabalar",
"En iyi gayretler",
"En iyi uygulamalar",
"En iyi uğraşlar",
"Teknoloji Transferi",
"Bilgi Transferi",
"Bilgi Paylaşımı",
"Garanti",
"Kefil",
"Ihtiyaçlarınızı karşılayacağız",
"Ihtiyaçlarınızı aşacağız",
"Taleplerinizi karşılayacağız",
"Taleplerinizi  aşacağız",
"Beklentilerinizi karşılayacağız",
"Gereksinimlerinizi karşılayacağız",
"Gereksinimlerinizi aşacağız",
"Beklentilerinizi aşacağız",
"Tatmin",
"müşteri memnuniyeti",
"başarıyla",
"müşterinin konu memnuniyeti",

"Oracle fera ses meilleurs efforts",
"Oracle interviendra dans les meilleurs délais",
"transfert de technologie",
"transfert technologique",
"transfert des connaissances",
"transfert de savoir",
"transmission de savoir",
"garantie",
"partenaire",
"partenariat",
"répondre le mieux à vos besoins",
"répondre à vos besoins",
"devancer vos besoins",
"respecter vos exigences",
"répondre à vos exigences",
"satisfaire à vos exigences",
"répondre à vos attentes",
"Oracle satisfera à vos besoins",
"Oracle satisfera à vos attentes",
"Oracle répondra à vos besoins",
"Oracle répondra à vos attentes",

"κάθε δυνατή προσπάθεια",
"βέλτιστες πρακτικές",
"μεταφορά τεχνολογίας",
"μεταφορά γνώσης, τεγνογνωσίας",    
"ανταλλαγή γνώσης, τεγνογνωσίας",
"εγγύηση",
"δέσμευση",
"εταίρος",    
"συνεταίρος",
"συνεταιρισμός",   
"Θα ικανοποιεί τις ανάγκες σας",
"Θα υπερβαίνει τις ανάγκες σας",
"θα ικανοποιεί τις απαιτήσεις σας",
"θα υπερβαίνει τις απαιτήσεις σας",
"θα ικανοποιεί τις προσδοκίες σας",
"θα υπερβαίνει τις προσδοκίες σας",

 
"beste inspanningen or beste praktijken",
"technologieoverdracht",
"kennisoverdracht",
"kennisdeling",
"garantie",
"garanderen",
"vennoot",
"vennootschap",
"Zal voldoen aan",
"overtreffen uw behoeften",
"Zal voldoen aan",
"overtreffen uw wensen",
"Zal voldoen aan",
"uw verwachtingen overtreffen",
"bevredigen",
"klanttevredenheid",
"met succes",
"met geslaagd",
"onderhevig aan klanttevredenheid",

"наилучшим образом",
"лучшая практика",
"лучшие способы",
"передовая практика",
"стандарты передовой практики",
"передача технологии",
"передача научных технологий",
"передача технологий",
"передача знаний",
"передача знаний и информации",
"обмен знаниями",
"давать гарантию",
"ручаться",
"гарантировать",
"давать поручительство",
"обещать",
"партнёрские отношения",
"партнёрство",
"удовлетворять потребность",
"соответствовать потребностям",
"удовлетворять запросы",
"потребности",
"превзойти ожидания", 
]

def create_instance():
    i= ForbiddenWords(phrases)
    i.change_name('Services Phrases To Avoid')
    i.set_categories(['Services'])
    i.change_help("""<B>Services Phrases To Avoid</B><BR>
<BR>
Identified phrases should  be avoided in services ODs.
""")
    return i
