from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QProgressBar, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QTextOption
from PyQt6.QtCore import Qt
from OzelButon import OzelButon
from YorumKutusu import YorumKutusu
import sqlite3

def veritabani_detay_getir():
    try:
        conn = sqlite3.connect('veritabani.db')
        cursor = conn.cursor()
        cursor.execute("SELECT detay FROM yorumlar")
        detaylar = cursor.fetchall()
        conn.close()
        return detaylar
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return []

def Pencere():
    app = QApplication([])
    pencere = QWidget()
    
    pencere.setStyleSheet("""
        QWidget#mainWindow {
            background-image: url(arka_plan.png);
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
        QLabel {
            background: transparent;
            color: white;
        }
        QPushButton {
            background-color: red;
            border: none;
            color: white;
        }
        QPushButton:hover {
            background-color: darkred;
            border: none;
            color: white;
        }
        QTextEdit {
            background-color: rgba(255, 255, 255, 0.8);
            border: 2px solid white;
            border-radius: 5px;
            padding: 5px;
        }
    """)
    pencere.setObjectName("mainWindow")
    
    bebas_font_id = QFontDatabase.addApplicationFont(r"C:\Users\efkar\OneDrive\Masaüstü\PYTHON\projedeneme1\Bebas-Regular.otf")
    bebas_font_family = QFontDatabase.applicationFontFamilies(bebas_font_id)[0]
    ubuntu_font_id = QFontDatabase.addApplicationFont(r"C:\Users\efkar\OneDrive\Masaüstü\PYTHON\projedeneme1\UbuntuMono-Bold.ttf")
    ubuntu_font_family = QFontDatabase.applicationFontFamilies(ubuntu_font_id)[0]
    
    
    pencere.setWindowTitle("Rüya Tabiri")
    pencere.setGeometry(100, 100, 500, 600)
    
    # Hoşgeldiniz yazısı
    etiket1 = QLabel("Merhaba Rüya Tabiri Programına Hoşgeldiniz!", pencere)
    etiket1.setStyleSheet("color:black")
    etiket1.setFont(QFont(ubuntu_font_family, 10))
    etiket1.adjustSize() # Etiketin gerçek boyutunu alma
    etiket1_x = (pencere.width() - etiket1.sizeHint().width()) // 2  # x ekseni ortala
    etiket1.move(etiket1_x, 50)
 
    # Sol üst logo
    etiket2 = QLabel(pencere)
    etiket2.setPixmap(QPixmap("logo1.png"))
    etiket2.move(10, 10)  
    
    # Sağ üst logo
    etiket3 = QLabel(pencere)
    etiket3.setPixmap(QPixmap("logo1.png"))
    etiket3.move(400, 10)  
    
    # Alt yazı
    etiket4 = QLabel("Yapay Zeka Dersi Projesi\n210303028-Mehmet Can KARA\n210303064-Merve KAHYA", pencere)
    etiket4.setStyleSheet("color:black")
    etiket4.setFont(QFont(ubuntu_font_family, 20))
    etiket4.adjustSize() # Etiketin gerçek boyutunu alma
    etiket4_x = (pencere.width() - etiket4.sizeHint().width()) // 2
    etiket4.move(etiket4_x, 510)  

    # Giriş kutusu
    text_kutusu = QTextEdit(pencere)
    text_kutusu.setFixedSize(400, 150)  # Yükseklik azaltıldı
    text_kutusu.setPlaceholderText("Rüyanızı yazınız...")
    text_kutusu.setFont(QFont(ubuntu_font_family, 12))
    text_kutusu_x = (pencere.width() - text_kutusu.width()) // 2
    text_kutusu.move(text_kutusu_x, 110)

    # Sonuç kutusu - düzeltildi
    sonuc_kutusu = YorumKutusu("", parent=pencere)  # parent parametresi belirtildi
    sonuc_kutusu.setFixedSize(400, 150)
    sonuc_kutusu_x = (pencere.width() - sonuc_kutusu.width()) // 2
    sonuc_kutusu.move(sonuc_kutusu_x, 270)  # Konumu yukarı alındı
    sonuc_kutusu.hide()

    # Progress bar oluşturma - güncellenmiş hali
    progress_bar = QProgressBar(pencere)
    progress_bar.setFixedSize(200, 30)
    progress_bar_x = (pencere.width() - progress_bar.width()) // 2
    progress_bar.move(progress_bar_x, 430)  # Konumu aşağı alındı
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(100)
    progress_bar.setValue(0)
    progress_bar.setTextVisible(True)
    progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: red;
            width: 10px;
            margin:0.5px;
        }
    """)
    progress_bar.hide()  # Başlangıçta gizli

    # Yorumla butonu
    buton = OzelButon("YORUMLA", pencere, 
                      yorum_kutusu=sonuc_kutusu,
                      text_kutusu=text_kutusu,
                      progress_bar=progress_bar)
    buton.setFixedSize(200, 50)  # Boyut küçültüldü
    buton_x = (pencere.width() - buton.width()) // 2
    buton.move(buton_x, 430)  # Konumu aşağı alındı

    pencere.show()
    app.exec()

Pencere()