import joblib
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFrame, QMessageBox
)
from PySide6.QtCore import Qt

class Klasifikasi(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.model = None
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("contentArea")
        
        self.load_model()
        self.init_ui()

    def load_model(self):
        """Memuat model NLP yang sudah dilatih."""
        try:
            model_path = os.path.join("assets", "models", "category_classifier.pkl")
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                print("Model klasifikasi belum tersedia.")
        except Exception as e:
            print(f"Gagal memuat model: {e}")

    def init_ui(self):
        # Layout Utama Vertikal Konten Kanan
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # --- 1. HEADER AREA  ---
        header_widget = QWidget()
        header_widget.setObjectName("headerArea")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_layout.setSpacing(5)

        self.title_label = QLabel("Smart AI Classification")
        self.title_label.setObjectName("welcomeLabel") 
        
        self.subtitle_label = QLabel("Asisten Otomatis Prediksi Kategori Pengeluaran Berbasis NLP")
        self.subtitle_label.setObjectName("subtitleLabel")
        
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(header_widget)

        # --- 2. MAIN CONTENT CARD  ---
        self.central_card = QFrame()
        self.central_card.setObjectName("classifierCard")
        
        card_layout = QVBoxLayout(self.central_card)
        card_layout.setContentsMargins(35, 35, 35, 35)
        card_layout.setSpacing(20)

        # Input Section
        input_box = QVBoxLayout()
        input_box.setSpacing(10)
        
        self.instruction = QLabel("Apa yang Anda beli hari ini?")
        self.instruction.setObjectName("inputInstruction")
        
        self.leDeskripsi = QLineEdit()
        self.leDeskripsi.setPlaceholderText("Misal: Nasi goreng spesial pedas atau bayar token listrik...")
        self.leDeskripsi.setObjectName("inputDeskripsi")
        self.leDeskripsi.setFixedHeight(50)
        
        input_box.addWidget(self.instruction)
        input_box.addWidget(self.leDeskripsi)
        card_layout.addLayout(input_box)

        # Action Button
        self.btnKlasifikasi = QPushButton("Analisis Deskripsi dengan AI")
        self.btnKlasifikasi.setObjectName("btnKlasifikasi2")
        self.btnKlasifikasi.setCursor(Qt.PointingHandCursor)
        self.btnKlasifikasi.setFixedHeight(45)
        self.btnKlasifikasi.clicked.connect(self.proses_klasifikasi)
        card_layout.addWidget(self.btnKlasifikasi)

        # Divider
        line = QFrame()
        line.setObjectName("dividerLine")
        line.setFrameShape(QFrame.HLine)
        card_layout.addWidget(line)

        # Result Section
        result_box = QVBoxLayout()
        result_box.setSpacing(8)
        result_box.setAlignment(Qt.AlignCenter)
        
        self.labelTitleHasil = QLabel("HASIL PREDIKSI KATEGORI")
        self.labelTitleHasil.setObjectName("resultHeader")
        self.labelTitleHasil.setAlignment(Qt.AlignCenter)
        
        self.labelHasil = QLabel("Menunggu Input Deskripsi Transaksi...")
        self.labelHasil.setObjectName("labelHasil")
        self.labelHasil.setAlignment(Qt.AlignCenter)
        
        result_box.addWidget(self.labelTitleHasil)
        result_box.addWidget(self.labelHasil)
        card_layout.addLayout(result_box)

        main_layout.addWidget(self.central_card)
        main_layout.addStretch() 

    def proses_klasifikasi(self):
        text = self.leDeskripsi.text().strip()

        if not text:
            QMessageBox.warning(self, "Input Kosong", "Harap masukkan deskripsi terlebih dahulu!")
            self.leDeskripsi.setFocus()
            return

        if self.model:
            try:
                # Jalankan prediksi menggunakan pipeline NLP (.pkl)
                prediction = self.model.predict([text])[0]
                self.labelHasil.setText(str(prediction).upper())
                
                if prediction in ["Makanan", "Minuman"]:
                    self.labelHasil.setProperty("categoryState", "food")
                elif prediction == "Transportasi":
                    self.labelHasil.setProperty("categoryState", "transport")
                else:
                    self.labelHasil.setProperty("categoryState", "default")
                
                # Memaksa Qt Engine memoles ulang style secara dinamis sesuai properti baru
                self.labelHasil.style().unpolish(self.labelHasil)
                self.labelHasil.style().polish(self.labelHasil)
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal melakukan klasifikasi: {e}")
        else:
            QMessageBox.critical(self, "Model Error", "Model klasifikasi (.pkl) tidak ditemukan di folder assets/models!")