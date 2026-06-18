import os
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon

class Sidebar(QFrame):
    # Signal Navigasi Menu Atas
    go_dashboard = Signal()
    go_statistik = Signal()
    go_klasifikasi = Signal()
    
    # Signal Utilitas Bawah
    trigger_logout = Signal()
    trigger_exit = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sidebarFrame")
        self.init_ui()

    def init_ui(self):
        # Layout Utama Vertikal Sidebar
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(15, 30, 15, 20)
        sidebar_layout.setSpacing(10)

        # 1. LOGO UTAMA
        self.lblSidebarLogo = QLabel()
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            self.lblSidebarLogo.setPixmap(logo_pixmap.scaled(55, 55, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lblSidebarLogo.setAlignment(Qt.AlignCenter)
        
        self.lblSidebarTitle = QLabel("SmartExpense")
        self.lblSidebarTitle.setObjectName("sidebarBrandTitle")
        self.lblSidebarTitle.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(self.lblSidebarLogo)
        sidebar_layout.addWidget(self.lblSidebarTitle)
        
        # Garis pembatas horizontal tipis di bawah brand logo
        line_top = QFrame()
        line_top.setObjectName("sidebarLine")
        line_top.setFrameShape(QFrame.HLine)
        sidebar_layout.addWidget(line_top)
        sidebar_layout.addSpacing(15)

        # Ukuran standar untuk seluruh ikon menu
        icon_size = QSize(18, 18)

        # 2. TOMBOL NAVIGASI MENU ATAS
        self.menu_dashboard = QPushButton("Dashboard")
        self.menu_dashboard.setObjectName("menuBtnActive") 
        self.menu_dashboard.setCursor(Qt.PointingHandCursor)
        self.menu_dashboard.setIconSize(icon_size)
        dashboard_icon_path = os.path.join("assets", "home.png")
        if os.path.exists(dashboard_icon_path):
            self.menu_dashboard.setIcon(QIcon(dashboard_icon_path))
        self.menu_dashboard.clicked.connect(self.go_dashboard.emit)
        
        self.menu_statistik = QPushButton("Statistik")
        self.menu_statistik.setObjectName("menuBtn")
        self.menu_statistik.setCursor(Qt.PointingHandCursor)
        self.menu_statistik.setIconSize(icon_size)
        statistik_icon_path = os.path.join("assets", "bar-chart.png")
        if os.path.exists(statistik_icon_path):
            self.menu_statistik.setIcon(QIcon(statistik_icon_path))
        self.menu_statistik.clicked.connect(self.go_statistik.emit)

        self.menu_klasifikasi = QPushButton("Smart AI")
        self.menu_klasifikasi.setObjectName("menuBtn")
        self.menu_klasifikasi.setCursor(Qt.PointingHandCursor)
        self.menu_klasifikasi.setIconSize(icon_size)
        klasifikasi_icon_path = os.path.join("assets", "ai.png")
        if os.path.exists(klasifikasi_icon_path):
            self.menu_klasifikasi.setIcon(QIcon(klasifikasi_icon_path))
        self.menu_klasifikasi.clicked.connect(self.go_klasifikasi.emit)

        sidebar_layout.addWidget(self.menu_dashboard)
        sidebar_layout.addWidget(self.menu_statistik)
        sidebar_layout.addWidget(self.menu_klasifikasi)
        
        sidebar_layout.addStretch() 

        # Garis pembatas bawah sebelum tombol utilitas keluar
        line_bottom = QFrame()
        line_bottom.setObjectName("sidebarLine")
        line_bottom.setFrameShape(QFrame.HLine)
        sidebar_layout.addWidget(line_bottom)

        # 3. TOMBOL UTILITAS KELUAR (BAWAH)
        self.menu_logout = QPushButton("Logout")
        self.menu_logout.setObjectName("menuBtnLogout")
        self.menu_logout.setCursor(Qt.PointingHandCursor)
        self.menu_logout.setIconSize(icon_size)
        logout_icon_path = os.path.join("assets", "logout.png")
        if os.path.exists(logout_icon_path):
            self.menu_logout.setIcon(QIcon(logout_icon_path))
        self.menu_logout.clicked.connect(self.trigger_logout.emit)

        self.menu_exit = QPushButton("Exit App")
        self.menu_exit.setObjectName("menuBtnExit")
        self.menu_exit.setCursor(Qt.PointingHandCursor)
        self.menu_exit.setIconSize(icon_size)
        exit_icon_path = os.path.join("assets", "close.png")
        if os.path.exists(exit_icon_path):
            self.menu_exit.setIcon(QIcon(exit_icon_path))
        self.menu_exit.clicked.connect(self.trigger_exit.emit)

        sidebar_layout.addWidget(self.menu_logout)
        sidebar_layout.addWidget(self.menu_exit)

    def set_active_menu(self, index):
        """
        Mengubah status visual tombol aktif berdasarkan indeks halaman.
        index 2: Dashboard, index 3: Statistik, index 4: Klasifikasi
        """
        # Reset seluruh tombol menu ke keadaan objek pasif ('menuBtn')
        self.menu_dashboard.setObjectName("menuBtn")
        self.menu_statistik.setObjectName("menuBtn")
        self.menu_klasifikasi.setObjectName("menuBtn")
        
        # Nyalakan status 'menuBtnActive' pada tombol yang sesuai dengan indeks aktif
        if index == 2:
            self.menu_dashboard.setObjectName("menuBtnActive")
        elif index == 3:
            self.menu_statistik.setObjectName("menuBtnActive")
        elif index == 4:
            self.menu_klasifikasi.setObjectName("menuBtnActive")
            
        # Paksa Qt merender ulang stylesheet eksternal agar perubahan warna langsung terlihat
        self.menu_dashboard.style().unpolish(self.menu_dashboard)
        self.menu_dashboard.style().polish(self.menu_dashboard)
        self.menu_statistik.style().unpolish(self.menu_statistik)
        self.menu_statistik.style().polish(self.menu_statistik)
        self.menu_klasifikasi.style().unpolish(self.menu_klasifikasi)
        self.menu_klasifikasi.style().polish(self.menu_klasifikasi)