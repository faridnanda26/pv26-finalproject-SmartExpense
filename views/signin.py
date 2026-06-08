from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from logic.validator import Validator

class SignIn(QWidget):
    """Halaman Pendaftaran User Baru"""
    # Signal untuk kembali ke tab Login setelah sukses atau batal
    go_to_login = Signal()

    def __init__(self, db_manager):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('signinPage')
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        # Layout Utama Halaman
        main_layout = QVBoxLayout(self) 
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container Kartu Sign-In 
        self.signup_card = QFrame()
        self.signup_card.setObjectName("signupCard") 
        self.signup_card.setFixedSize(450, 460) 
        
        card_layout = QVBoxLayout(self.signup_card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(15)

        # Logo
        self.lblLogo = QLabel()
        logo_pixmap = QPixmap("assets/logo.png") 
        self.lblLogo.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblLogo.setAlignment(Qt.AlignCenter)
        self.lblLogo.setContentsMargins(0, 0, 0, 5)
        card_layout.addWidget(self.lblLogo) 

        # Judul
        self.label = QLabel('DAFTAR AKUN BARU')
        self.label.setObjectName("signupTitle") 
        self.label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.label)

        # Input Fields
        self.leFullName = QLineEdit()
        self.leFullName.setPlaceholderText('Nama Lengkap')
        card_layout.addWidget(self.leFullName)

        self.leUsername = QLineEdit()
        self.leUsername.setPlaceholderText('Username Baru')
        card_layout.addWidget(self.leUsername)

        self.lePassword = QLineEdit()
        self.lePassword.setPlaceholderText('Password')
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.lePassword)

        # Layout Tombol
        btn_layout = QHBoxLayout()
        
        # Tombol Daftar 
        self.btnRegister = QPushButton('Daftar Sekarang')
        self.btnRegister.setObjectName("btnRegister") 
        self.btnRegister.setCursor(Qt.PointingHandCursor)
        self.btnRegister.clicked.connect(self.handle_signup)
        btn_layout.addWidget(self.btnRegister)

        # Tombol Batal
        self.btnBack = QPushButton('Batal')
        self.btnBack.setObjectName("btnBack") 
        self.btnBack.setCursor(Qt.PointingHandCursor)
        self.btnBack.clicked.connect(self.go_to_login.emit)
        btn_layout.addWidget(self.btnBack)

        card_layout.addLayout(btn_layout)
        main_layout.addWidget(self.signup_card)

    def handle_signup(self):
        # Ambil input
        nama = self.leFullName.text().strip()
        username = self.leUsername.text().strip()
        password = self.lePassword.text().strip()

        # 1. Validasi Nama menggunakan Validator 
        is_valid_nama, msg_nama = Validator.validasi_nama(nama)
        if not is_valid_nama:
            QMessageBox.warning(self, "Input Salah", msg_nama)
            self.leFullName.setFocus()
            return

        # 2. Validasi Username
        is_valid_user, msg_user = Validator.validasi_username(username)
        if not is_valid_user:
            QMessageBox.warning(self, "Input Salah", msg_user)
            self.leUsername.setFocus()
            return

        # 3. Validasi Password
        is_valid_pw, msg_pw = Validator.validasi_password(password)
        if not is_valid_pw:
            QMessageBox.warning(self, "Input Salah", msg_pw)
            self.lePassword.setFocus()
            return

        # 4. Kirim ke Database
        # register_user mengembalikan (True/False, Pesan)
        success, message = self.db.register_user(username, password, nama)

        if success:
            QMessageBox.information(self, "Sukses", "Akun berhasil dibuat! Silakan login.")
            # Bersihkan form
            self.leFullName.clear()
            self.leUsername.clear()
            self.lePassword.clear()
            # Pindah ke tab Login otomatis
            self.go_to_login.emit()
        else:
            # Biasanya gagal karena username sudah ada (Unique Constraint)
            QMessageBox.critical(self, "Gagal Daftar", message)