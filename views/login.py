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
        # Batasi ukuran kartu agar tidak melebar memenuhi QMainWindow
        self.login_card.setFixedSize(450, 350) 
        
        card_layout = QVBoxLayout(self.login_card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        # 3. Logo Aplikasi
        self.lblLogo = QLabel()
        pixmap = QPixmap("assets/logo.png") # Ganti dengan nama file logo Anda
        # Resize logo ke ukuran yang pas (misal 80x80 px) agar tetap tajam
        self.lblLogo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblLogo.setAlignment(Qt.AlignCenter)
        self.lblLogo.setContentsMargins(0, 0, 0, 10) # Beri jarak sedikit ke bawah
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

        # 6. Buttons
        btn_layout = QHBoxLayout()
        self.btnLogin = QPushButton('Masuk')
        self.btnLogin.setObjectName("btnLogin") 
        self.btnLogin.setCursor(Qt.PointingHandCursor)
        self.btnLogin.clicked.connect(self.handle_login)
        
        self.btnSignin = QPushButton('Daftar')
        self.btnSignin.setObjectName("btnGoToSignup") 
        self.btnSignin.setCursor(Qt.PointingHandCursor)
        self.btnSignin.clicked.connect(self.go_to_signup.emit)
        
        btn_layout.addWidget(self.btnLogin)
        btn_layout.addWidget(self.btnSignin)

        card_layout.addLayout(btn_layout)
        
        # 7. Masukkan kartu ke layout utama
        main_layout.addWidget(self.login_card)

    def handle_login(self):
        # Ambil input dari QLineEdit 
        username = self.leUsername.text().strip()
        password = self.lePassword.text().strip()

        # 1. Jalankan Validasi Username menggunakan class Validator
        is_valid_user, msg_user = Validator.validasi_username(username)
        if not is_valid_user:
            QMessageBox.warning(self, "Input Salah", msg_user)
            self.leUsername.setFocus() # Arahkan kursor kembali ke username
            return

        # 2. Jalankan Validasi Password menggunakan class Validator
        is_valid_pw, msg_pw = Validator.validasi_password(password)
        if not is_valid_pw:
            QMessageBox.warning(self, "Input Salah", msg_pw)
            self.lePassword.setFocus() # Arahkan kursor kembali ke password
            return

        # 3. Jika lolos validasi, baru cek ke Database
        user = self.db.check_login(username, password)
        
        if user:
            # Reset input sebelum pindah halaman
            self.leUsername.clear()
            self.lePassword.clear()
            QMessageBox.information(self, "Berhasil", f"Selamat datang, {user['nama_lengkap']}!")
            # Kirim signal login sukses
            self.login_success.emit(user['id'], user['nama_lengkap'])
        else:
            QMessageBox.critical(self, "Gagal", "Username atau Password salah.")
            self.lePassword.clear()
            self.lePassword.setFocus()