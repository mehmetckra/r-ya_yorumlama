from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption  # QTextOption'ı QtGui'den import ediyoruz

class YorumKutusu(QTextEdit):
    def __init__(self, metin, parent=None):
        super().__init__(metin, parent)
        self.init_ui()
        self.setReadOnly(True)
    
    def init_ui(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.8);
                border: 2px solid white;
                border-radius: 5px;
                padding: 5px;
                color: black;
                font-size: 14px;
            }
        """)
        
        # Düzeltilmiş satır sarma modu ayarı
        self.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        
        # Metni sol üstten hizalama
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Başlangıç metni boş olsun
        self.clear()
    
    def setText(self, text):
        super().setPlainText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
