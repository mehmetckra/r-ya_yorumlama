from PyQt6.QtWidgets import QPushButton, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt
import sqlite3
from metin_islemci import metin_duzenle  # Import güncellendi

class OzelButon(QPushButton):
    def __init__(self, metin, parent=None, yorum_kutusu=None, text_kutusu=None, progress_bar=None):
        super().__init__(metin, parent)
        self.yorum_kutusu = yorum_kutusu
        self.text_kutusu = text_kutusu
        self.progress_bar = progress_bar
        self.progress_timer = QTimer(self)  # self eklendi
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_value = 0  # progress değeri eklendi
        self.init_ui()
        self.clicked.connect(self.baslat_yorumlama)
    
    def init_ui(self):
        self.setFixedSize(200, 75)
        self.setFont(QFont("bebas_font_family", 30))
        self.setStyleSheet("""
            QPushButton {
                background-color: red;
                border: none;
                border-radius: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread:pad, 
                    x1:0.028, y1:0.511091, 
                    x2:0.829, y2:0.590909, 
                    stop:0.113636 rgba(234, 77, 254, 255), 
                    stop:0.727273 rgba(255, 7, 67, 255)
                );
            }
            QPushButton:pressed {
                background-color: darkred;
                padding-left: 3px;
                padding-top: 3px;
            }
        """)

    def baslat_yorumlama(self):
        self.hide()  # Butonu gizle
        if self.progress_bar:
            self.progress_value = 0  # Değeri sıfırla
            self.progress_bar.setValue(0)
            self.progress_bar.show()
            self.progress_timer.start(30)  # Hızı artırmak için 30ms yapıldı

    def update_progress(self):
        if self.progress_bar:
            self.progress_value += 1
            self.progress_bar.setValue(self.progress_value)
            
            if self.progress_value >= 100:
                self.progress_timer.stop()
                self.progress_bar.hide()
                self.ruyayi_yorumla()
                self.show()

    def ruyayi_yorumla(self):
        try:
            if self.yorum_kutusu:
                self.yorum_kutusu.show()
                
            # Kullanıcının girdiği metni al
            girilen_metin = self.text_kutusu.toPlainText()  # lower() kaldırıldı
            kelimeler = girilen_metin.split()
            
            # Duygu analizi için orijinal metni sakla
            duygu_metni = girilen_metin

            conn = sqlite3.connect('ruyaanlamlari.db')
            cursor = conn.cursor()
            
            detaylar = []
            
            for kelime in kelimeler:
                cursor.execute("SELECT detay FROM kelime_detay WHERE kelime = ?", (kelime.lower(),))
                sonuc = cursor.fetchone()
                if sonuc:
                    detaylar.append(sonuc[0])

            if detaylar and self.yorum_kutusu:
                self.text_kutusu.clear()
                # Hem orijinal metni hem de detayları gönder
                duzenlenmis_yorum = metin_duzenle(detaylar, duygu_metni)
                self.yorum_kutusu.setText(duzenlenmis_yorum)
            elif self.yorum_kutusu:
                self.yorum_kutusu.setText("Rüya yorumu bulunamadı.")

            conn.close()
        except Exception as e:
            print(f"Hata: {e}")
            if self.yorum_kutusu:
                self.yorum_kutusu.setText("Bir hata oluştu.")
