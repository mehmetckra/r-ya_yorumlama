from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, 
                           QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont
import sqlite3

class RuyaEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Rüya Ekle')
        self.setGeometry(100, 100, 400, 300)
        
        # Ana layout
        layout = QVBoxLayout()
        
        # Kelime girişi
        kelime_layout = QHBoxLayout()
        kelime_label = QLabel('Kelime:')
        self.kelime_input = QLineEdit()
        kelime_layout.addWidget(kelime_label)
        kelime_layout.addWidget(self.kelime_input)
        
        # Detay girişi
        detay_layout = QVBoxLayout()
        detay_label = QLabel('Detay:')
        self.detay_input = QTextEdit()
        detay_layout.addWidget(detay_label)
        detay_layout.addWidget(self.detay_input)
        
        # Ekle butonu
        self.ekle_btn = QPushButton('Ekle')
        self.ekle_btn.clicked.connect(self.ruya_ekle)
        
        # Layout'ları ana layout'a ekle
        layout.addLayout(kelime_layout)
        layout.addLayout(detay_layout)
        layout.addWidget(self.ekle_btn)
        
        self.setLayout(layout)
        
        # Stil
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
    def ruya_ekle(self):
        kelime = self.kelime_input.text().strip().lower()
        detay = self.detay_input.toPlainText().strip()
        
        if not kelime or not detay:
            QMessageBox.warning(self, 'Uyarı', 'Kelime ve detay alanları boş bırakılamaz!')
            return
            
        try:
            conn = sqlite3.connect('ruyaanlamlari.db')
            cursor = conn.cursor()
            
            # Tablonun varlığını kontrol et, yoksa oluştur
            cursor.execute('''CREATE TABLE IF NOT EXISTS kelime_detay 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             kelime TEXT NOT NULL,
                             detay TEXT NOT NULL)''')
            
            # Kelime kontrolü
            cursor.execute('SELECT kelime FROM kelime_detay WHERE kelime = ?', (kelime,))
            if cursor.fetchone():
                QMessageBox.warning(self, 'Uyarı', f'"{kelime}" kelimesi zaten veritabanında mevcut!')
                return
            
            # Veriyi ekle
            cursor.execute('INSERT INTO kelime_detay (kelime, detay) VALUES (?, ?)',
                         (kelime, detay))
            
            conn.commit()
            
            QMessageBox.information(self, 'Başarılı', 'Rüya başarıyla eklendi!')
            
            # Input alanlarını temizle
            self.kelime_input.clear()
            self.detay_input.clear()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Hata', f'Veritabanı hatası: {str(e)}')
            
        finally:
            conn.close()

# Test için
if __name__ == '__main__':

    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = RuyaEkle()
    window.show()
    sys.exit(app.exec())
