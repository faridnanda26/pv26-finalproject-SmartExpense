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
        # 1. Layout Utama Halaman
        main_layout = QVBoxLayout(self) 
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 2. Container Kartu Sign-In 
        self.signup_card = QFrame()
        self.signup_card.setObjectName("signupCard")
        self.signup_card.setFixedSize(450, 480) 
        
        card_layout = QVBoxLayout(self.signup_card)
        card_layout.setContentsMargins(40, 35, 40, 35)
        card_layout.setSpacing(18)

        # 3. Logo Aplikasi
        self.lblLogo = QLabel()
        logo_pixmap = QPixmap("assets/logo.png") 
        self.lblLogo.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblLogo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lblLogo) 

        # 4. Judul
        self.label = QLabel('DAFTAR AKUN BARU')
        self.label.setObjectName("signupTitle") 
        self.label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.label)

        # 5. Input Fields
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

        # 6. Tombol Daftar Utama 
        self.btnRegister = QPushButton('Daftar Sekarang')
        self.btnRegister.setObjectName("btnRegister") 
        self.btnRegister.setCursor(Qt.PointingHandCursor)
        self.btnRegister.setFixedHeight(45)
        self.btnRegister.clicked.connect(self.handle_signup)
        card_layout.addWidget(self.btnRegister)

        # 7. Teks Tautan Kembali 
        self.lblLoginLink = QLabel('Sudah punya akun? <a href="#login" style="text-decoration: none; color: #005088; font-weight: bold;">Login</a>')
        self.lblLoginLink.setObjectName("loginLink")
        self.lblLoginLink.setAlignment(Qt.AlignCenter)
        self.lblLoginLink.setCursor(Qt.PointingHandCursor)
        
        # Mengizinkan interaksi link HTML dan dihubungkan ke signal
        self.lblLoginLink.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.lblLoginLink.linkActivated.connect(lambda: self.go_to_login.emit())
        card_layout.addWidget(self.lblLoginLink)

        # 8. Masukkan kartu ke layout utama
        main_layout.addWidget(self.signup_card)

    def handle_signup(self):
        # Ambil input
        nama = self.leFullName.text().strip()
        username = self.leUsername.text().strip()
        password = self.lePassword.text().strip()

        # 1. Validasi Nama
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
        success, message = self.db.register_user(username, password, nama)

        if success:
            QMessageBox.information(self, "Sukses", "Akun berhasil dibuat! Silakan login.")
            self.leFullName.clear()
            self.leUsername.clear()
            self.lePassword.clear()
            self.go_to_login.emit()
        else:
            QMessageBox.critical(self, "Gagal Daftar", message)