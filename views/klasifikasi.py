import joblib
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QFrame, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt, Signal

class Klasifikasi(QWidget):
    go_back = Signal()

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.model = None
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("klasifikasiPage")
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
        self.setObjectName("klasifikasiPage")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)

        # --- 1. HEADER AREA ---
        header_widget = QWidget()
        header_widget.setObjectName("headerArea")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 20)

        self.btnBack = QPushButton("<- Kembali")
        self.btnBack.setObjectName("btnBack")
        self.btnBack.setCursor(Qt.PointingHandCursor)
        self.btnBack.clicked.connect(self.go_back.emit)
        self.btnBack.setFixedSize(120, 40)
        
        header_layout.addWidget(self.btnBack)
        header_layout.addStretch()
        
        title_info = QVBoxLayout()
        self.title_label = QLabel("Smart Classification")
        self.title_label.setObjectName("titleLabel")
        
        self.subtitle_label = QLabel("AI-Powered Expense Categorization")
        self.subtitle_label.setObjectName("subtitleLabel")
        
        title_info.addWidget(self.title_label, alignment=Qt.AlignRight)
        title_info.addWidget(self.subtitle_label, alignment=Qt.AlignRight)
        header_layout.addLayout(title_info)
        
        main_layout.addWidget(header_widget)

        # --- 2. MAIN CONTENT CARD ---
        self.central_card = QFrame()
        self.central_card.setObjectName("classifierCard")
        card_layout = QVBoxLayout(self.central_card)
        card_layout.setContentsMargins(35, 40, 35, 40)
        card_layout.setSpacing(25)

        # Input Section
        input_box = QVBoxLayout()
        self.instruction = QLabel("Apa yang Anda beli hari ini?")
        self.instruction.setObjectName("inputInstruction")
        
        self.leDeskripsi = QLineEdit()
        self.leDeskripsi.setPlaceholderText("Misal: Nasi goreng spesial pedas...")
        self.leDeskripsi.setObjectName("inputDeskripsi")
        self.leDeskripsi.setFixedHeight(55)
        
        input_box.addWidget(self.instruction)
        input_box.addWidget(self.leDeskripsi)
        card_layout.addLayout(input_box)

        # Action Button
        self.btnKlasifikasi = QPushButton("Analisis Kategori")
        self.btnKlasifikasi.setObjectName("btnKlasifikasi2")
        self.btnKlasifikasi.setCursor(Qt.PointingHandCursor)
        self.btnKlasifikasi.setFixedHeight(50)
        self.btnKlasifikasi.clicked.connect(self.proses_klasifikasi)
        card_layout.addWidget(self.btnKlasifikasi)

        # Divider (Garis Pemisah)
        line = QFrame()
        line.setObjectName("dividerLine")
        line.setFrameShape(QFrame.HLine)
        card_layout.addWidget(line)

        # Result Section
        result_box = QVBoxLayout()
        result_box.setAlignment(Qt.AlignCenter)
        
        self.labelTitleHasil = QLabel("HASIL PREDIKSI")
        self.labelTitleHasil.setObjectName("resultHeader")
        self.labelTitleHasil.setAlignment(Qt.AlignCenter)
        
        self.labelHasil = QLabel("Menunggu Input...")
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
            return

        if self.model:
            try:
                # Prediksi menggunakan model NLP
                prediction = self.model.predict([text])[0]
                
                # Update Label Hasil
                self.labelHasil.setText(prediction)
                
                # Berikan warna berbeda berdasarkan kategori
                if prediction == "Makanan" or prediction == "Minuman":
                    self.labelHasil.setStyleSheet("font-size: 28px; font-weight: bold; color: #f39c12;")
                elif prediction == "Transportasi":
                    self.labelHasil.setStyleSheet("font-size: 28px; font-weight: bold; color: #1abc9c;")
                else:
                    self.labelHasil.setStyleSheet("font-size: 28px; font-weight: bold; color: #005088;")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal melakukan klasifikasi: {e}")
        else:
            QMessageBox.critical(self, "Model Error", "Model klasifikasi (.pkl) tidak ditemukan!")