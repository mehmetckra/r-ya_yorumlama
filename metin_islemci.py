from transformers import BertTokenizer, BertForSequenceClassification, BertModel
import torch
import torch.nn.functional as F
import numpy as np

# Duygu durumları ve karşılık gelen yorumlar
DUYGU_YORUMLARI = {
    'mutlu': [
        "Rüyanızda mutlu olmanız, hayatınızdaki olumlu gelişmelerin habercisidir.",
        "Mutluluk dolu bir rüya, yakın zamanda güzel haberler alacağınızı gösterir.",
        "Rüyada mutlu olmak, iç huzurunuzun ve başarılarınızın işaretidir."
    ],
    'üzgün': [
        "Rüyanızda üzgün olmanız, içinizdeki duyguları dışa vurma ihtiyacını gösterir.",
        "Üzüntülü bir rüya, hayatınızda çözümlenmemiş durumların varlığına işaret eder.",
        "Rüyada üzüntü, yakında güzel gelişmelerle son bulacak bir dönemin işaretidir."
    ],
    'sinirli': [
        "Rüyada sinirli olmak, bastırılmış duygularınızın açığa çıkma isteğini gösterir.",
        "Öfke dolu bir rüya, çevrenizde değiştirilmesi gereken durumların varlığına işaret eder.",
        "Rüyada sinir, enerjinizi daha yapıcı yönlere kanalize etme ihtiyacınızı gösterir."
    ],
    'ağlayan': [
        "Rüyada ağlamak, duygusal bir arınma sürecinde olduğunuzu gösterir.",
        "Ağlama içeren bir rüya, içsel bir iyileşme sürecinin başlangıcına işaret eder.",
        "Rüyada ağlamak, yakında ferahlayacağınız ve rahatlayacağınız bir döneme işaret eder."
    ],
    'korkmuş': [
        "Rüyada korkmuş hissetmek, bilinçaltınızda yüzleşmekten kaçındığınız bir durum olduğunu gösterir.",
        "Korku dolu bir rüya, hayatınızda sizi endişelendiren bir konunun varlığına işaret eder.",
        "Rüyada korkmak, güvende olma isteğinizi ve içsel korunma ihtiyacınızı temsil eder."
    ],
    'heyecanlı': [
        "Rüyada heyecanlanmak, hayatınıza enerji katan yeniliklerin yolda olduğuna işaret eder.",
        "Heyecan dolu bir rüya, merak ve motivasyonunuzun artacağını gösterir.",
        "Rüyada heyecanlanmak, beklediğiniz bir olayın gerçekleşeceğinin habercisidir."
    ],
    'şaşkın': [
        "Rüyada şaşkın hissetmek, hayatınızda beklenmedik değişikliklerin olabileceğini gösterir.",
        "Şaşkınlık dolu bir rüya, yeni bilgiler öğrenme ve keşif dönemine işaret eder.",
        "Rüyada şaşırmak, olaylara karşı açık fikirli olmanız gerektiğini hatırlatır."
    ],
    'huzurlu': [
        "Rüyada huzur içinde olmak, içsel dengelerinizi sağladığınızı ve mutlu bir döneme girdiğinizi gösterir.",
        "Huzur dolu bir rüya, hayatınızda dinginlik ve uyumun hakim olacağına işaret eder.",
        "Rüyada huzurlu hissetmek, olumlu enerjilerin sizi çevrelediğinin habercisidir."
    ],
    'endişeli': [
        "Rüyada endişelenmek, bilinçaltınızdaki kararsızlıkların ve çözümlenmemiş meselelerin işaretidir.",
        "Endişe dolu bir rüya, üzerinizde baskı oluşturan bir durumun farkında olduğunuzu gösterir.",
        "Rüyada endişeli hissetmek, sorunları ele alma ve çözüme kavuşturma ihtiyacınızı temsil eder."
    ],
    'rahatlamış': [
        "Rüyada rahatlamak, üzerinizdeki baskılardan kurtulacağınız anlamına gelir.",
        "Rahatlama hissi içeren bir rüya, huzurlu ve tatmin edici bir sürecin başladığını gösterir.",
        "Rüyada rahatlamış hissetmek, içsel dengenizin yerine geldiğini ve kendinize güveninizin arttığını simgeler."
    ],
    'yalnız': [
        "Rüyada yalnız hissetmek, içsel keşif ve kendinizle yüzleşme sürecine girdiğinizi gösterir.",
        "Yalnızlık dolu bir rüya, bağımsızlık ve özgüven kazanma ihtiyacınızı simgeler.",
        "Rüyada yalnız kalmak, kendinizi daha iyi tanımanız gerektiğini hatırlatır."
    ],
    'neşeli': [
        "Rüyada neşeli hissetmek, hayatınızda keyifli ve mutlu anlar yaşayacağınızı gösterir.",
        "Neşe dolu bir rüya, enerjinizi yükseltecek olumlu gelişmelerin habercisidir.",
        "Rüyada neşeli olmak, çevrenizle güçlü bağlar kurduğunuzu simgeler."
    ],
    'pişman': [
        "Rüyada pişmanlık hissetmek, geçmişte yaptığınız bir hatadan ders çıkardığınızı gösterir.",
        "Pişmanlık dolu bir rüya, içsel hesaplaşmalarınızın farkında olmanız gerektiğini gösterir.",
        "Rüyada pişman olmak, yeni fırsatlarla hatalarınızı telafi etme şansınızın olduğuna işaret eder."
    ],
    'gururlu': [
        "Rüyada gurur duymak, başarılarınızın takdir edildiğini ve özsaygınızın arttığını gösterir.",
        "Gurur dolu bir rüya, kişisel hedeflerinize ulaşma yolunda ilerlediğinizi simgeler.",
        "Rüyada gururlu hissetmek, çevreniz tarafından saygı ve sevgi gördüğünüzü işaret eder."
    ],
    'kararsız': [
        "Rüyada kararsız hissetmek, hayatınızdaki belirsizlikleri ve netleşmemiş kararları simgeler.",
        "Kararsızlık dolu bir rüya, birden fazla seçenek arasında kalacağınızı işaret eder.",
        "Rüyada kararsız olmak, içsel dengenizi bulma ihtiyacınızı temsil eder."
    ]
}

# Doğa olayları sözlüğü ekleniyor
DOGA_OLAYI_YORUMLARI = {
    'yağmur': [
        "Rüyada yağmur görmek, bereket ve bolluk işaretidir.",
        "Yağmurlu bir rüya, duygusal arınma ve yenilenme sürecine girdiğinizi gösterir.",
        "Rüyada yağmur, yakın zamanda alacağınız güzel haberlerin işaretidir."
    ],
    'kar': [
        "Rüyada kar görmek, temiz bir başlangıç yapacağınıza işaret eder.",
        "Karlı bir rüya, hayatınızdaki zorlukların geçici olduğunu gösterir.",
        "Rüyada kar yağışı, iç huzurunuzun artacağının habercisidir."
    ],
    'fırtına': [
        "Rüyada fırtına görmek, hayatınızdaki değişimlere hazır olmanız gerektiğini gösterir.",
        "Fırtınalı bir rüya, zorlu ama gelişiminiz için gerekli bir dönemden geçeceğinize işaret eder.",
        "Rüyada fırtına, yaklaşan güçlü değişimlerin habercisidir."
    ],
    'güneş': [
        "Rüyada güneş görmek, aydınlık bir geleceğe işaret eder.",
        "Güneşli bir rüya, başarı ve mutluluğun yakın olduğunu gösterir.",
        "Rüyada parlak güneş, hedeflerinize ulaşacağınızın işaretidir."
    ],
    'ay': [
        "Rüyada ay görmek, duygusal farkındalığınızın artacağını gösterir.",
        "Ay'ı gördüğünüz rüya, içsel yolculuğunuzun başladığına işaret eder.",
        "Rüyada parlak ay, sezgilerinizin güçleneceğini simgeler."
    ],
    'yıldız': [
        "Rüyada yıldız görmek, şansınızın açılacağına işaret eder.",
        "Yıldızlı bir rüya, dileklerinizin gerçekleşeceğini gösterir.",
        "Rüyada parlak yıldızlar, başarı ve şöhret kazanacağınızı simgeler."
    ],
    'gökkuşağı': [
        "Rüyada gökkuşağı görmek, güzel günlerin yakın olduğunu gösterir.",
        "Gökkuşağı içeren bir rüya, zorlu zamanların sona ereceğine işaret eder.",
        "Rüyada gökkuşağı, umut ve mutluluğun habercisidir."
    ],
    'sel': [
        "Rüyada sel görmek, duygusal bir taşkınlık yaşayacağınıza işaret eder.",
        "Sel gören bir rüya, hayatınızdaki engellerin kalkacağını gösterir.",
        "Rüyada sel suları, zorlu duyguların akıp gideceğini simgeler."
    ],
    'deprem': [
        "Rüyada deprem görmek, hayatınızda köklü değişimler olacağını gösterir.",
        "Deprem içeren bir rüya, yeni başlangıçlar yapacağınıza işaret eder.",
        "Rüyada deprem, eski düzeninizin değişeceğinin habercisidir."
    ],
    'sis': [
        "Rüyada sis görmek, belirsizliklerin yakında aydınlanacağını gösterir.",
        "Sisli bir rüya, yakında netlik kazanacak durumların varlığına işaret eder.",
        "Rüyada yoğun sis, gizli gerçeklerin ortaya çıkacağını simgeler."
    ]
}

# Hayvanlarla ilgili yorumlar ekleniyor
HAYVAN_YORUMLARI = {
    'kuş': [
        "Rüyada kuş görmek, özgürlüğe kavuşacağınızın ve yeni fırsatlar yakalayacağınızın işaretidir.",
        "Kuş görülen rüya, hayallerinizin gerçekleşeceğini ve yüksek hedeflere ulaşacağınızı gösterir.",
        "Rüyada kuş, size gelecek güzel haberlerin müjdecisidir."
    ],
    'kedi': [
        "Rüyada kedi görmek, bağımsızlık ve özgürlük duygularınızın güçleneceğini gösterir.",
        "Kedi görülen rüya, sezgilerinizin güçleneceğine ve gizli gerçekleri keşfedeceğinize işaret eder.",
        "Rüyada kedi, çevrenizdeki ikiyüzlülüklere karşı dikkatli olmanız gerektiğini hatırlatır."
    ],
    'köpek': [
        "Rüyada köpek görmek, sadık dostluklar kuracağınızın ve güvenilir insanlarla tanışacağınızın işaretidir.",
        "Köpek görülen rüya, koruma ve güven duygularınızın güçleneceğini gösterir.",
        "Rüyada köpek, size sadık kalacak yeni dostlar edineceğinizi simgeler."
    ],
    'at': [
        "Rüyada at görmek, güç ve başarıya ulaşacağınızın işaretidir.",
        "At görülen rüya, kariyerinizde hızlı ilerleyeceğinizi ve hedeflerinize ulaşacağınızı gösterir.",
        "Rüyada at, özgürlük ve güç kazanacağınızı simgeler."
    ],
    'yılan': [
        "Rüyada yılan görmek, gizli düşmanlarınıza karşı uyanık olmanız gerektiğini gösterir.",
        "Yılan görülen rüya, yaşamınızda bir değişim ve yenilenme sürecine gireceğinizi işaret eder.",
        "Rüyada yılan, çevrenizdeki tehlikelere karşı dikkatli olmanız gerektiğini hatırlatır."
    ],
    'kuzu': [
        "Rüyada kuzu görmek, masumiyet ve saflığın simgesidir, güzel günlerin yakın olduğunu gösterir.",
        "Kuzu görülen rüya, huzur dolu günlerin yaklaştığına işaret eder.",
        "Rüyada kuzu, hayatınıza gelecek bereketin habercisidir."
    ],
    'balık': [
        "Rüyada balık görmek, maddi kazanç ve bereket işaretidir.",
        "Balık görülen rüya, duygusal zenginlik ve bolluk yaşayacağınızı gösterir.",
        "Rüyada balık, yakında alacağınız güzel haberlerin simgesidir."
    ],
    'kartal': [
        "Rüyada kartal görmek, yüksek mevkilere geleceğinizin ve başarı kazanacağınızın işaretidir.",
        "Kartal görülen rüya, hedeflerinize ulaşacağınızı ve güç kazanacağınızı gösterir.",
        "Rüyada kartal, liderlik vasıflarınızın güçleneceğini simgeler."
    ]
}

# Tanıdık kişiler için yorumlar ekleniyor
TANIDIK_YORUMLARI = {
    'anne': [
        "Rüyada annenizi görmek, yakında güzel haberler alacağınızı ve sevdiklerinizle mutlu günler geçireceğinizi gösterir.",
        "Annenizle ilgili rüya, ailenizle ilgili olumlu gelişmelerin habercisidir.",
        "Rüyada annenizi görmek, şefkat ve merhamet duygularınızın artacağına işaret eder."
    ],
    'baba': [
        "Rüyada babanızı görmek, iş hayatınızda başarı ve ilerleme kaydedeceğinizi gösterir.",
        "Babanızla ilgili rüya, hayatınızda güven ve istikrarın artacağına işaret eder.",
        "Rüyada babanızı görmek, önemli kararlar alırken doğru yolda olduğunuzu simgeler."
    ],
    'kardeş': [
        "Rüyada kardeşinizi görmek, aile bağlarınızın güçleneceğini ve destekçilerinizin artacağını gösterir.",
        "Kardeşinizle ilgili rüya, yakın çevrenizle ilişkilerinizin iyileşeceğine işaret eder.",
        "Rüyada kardeşinizi görmek, güvenebileceğiniz kişilerle tanışacağınızı simgeler."
    ],
    'arkadaş': [
        "Rüyada arkadaşınızı görmek, sosyal çevrenizin genişleyeceğini ve yeni dostluklar kuracağınızı gösterir.",
        "Arkadaşınızla ilgili rüya, güzel bir sürprizle karşılaşacağınıza işaret eder.",
        "Rüyada arkadaşınızı görmek, paylaşacağınız güzel anların habercisidir."
    ],
    'sevgili': [
        "Rüyada sevgilinizi görmek, duygusal hayatınızda olumlu gelişmeler yaşanacağını gösterir.",
        "Sevgilinizle ilgili rüya, ilişkinizin güçleneceğine ve mutlu günler geçireceğinize işaret eder.",
        "Rüyada sevgilinizi görmek, aşk hayatınızda yeni bir dönemin başlayacağını simgeler."
    ],
    'eş': [
        "Rüyada eşinizi görmek, evliliğinizde huzur ve mutluluğun artacağını gösterir.",
        "Eşinizle ilgili rüya, aile yaşamınızda güzel gelişmeler olacağına işaret eder.",
        "Rüyada eşinizi görmek, ortak hedeflerinize ulaşacağınızı simgeler."
    ]
}

# Zaman ve Döngü yorumları ekleniyor
ZAMAN_DONGU_YORUMLARI = {
    'tekrar': [
        "Tekrarlayan rüyalar görmeniz, çözülmemiş bir durumla yüzleşmeniz gerektiğini gösterir.",
        "Aynı rüyayı tekrar görmeniz, bilinçaltınızın size önemli bir mesaj verdiğine işaret eder.",
        "Rüyanın tekrarlanması, hayatınızda değiştirilmesi gereken bir durumun varlığını simgeler."
    ],
    'kabus': [
        "Kabus görmeniz, bastırılmış korku ve endişelerinizle yüzleşme zamanının geldiğini gösterir.",
        "Kötü rüyalar, iç dünyanızda çözülmeyi bekleyen duygusal yüklere işaret eder.",
        "Kabus niteliğindeki rüyalar, hayatınızdaki stres kaynaklarını ele almanız gerektiğini hatırlatır."
    ],
    'lucid': [
        "Lucid rüya görmeniz, kendi hayatınız üzerinde daha fazla kontrol sahibi olma isteğinizi gösterir.",
        "Rüyanızın farkında olmanız, öz farkındalığınızın ve içgörünüzün güçlendiğine işaret eder.",
        "Bilinçli rüya deneyimi, kişisel gelişiminizde önemli bir aşamaya geldiğinizi simgeler."
    ]
}

# Global değişkenler
tokenizer = None
model = None

try:
    model_name = "dbmdz/bert-base-turkish-cased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    model.eval()
except Exception as e:
    print(f"Model/Tokenizer yüklenirken hata oluştu: {e}")

def duygu_tespit_et(metin):
    duygu_anahtar_kelimeler = {
        'mutlu': ['mutlu', 'sevinçli', 'neşeli', 'keyifli', 'güzel', 'harika', 'sevindim'],
        'üzgün': ['üzgün', 'kederli', 'mutsuz', 'hüzünlü', 'kötü', 'mahzun'],
        'sinirli': ['sinirli', 'öfkeli', 'kızgın', 'hiddetli', 'agresif', 'sinirlendim'],
        'ağlayan': ['ağla', 'ağlıyor', 'gözyaşı', 'hıçkır', 'ağlayan', 'ağladım'],
        'korkmuş': ['korku', 'korkmuş', 'korktum', 'ürktüm', 'dehşet', 'tedirgin'],
        'heyecanlı': ['heyecan', 'heyecanlı', 'coşkulu', 'coştum', 'heyecanlandım'],
        'şaşkın': [
            'şaşır', 'şaşkın', 'şaşırdım', 'şaşırmış', 'şaşırarak',
            'hayret', 'şok', 'şaşırttı', 'şaşırtıcı', 'hayrete düş',
            'şaşırınca', 'şaşırmak', 'şaşırıp', 'şaşırdığım',
            'şaşırmıştım', 'şaşıracak', 'inanamadım', 'beklemiyordum'
        ],
        'huzurlu': ['huzur', 'huzurlu', 'sakin', 'dingin', 'rahat', 'huzurluydum'],
        'endişeli': ['endişe', 'endişeli', 'kaygılı', 'tedirgin', 'endişelendim'],
        'rahatlamış': ['rahatlama', 'rahatladım', 'gevşedim', 'ferahladım', 'hafifledim'],
        'yalnız': ['yalnız', 'yalnızlık', 'tek başıma', 'kimsesiz', 'yalnızdım'],
        'neşeli': ['neşe', 'neşeli', 'eğlenceli', 'eğlendim', 'kahkaha'],
        'pişman': ['pişman', 'pişmanlık', 'keşke', 'vicdan', 'pişmanım'],
        'gururlu': ['gurur', 'gururlu', 'onurlu', 'başarılı', 'gururlandım'],
        'kararsız': ['kararsız', 'kararsızlık', 'tereddüt', 'şüpheli', 'kararsızdım']
    }
    
    metin = metin.lower().strip()
    print(f"Analiz edilen metin: {metin}")  # Debug için
    
    en_yuksek_eslesme = 0
    tespit_edilen_duygu = None
    eslesme_detaylari = {}
    
    for duygu, kelimeler in duygu_anahtar_kelimeler.items():
        eslesme_sayisi = 0
        bulunan_kelimeler = []
        
        for kelime in kelimeler:
            for metin_kelime in metin.split():
                if kelime in metin_kelime:
                    eslesme_sayisi += 1
                    bulunan_kelimeler.append(kelime)
                    break
        
        eslesme_detaylari[duygu] = {
            'skor': eslesme_sayisi,
            'bulunan': bulunan_kelimeler
        }
        
        if eslesme_sayisi > en_yuksek_eslesme:
            en_yuksek_eslesme = eslesme_sayisi
            tespit_edilen_duygu = duygu
    
    print(f"Eşleşme detayları: {eslesme_detaylari}")  # Debug için
    print(f"Tespit edilen duygu: {tespit_edilen_duygu}")  # Debug için
    
    return tespit_edilen_duygu

def doga_olayi_tespit_et(metin):
    doga_anahtar_kelimeler = {
        'yağmur': ['yağmur', 'yağış', 'yağdı', 'yağıyor'],
        'kar': ['kar', 'karla', 'karlı', 'kar yağışı', 'kar yağıyor'],
        'fırtına': ['fırtına', 'kasırga', 'bora', 'tayfun'],
        'güneş': ['güneş', 'güneşli', 'güneşin', 'parlak güneş'],
        'ay': ['ay', 'dolunay', 'hilal', 'mehtap'],
        'yıldız': ['yıldız', 'yıldızlar', 'yıldızlı'],
        'gökkuşağı': ['gökkuşağı', 'gökkuşağını'],
        'sel': ['sel', 'sel suyu', 'sel baskını'],
        'deprem': ['deprem', 'sarsıntı', 'zelzele'],
        'sis': ['sis', 'sisli', 'puslu', 'bulanık']
    }
    
    metin = metin.lower().strip()
    tespit_edilen_olaylar = []
    
    for olay, kelimeler in doga_anahtar_kelimeler.items():
        if any(kelime in metin for kelime in kelimeler):
            tespit_edilen_olaylar.append(olay)
    
    return tespit_edilen_olaylar

def hayvan_tespit_et(metin):
    hayvan_anahtar_kelimeler = {
        'kuş': ['kuş', 'kuşlar', 'güvercin', 'serçe', 'kanarya'],
        'kedi': ['kedi', 'kediler', 'kedicik', 'miyav', 'tekir'],
        'köpek': ['köpek', 'köpekler', 'havlayan', 'köpeğim'],
        'at': ['at', 'atlar', 'beyaz at', 'kır at', 'yağız at'],
        'yılan': ['yılan', 'yılanlar', 'kobra', 'piton'],
        'kuzu': ['kuzu', 'kuzular', 'kuzucuk', 'kuzu gibi'],
        'balık': ['balık', 'balıklar', 'balıkçı', 'olta'],
        'kartal': ['kartal', 'kartallar', 'kartala', 'kartal gibi']
    }
    
    metin = metin.lower().strip()
    tespit_edilen_hayvanlar = []
    
    for hayvan, kelimeler in hayvan_anahtar_kelimeler.items():
        if any(kelime in metin for kelime in kelimeler):
            tespit_edilen_hayvanlar.append(hayvan)
    
    return tespit_edilen_hayvanlar

def zaman_dongu_tespit_et(metin):
    zaman_anahtar_kelimeler = {
        'tekrar': [
            'tekrar', 'yine', 'aynı rüya', 'tekrarlayan',
            'sürekli', 'devamlı', 'her zaman', 'hep aynı'
        ],
        'kabus': [
            'kabus', 'kötü rüya', 'korkunç', 'korku dolu',
            'dehşet', 'korkutucu', 'ürkütücü', 'rahatsız edici'
        ],
        'lucid': [
            'lucid', 'farkında', 'bilinçli rüya', 'kontrol',
            'rüyada uyanık', 'rüyamın farkındaydım', 'yönlendirebildim'
        ]
    }
    
    metin = metin.lower().strip()
    tespit_edilen_durumlar = []
    
    for durum, kelimeler in zaman_anahtar_kelimeler.items():
        if any(kelime in metin for kelime in kelimeler):
            tespit_edilen_durumlar.append(durum)
    
    return tespit_edilen_durumlar

def tanidik_tespit_et(metin):
    tanidik_anahtar_kelimeler = {
        'anne': ['anne', 'annem', 'annemi', 'annemle', 'valide'],
        'baba': ['baba', 'babam', 'babamı', 'babamla', 'peder'],
        'kardeş': ['kardeş', 'kardeşim', 'abla', 'abi', 'ablam', 'abim', 'kardeşimle'],
        'arkadaş': ['arkadaş', 'arkadaşım', 'dostum', 'arkadaşımı', 'arkadaşımla'],
        'sevgili': ['sevgili', 'sevgilim', 'aşkım', 'nişanlı', 'nişanlım'],
        'eş': ['eş', 'eşim', 'karım', 'kocam', 'hanım', 'beyim']
    }
    
    metin = metin.lower().strip()
    tespit_edilen_kisiler = []
    
    for kisi, kelimeler in tanidik_anahtar_kelimeler.items():
        if any(kelime in metin for kelime in kelimeler):
            tespit_edilen_kisiler.append(kisi)
    
    return tespit_edilen_kisiler

def metin_duzenle(detay_metni_listesi, duygu_metni):
    try:
        if not detay_metni_listesi:
            return "Yorum bulunamadı."

        # Tüm analizleri yap
        tespit_edilen_duygu = duygu_tespit_et(duygu_metni)
        tespit_edilen_olaylar = doga_olayi_tespit_et(duygu_metni)
        tespit_edilen_hayvanlar = hayvan_tespit_et(duygu_metni)
        tespit_edilen_zamanlar = zaman_dongu_tespit_et(duygu_metni)
        tespit_edilen_kisiler = tanidik_tespit_et(duygu_metni)
        
        # Birleşik yorum metni oluştur
        import random
        yorumlar = []
        
        # Ana rüya yorumunu ekle
        birlesik_metin = " ".join(detay_metni_listesi)
        yorumlar.append(f"Rüyanızın genel yorumu şu şekildedir: {birlesik_metin}")
        
        # Duygu yorumu
        if tespit_edilen_duygu and tespit_edilen_duygu in DUYGU_YORUMLARI:
            duygu_yorumu = random.choice(DUYGU_YORUMLARI[tespit_edilen_duygu])
            yorumlar.append(f"Rüyanızda {tespit_edilen_duygu} duygusunu yaşamanız, {duygu_yorumu.lower()}")
        
        # Doğa olayları yorumu
        if tespit_edilen_olaylar:
            for olay in tespit_edilen_olaylar:
                if olay in DOGA_OLAYI_YORUMLARI:
                    olay_yorumu = random.choice(DOGA_OLAYI_YORUMLARI[olay])
                    yorumlar.append(f"Rüyanızda {olay} görmeniz, {olay_yorumu.lower()}")
        
        # Hayvan yorumu
        if tespit_edilen_hayvanlar:
            for hayvan in tespit_edilen_hayvanlar:
                if hayvan in HAYVAN_YORUMLARI:
                    hayvan_yorumu = random.choice(HAYVAN_YORUMLARI[hayvan])
                    yorumlar.append(f"Rüyanızda {hayvan} görmeniz, {hayvan_yorumu.lower()}")
        
        # Tanıdık kişi yorumu
        if tespit_edilen_kisiler:
            for kisi in tespit_edilen_kisiler:
                if kisi in TANIDIK_YORUMLARI:
                    kisi_yorumu = random.choice(TANIDIK_YORUMLARI[kisi])
                    yorumlar.append(f"Rüyanızda {kisi}nizi görmeniz, {kisi_yorumu.lower()}")
        
        # Zaman ve döngü yorumu
        if tespit_edilen_zamanlar:
            for zaman in tespit_edilen_zamanlar:
                if zaman in ZAMAN_DONGU_YORUMLARI:
                    zaman_yorumu = random.choice(ZAMAN_DONGU_YORUMLARI[zaman])
                    yorumlar.append(f"Bu rüyanın {zaman} niteliği, {zaman_yorumu.lower()}")

        # Tüm yorumları birleştir ve paragraflar halinde düzenle
        sonuc = "\n\n".join(yorumlar)
        
        # Özet ve tavsiye ekle
        ozet = """
        
Özet ve Tavsiyeler:
Bu rüya genel olarak hayatınızdaki değişimleri ve iç dünyanızı yansıtmaktadır. 
Rüyanızda görülen semboller ve duygular, bilinçaltınızın size verdiği mesajları içermektedir.
Size tavsiyemiz, bu dönemde iç sesinizi dinlemeniz ve rüyanızda size gösterilen işaretlere dikkat etmenizdir.
Yinede unutmamanızı isteriz ki bu bir rüyadır ve rüya yorumları her zaman gerçeği yansıtmaz.
Lütfen rüya yorumlarına ve fal yorumlarının hayatınızdaki kararlara zarar vermesine izin vermeyin.
Başka bir rüya yorumunda görüşmek üzere!
"""

        return sonuc + ozet

    except Exception as e:
        print(f"Metin düzenleme hatası: {e}")
        return " ".join(detay_metni_listesi)
