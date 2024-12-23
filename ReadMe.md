# Rüya Tabiri Programı

Bu proje, kullanıcıların rüyalarını analiz ederek yorumlayan bir rüya tabiri programıdır. Kullanıcılar rüyalarını yazarak, rüyalarında geçen olaylar, duygular, hayvanlar ve tanıdık kişiler hakkında yorumlar alabilirler.

## Özellikler

- **Rüya Ekleme:** Kullanıcılar yeni rüya yorumları ekleyebilir.
- **Rüya Analizi:** Kullanıcıların yazdığı rüyaları analiz ederek detaylı yorumlar sunar.
- **Duygu Tespiti:** Rüyada hissedilen duyguları tespit eder ve yorumlar.
- **Doğa Olayları Tespiti:** Rüyada geçen doğa olaylarını tespit eder ve yorumlar.
- **Hayvan Tespiti:** Rüyada görülen hayvanları tespit eder ve yorumlar.
- **Tanıdık Kişi Tespiti:** Rüyada görülen tanıdık kişileri tespit eder ve yorumlar.
- **Zaman ve Döngü Tespiti:** Rüyada tekrarlayan olayları ve kabusları tespit eder ve yorumlar.

## Kullanım

1. Projeyi çalıştırmak için aşağıdaki komutu kullanın:
    python arayüz.py dosyasını çalıştırın.
    ```

2. Program açıldığında, rüyanızı yazın ve "YORUMLA" butonuna tıklayın.

3. Rüyanız analiz edildikten sonra, sonuçlar ekranda görüntülenecektir.

4. Eğer veri tabanına yeni bir rüya yorumu eklemek isterseniz sadece python RuyaEkle.py dosyasını çalıştırın.

## Dosya Yapısı

- [`arayüz.py`](arayüz.py): Programın ana arayüzünü oluşturur.
- [`OzelButon.py`](OzelButon.py): Yorumlama butonunun işlevselliğini sağlar.
- [`YorumKutusu.py`](YorumKutusu.py): Yorumların görüntülendiği metin kutusunu oluşturur.
- [`RuyaEkle.py`](RuyaEkle.py): Yeni rüya yorumları eklemek için kullanılan arayüzü sağlar.
- [`metin_islemci.py`](metin_islemci.py): Rüya analizini gerçekleştiren fonksiyonları içerir.
- [`ruyaanlamlari.db`](ruyaanlamlari.db): Rüya yorumlarının saklandığı SQLite veritabanı.

## Gerekli Kütüphaneler

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız olacak:

- `PyQt6`
- `sqlite3`
- `transformers`

Bu kütüphaneleri yüklemek için aşağıdaki komutu kullanabilirsiniz:
```sh
pip install PyQt6 sqlite3 transformers
```

## Makine Öğrenmesi Modeli

Bu projede, Türkçe metin analizi için `dbmdz/bert-base-turkish-cased` modelini kullanıyoruz. Modeli ve tokenizer'ı yüklemek için aşağıdaki adımları izleyin:

```python
pip install transformers

from transformers import BertTokenizer, BertModel

model_name = "dbmdz/bert-base-turkish-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
model.eval()
