import csv
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QLabel, QTableWidget, QTabWidget,
    QTableWidgetItem, QMessageBox, QStyle, QDialog, QFileDialog
)

from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from views.login import Login
from views.signin import SignIn
from views.dashboard import Dashboard
from views.statistik import Statistik
from views.klasifikasi import Klasifikasi

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Smart Expense")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon("assets/logo.png"))

        self.db = db
        self.current_user_id = None
        self.current_user_name = None

        self.center_on_screen()
        self.setup_ui()
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.setup_statusbar()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.setCentralWidget(self.tabs)

        # Inisialisasi page
        self.login_page = Login(self.db)
        self.sign_in_page = SignIn(self.db)
        self.dashboard_page = Dashboard(self.db)
        self.stat_page = Statistik(self.db)
        self.klasifikasi_page = Klasifikasi(self.db)

        # Tambahkan ke QTabWidget
        self.tabs.addTab(self.login_page, "Login")
        self.tabs.addTab(self.sign_in_page, "Sign-In")
        self.tabs.addTab(self.dashboard_page, "Dashboard")
        self.tabs.addTab(self.stat_page, "Statistik")
        self.tabs.addTab(self.klasifikasi_page, "klasifikasi")
        
        # 1. Navigasi antar Tab
        self.login_page.go_to_signup.connect(lambda: self.tabs.setCurrentIndex(1))
        self.sign_in_page.go_to_login.connect(lambda: self.tabs.setCurrentIndex(0))
        self.dashboard_page.go_to_stat.connect(lambda: self.tabs.setCurrentIndex(3))
        self.stat_page.go_back.connect(lambda: self.tabs.setCurrentIndex(2))
        self.stat_page.go_klasifikasi.connect(lambda: self.tabs.setCurrentIndex(4))
        self.klasifikasi_page.go_back.connect(lambda: self.tabs.setCurrentIndex(3))

        # 2. Respon ketika Login Berhasil
        self.login_page.login_success.connect(self.on_login_success)
        
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)

    def create_actions(self):
        style = self.style()

        # About
        self.about_action = QAction("About", self)
        self.about_action.setIcon(style.standardIcon(QStyle.SP_MessageBoxInformation)) # default icon
        self.about_action.triggered.connect(self.show_version)

        # Logout
        self.logout_action = QAction("Logout", self)
        self.logout_action.setIcon(QIcon("assets/logout.png"))
        self.logout_action.triggered.connect(self.logout)

        # Close
        self.close_action = QAction("Close", self)
        self.close_action.setIcon(QIcon("assets/close.png"))
        self.close_action.triggered.connect(self.close)

        # CSV
        self.csv_action = QAction("Export CSV", self)
        self.csv_action.setIcon(QIcon("assets/csv.png"))
        self.csv_action.triggered.connect(self.export_csv)


    def create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.csv_action)
        file_menu.addSeparator()
        file_menu.addAction(self.logout_action)
        file_menu.addAction(self.close_action)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(self.about_action)

    def create_toolbars(self):
        pass

    def show_version(self):
        version_info = (
            "Smart Expense Tracker AI\n"
            "Version: 1.0.0 (Stable)\n\n"
            "Teknologi Utama:\n"
            "- Core Framework: PySide6 (Qt for Python)\n"
            "- Database: SQLite 3\n"
            "- Engine ML: Scikit-Learn (Linear Regression)\n\n"
            "Pengembang:\n"
            "- Valerine Jesika Dewi (F1D02310027)\n"
            "- Farid Nanda Syauqi (F1D02310050)\n"
            "- Amir Hamzah (F1D021027)\n\n"
            "Build Date: Mei 2026\n"
            "© 2026 Tim Proyek Unram."
        )
        
        QMessageBox.information(
            self,
            "Tentang Aplikasi", 
            version_info
        )

    # --- Tambahan Method Handler ---
    def on_login_success(self, user_id, user_nama):
        """Logic ketika user berhasil masuk"""
        self.current_user_id = user_id
        self.current_user_name = user_nama

        self.dashboard_page.set_user_session(user_id, user_nama)
        self.stat_page.set_user_session(user_id, user_nama)
        
        # Aktifkan tab dashboard dan pindah ke sana
        self.tabs.setTabEnabled(2, True)
        self.tabs.setTabEnabled(3, True)
        self.tabs.setTabEnabled(4, True)
        self.tabs.setCurrentIndex(2)
        
        # Kunci tab Login & Sign-Up agar user tidak kembali ke sana tanpa logout
        self.tabs.setTabEnabled(0, False)
        self.tabs.setTabEnabled(1, False)

    def setup_statusbar(self):
        """Menampilkan Nama & NIM Anggota di bagian bawah aplikasi"""
        status_bar = self.statusBar()
        status_bar.setObjectName("mainStatusBar")
        
        info_tim = (
            "Valerine Jesika Dewi (F1D02310027) | "
            "Farid Nanda Syauqi (F1D02310050) | "
            "Amir Hamzah (F1D021027)"
        )
        
        self.lbl_tim = QLabel(info_tim)
        self.lbl_tim.setObjectName("lblStatusBar")
        
        # addPermanentWidget memastikan label ada di sebelah kanan 
        # dan tidak tertutup oleh pesan sementara (seperti 'Ready')
        status_bar.addPermanentWidget(self.lbl_tim)

    def logout(self):
        """Menghapus session dan kembali ke halaman login"""
        confirm = QMessageBox.question(
            self, "Konfirmasi Logout",
            "Apakah Anda yakin ingin keluar dari akun ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            # 1. Bersihkan session data
            self.current_user_id = None
            self.current_user_name = None
            
            # 2. Reset status Tab (Aktifkan Login/Sign-In, Matikan Dashboard dkk)
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.tabs.setTabEnabled(4, False)
            
            # 3. Pindah ke tab Login
            self.tabs.setCurrentIndex(0)
            self.statusBar().showMessage("Logged out successfully", 3000)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Konfirmasi Keluar',
            "Apakah Anda yakin ingin menutup aplikasi Smart Expense?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept() # Menutup aplikasi
        else:
            event.ignore() # Membatalkan penutupan

    def export_csv(self):
        # Pastikan user sudah login
        if not self.current_user_id:
            QMessageBox.warning(self, "Export Gagal", "Silakan login terlebih dahulu.")
            return

        # Membuka dialog simpan file
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Data Pengeluaran", 
            f"Laporan_Pengeluaran_{self.current_user_name}.csv", 
            "CSV Files (*.csv)"
        )
        
        if not filepath:
            return
        
        try:
            data = self.db.get_all_expenses_by_user(self.current_user_id)
            
            if not data:
                QMessageBox.warning(self, "Export Gagal", "Tidak ada data pengeluaran untuk diekspor.")
                return

            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Menulis Header
                writer.writerow(["Tanggal", "Kategori", "Nominal (Rp)", "Deskripsi"])
                
                # Menulis Baris Data
                for r in data:
                    # r['tanggal'], r['nama_kategori'], r['nominal'], r['deskripsi']
                    writer.writerow([
                        r[0], # Tanggal
                        r[1], # Kategori
                        r[2], # Nominal
                        r[3]  # Deskripsi
                    ])
                    
            QMessageBox.information(self, "Success", f"Data berhasil diekspor ke:\n{filepath}")
            self.statusBar().showMessage(f"Exported to {filepath}", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error Export", f"Gagal mengekspor data: {str(e)}")