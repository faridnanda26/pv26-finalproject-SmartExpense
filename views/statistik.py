from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame
)
from PySide6.QtCore import Qt, QDate, Signal
from .chart_widget import ExpensePieChartWidget  

class Statistik(QWidget):
    # Signal untuk memberitahu MainWindow agar pindah kembali ke Dashboard
    go_back = Signal()
    go_klasifikasi = Signal()

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager

        self.user_id = None
        self.user_nama = ""

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("statistikPage")
        self.current_date = QDate.currentDate()
        
        self.init_ui()

    def set_user_session(self, user_id, user_nama):
        """Menerima data user dari MainWindow setelah login sukses"""
        self.user_id = user_id
        self.user_nama = user_nama
        self.refresh_statistics()

    def init_ui(self):
        # Layout Utama
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 1. HEADER (Tombol Kembali di Kiri, Tombol Klasifikasi di Kanan)
        header_layout = QHBoxLayout()
        
        # Tombol Kembali (Kiri)
        self.btnBack = QPushButton("<- Kembali ke Dashboard")
        self.btnBack.setObjectName("btnBack")
        self.btnBack.clicked.connect(self.go_back.emit)
        header_layout.addWidget(self.btnBack)
        
        # STRETCH: Ini yang akan mendorong tombol berikutnya ke paling kanan
        header_layout.addStretch()
        
        # Tombol Klasifikasi (Kanan)
        self.btnKlasifikasi = QPushButton("Klasifikasi ->")
        self.btnKlasifikasi.setObjectName("btnKlasifikasi")
        self.btnKlasifikasi.clicked.connect(self.go_klasifikasi.emit)
        header_layout.addWidget(self.btnKlasifikasi)
        
        # Tambahkan header_layout ke layout utama 
        layout.addLayout(header_layout)

        # 2. NAVIGASI BULAN (Container Frame)
        self.nav_frame = QFrame()
        self.nav_frame.setObjectName("navFrameStat")
        nav_layout = QHBoxLayout(self.nav_frame)

        self.btnPrev = QPushButton(" < ")
        self.btnPrev.setObjectName("btnNavMonthStat")
        self.btnPrev.setFixedSize(30, 30)
        self.btnPrev.clicked.connect(self.prev_month)

        self.labelBulan = QLabel(self.current_date.toString("MMMM yyyy"))
        self.labelBulan.setObjectName("labelBulanStat")
        self.labelBulan.setAlignment(Qt.AlignCenter)
        self.labelBulan.setFixedWidth(200)

        self.btnNext = QPushButton(" > ")
        self.btnNext.setObjectName("btnNavMonthStat")
        self.btnNext.setFixedSize(30, 30)
        self.btnNext.clicked.connect(self.next_month)

        nav_layout.addStretch()
        nav_layout.addWidget(self.btnPrev)
        nav_layout.addWidget(self.labelBulan)
        nav_layout.addWidget(self.btnNext)
        nav_layout.addStretch()
        
        layout.addWidget(self.nav_frame)

        self.labelTotal = QLabel("Total Pengeluaran: Rp 0")
        self.labelTotal.setObjectName("labelTotalStat")
        self.labelTotal.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.labelTotal)

        # 3. AREA GRAFIK
        self.chart_container = QFrame()
        self.chart_container.setObjectName("chartContainer")
        chart_main_layout = QVBoxLayout(self.chart_container)
        
        self.pie_chart = ExpensePieChartWidget()
        chart_main_layout.addWidget(self.pie_chart)
        
        layout.addWidget(self.chart_container)
        
        self.setLayout(layout)

    # --- LOGIKA NAVIGASI ---
    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.refresh_statistics()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.refresh_statistics()

    def refresh_statistics(self):
        bulan = self.current_date.month()
        tahun = self.current_date.year()
        self.labelBulan.setText(self.current_date.toString("MMMM yyyy"))
        
        # 1. Update Label Total
        total = self.db.get_total_monthly(self.user_id, bulan, tahun)
        self.labelTotal.setText(f"Total Pengeluaran: Rp {total:,.0f}")
        
        # 2. Update Grafik
        df = self.db.get_category_data_df(self.user_id, bulan, tahun)
        self.pie_chart.plot(df, f"Distribusi Kategori - {self.current_date.toString('MMMM yyyy')}")