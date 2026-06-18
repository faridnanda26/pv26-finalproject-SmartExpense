from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from logic.validator import Validator

class Login(QWidget):
    login_success = Signal(int, str)  # Mengirim (user_id, nama_lengkap)
    go_to_signup = Signal()           # Signal untuk pindah ke tab SignUp

    def __init__(self, db_manager):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('loginPage')
        self.db = db_manager 
        self.init_ui()

    def init_ui(self):
        # 1. Layout Utama Halaman (Background luar kartu)
        main_layout = QVBoxLayout(self) 
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0) 

        # 2. Container Kartu Login (Area Putih)
        self.login_card = QFrame()
        self.login_card.setObjectName("loginCard")
        self.login_card.setFixedSize(450, 420) 
        
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setContentsMargins(40, 35, 40, 35)
        card_layout.setSpacing(18)

        # 3. Logo Aplikasi
        self.lblLogo = QLabel()
        pixmap = QPixmap("assets/logo.png") 
        self.lblLogo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblLogo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.lblLogo)

        # 4. Judul
        self.label = QLabel('SMART EXPENSE')
        self.label.setObjectName("loginTitle") 
        self.label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.label)

        # 5. Input Fields
        self.leUsername = QLineEdit()
        self.leUsername.setPlaceholderText('Username')
        card_layout.addWidget(self.leUsername)

        self.lePassword = QLineEdit()
        self.lePassword.setPlaceholderText('Password')
        self.lePassword.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.lePassword)

        # 6. Tombol Masuk Utama (Lebar Penuh)
        self.btnLogin = QPushButton('Masuk')
        self.btnLogin.setObjectName("btnLogin") 
        self.btnLogin.setCursor(Qt.PointingHandCursor)
        self.btnLogin.setFixedHeight(45) 
        self.btnLogin.clicked.connect(self.handle_login)
        card_layout.addWidget(self.btnLogin)

        # 7. Teks Tautan Registrasi
        self.lblSignupLink = QLabel('Belum punya akun? <a href="#signup" style="text-decoration: none; color: #005088; font-weight: bold;">Daftar</a>')
        self.lblSignupLink.setObjectName("signupLink")
        self.lblSignupLink.setAlignment(Qt.AlignCenter)
        self.lblSignupLink.setCursor(Qt.PointingHandCursor)
        
        # Mengizinkan interaksi link HTML dan menghubungkannya ke signal
        self.lblSignupLink.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.lblSignupLink.linkActivated.connect(lambda: self.go_to_signup.emit())
        
        card_layout.addWidget(self.lblSignupLink)
        
        # 8. Masukkan kartu ke layout utama
        main_layout.addWidget(self.login_card)

    def handle_login(self):
        username = self.leUsername.text().strip()
        password = self.lePassword.text().strip()

        # 1. Validasi Username
        is_valid_user, msg_user = Validator.validasi_username(username)
        if not is_valid_user:
            QMessageBox.warning(self, "Input Salah", msg_user)
            self.leUsername.setFocus()
            return

        # 2. Validasi Password
        is_valid_pw, msg_pw = Validator.validasi_password(password)
        if not is_valid_pw:
            QMessageBox.warning(self, "Input Salah", msg_pw)
            self.lePassword.setFocus()
            return

        # 3. Cek Ke Database
        user = self.db.check_login(username, password)
        
        if user:
            self.leUsername.clear()
            self.lePassword.clear()
            QMessageBox.information(self, "Berhasil", f"Selamat datang, {user['nama_lengkap']}!")
            self.login_success.emit(user['id'], user['nama_lengkap'])
        else:
            QMessageBox.critical(self, "Gagal", "Username atau Password salah.")
            self.lePassword.clear()
            self.lePassword.setFocus()