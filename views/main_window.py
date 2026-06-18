import csv
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTabWidget, QMessageBox, QStyle, QFileDialog, QLabel
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from views.login import Login
from views.signin import SignIn
from views.dashboard import Dashboard
from views.statistik import Statistik
from views.klasifikasi import Klasifikasi
from views.sidebar import Sidebar  

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
        self.setup_statusbar()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        # 1. Buat widget sentral dan pasang layout horizontal terluar
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_window_layout = QHBoxLayout(self.central_widget)
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.main_window_layout.setSpacing(0)

        # 2. Tambahkan Master Sidebar ke jendela utama
        self.sidebar = Sidebar()
        self.main_window_layout.addWidget(self.sidebar)
        self.sidebar.hide()  # Default awal disembunyikan (muncul hanya setelah login)

        # 3. Sistem Multi-Halaman menggunakan QTabWidget (Tab bar disembunyikan)
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.main_window_layout.addWidget(self.tabs)

        # Inisialisasi setiap halaman objek
        self.login_page = Login(self.db)
        self.sign_in_page = SignIn(self.db)
        self.dashboard_page = Dashboard(self.db)
        self.stat_page = Statistik(self.db)
        self.klasifikasi_page = Klasifikasi(self.db)

        # Daftarkan halaman ke indeks Tab
        self.tabs.addTab(self.login_page, "Login")              # Index 0
        self.tabs.addTab(self.sign_in_page, "Sign-In")          # Index 1
        self.tabs.addTab(self.dashboard_page, "Dashboard")      # Index 2
        self.tabs.addTab(self.stat_page, "Statistik")           # Index 3
        self.tabs.addTab(self.klasifikasi_page, "Klasifikasi")  # Index 4
        
        # ============================================================================
        # MANAJEMEN ROUTING SIGNAL & SLOTS
        # ============================================================================
        
        # Navigasi Autentikasi Awal
        self.login_page.go_to_signup.connect(lambda: self.tabs.setCurrentIndex(1))
        self.sign_in_page.go_to_login.connect(lambda: self.tabs.setCurrentIndex(0))
        self.login_page.login_success.connect(self.on_login_success)

        # Navigasi Router Menggunakan Komponen Sidebar Baru
        self.sidebar.go_dashboard.connect(lambda: self.switch_internal_page(2))
        self.sidebar.go_statistik.connect(lambda: self.switch_internal_page(3))
        self.sidebar.go_klasifikasi.connect(lambda: self.switch_internal_page(4))
        
        # Utilitas Aksi Sidebar Bagian Bawah
        self.sidebar.trigger_logout.connect(self.logout)
        self.sidebar.trigger_exit.connect(self.close)

        # Proteksi Awal: Kunci akses halaman internal sebelum user login
        self.tabs.setTabEnabled(2, False)
        self.tabs.setTabEnabled(3, False)
        self.tabs.setTabEnabled(4, False)

    def switch_internal_page(self, tab_index):
        """Mengatur perpindahan halaman konten sekaligus merubah status aktif tombol sidebar."""
        self.tabs.setCurrentIndex(tab_index)
        
        # Sinkronisasikan perubahan visual tombol di dalam sidebar
        self.sidebar.set_active_menu(tab_index)
        
        # Trigger pembaruan data secara real-time saat halaman dibuka
        if tab_index == 2:
            self.dashboard_page.load_data()
        elif tab_index == 3:
            self.stat_page.refresh_statistics()

    def on_login_success(self, user_id, user_nama):
        """Logic penanganan session ketika user berhasil masuk"""
        self.current_user_id = user_id
        self.current_user_name = user_nama

        # Kirim data user session ke masing-masing halaman anak
        self.dashboard_page.set_user_session(user_id, user_nama)
        self.stat_page.set_user_session(user_id, user_nama)
        
        # Buka gembok proteksi halaman internal
        self.tabs.setTabEnabled(2, True)
        self.tabs.setTabEnabled(3, True)
        self.tabs.setTabEnabled(4, True)
        
        # Kunci halaman login agar tidak bisa diakses tanpa logout
        self.tabs.setTabEnabled(0, False)
        self.tabs.setTabEnabled(1, False)
        
        # TAMPILKAN SIDEBAR UTAMA & Masuk ke Dashboard
        self.sidebar.show()
        self.switch_internal_page(2)

    def logout(self):
        """Menghapus session, menyembunyikan sidebar, dan kembali ke login form"""
        confirm = QMessageBox.question(
            self, "Konfirmasi Logout",
            "Apakah Anda yakin ingin keluar dari akun ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.current_user_id = None
            self.current_user_name = None
            
            # Kembalikan status akses halaman awal
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.tabs.setTabEnabled(4, False)
            
            # SEMBUNYIKAN PANEL SIDEBAR KEMBALI
            self.sidebar.hide()
            self.tabs.setCurrentIndex(0)
            self.statusBar().showMessage("Logged out successfully", 3000)

    def create_actions(self):
        style = self.style()

        # About
        self.about_action = QAction("About", self)
        self.about_action.setIcon(style.standardIcon(QStyle.SP_MessageBoxInformation))
        self.about_action.triggered.connect(self.show_version)

        # Logout Menu Action 
        self.logout_action = QAction("Logout", self)
        self.logout_action.setIcon(QIcon("assets/logout.png"))
        self.logout_action.triggered.connect(self.logout)

        # Close
        self.close_action = QAction("Close", self)
        self.close_action.setIcon(QIcon("assets/close.png"))
        self.close_action.triggered.connect(self.close)

        # CSV Export
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
            "Build Date: June 2026\n"
            "© 2026 Tim Informatika Unram."
        )
        
        QMessageBox.information(
            self,
            "Tentang Aplikasi", 
            version_info
        )

    def setup_statusbar(self):
        status_bar = self.statusBar()
        status_bar.setObjectName("mainStatusBar")
        
        info_tim = (
            "Valerine Jesika Dewi (F1D02310027) | "
            "Farid Nanda Syauqi (F1D02310050) | "
            "Amir Hamzah (F1D021027)"
        )
        
        self.lbl_tim = QLabel(info_tim)
        self.lbl_tim.setObjectName("lblStatusBar")
        status_bar.addPermanentWidget(self.lbl_tim)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Konfirmasi Keluar',
            "Apakah Anda yakin ingin menutup aplikasi Smart Expense?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def export_csv(self):
        if not self.current_user_id:
            QMessageBox.warning(self, "Export Gagal", "Silakan login terlebih dahulu.")
            return

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
                writer.writerow(["Tanggal", "Kategori", "Nominal (Rp)", "Deskripsi"])
                for r in data:
                    writer.writerow([r[0], r[1], r[2], r[3]])
                    
            QMessageBox.information(self, "Success", f"Data berhasil diekspor ke:\n{filepath}")
            self.statusBar().showMessage(f"Exported to {filepath}", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "Error Export", f"Gagal mengekspor data: {str(e)}")