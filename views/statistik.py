from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from .chart_widget import ExpensePieChartWidget  

class Statistik(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager

        self.user_id = None
        self.user_nama = ""

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("contentArea")
        self.current_date = QDate.currentDate()
        
        self.init_ui()

    def set_user_session(self, user_id, user_nama):
        """Menerima data user dari MainWindow setelah login sukses"""
        self.user_id = user_id
        self.user_nama = user_nama
        self.refresh_statistics()

    def init_ui(self):
        # Layout Utama Vertikal (Membagi Halaman Menjadi 3 Bagian Utama)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header Title Halaman
        self.lblPageTitle = QLabel("Analisis & Statistik Pengeluaran")
        self.lblPageTitle.setObjectName("welcomeLabel")
        main_layout.addWidget(self.lblPageTitle)

        # ============================================================================
        # BAGIAN 1: SUSUNAN KARTU RINGKASAN 
        # ============================================================================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        # 1A. Card Total Pengeluaran
        self.card_total = QFrame()
        self.card_total.setObjectName("cardTotalExpense")
        layout_ct = QVBoxLayout(self.card_total)
        lbl_title_ct = QLabel("TOTAL PENGELUARAN")
        lbl_title_ct.setObjectName("statCardTitle")
        self.val_total = QLabel("Rp 0")
        self.val_total.setObjectName("statCardValueTotal")
        layout_ct.addWidget(lbl_title_ct)
        layout_ct.addWidget(self.val_total)

        # 1B. Card Jumlah Pengeluaran (Total Transaksi)
        self.card_count = QFrame()
        self.card_count.setObjectName("cardCountExpense")
        layout_cc = QVBoxLayout(self.card_count)
        lbl_title_cc = QLabel("JUMLAH TRANSAKSI")
        lbl_title_cc.setObjectName("statCardTitle")
        self.val_count = QLabel("0 Transaksi")
        self.val_count.setObjectName("statCardValue")
        layout_cc.addWidget(lbl_title_cc)
        layout_cc.addWidget(self.val_count)

        # 1C. Card Kategori Dominan
        self.card_dominant = QFrame()
        self.card_dominant.setObjectName("cardDominantExpense")
        layout_cd = QVBoxLayout(self.card_dominant)
        lbl_title_cd = QLabel("KATEGORI DOMINAN")
        lbl_title_cd.setObjectName("statCardTitle")
        self.val_dominant = QLabel("-")
        self.val_dominant.setObjectName("statCardValueDominant")
        layout_cd.addWidget(lbl_title_cd)
        layout_cd.addWidget(self.val_dominant)

        # Masukkan ketiga kartu ke dalam layout baris horizontal
        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_count)
        cards_layout.addWidget(self.card_dominant)
        main_layout.addLayout(cards_layout)

        self.buat_efek_shadow(self.card_total)
        self.buat_efek_shadow(self.card_count)
        self.buat_efek_shadow(self.card_dominant)

        # ============================================================================
        # BAGIAN 2: NAVIGASI PAGINASI BULAN 
        # ============================================================================
        self.nav_frame = QFrame()
        self.nav_frame.setObjectName("navFrameStat") 
        nav_layout = QHBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(10, 5, 10, 5)

        self.btnPrev = QPushButton(" < ")
        self.btnPrev.setObjectName("btnNavMonthStat")
        self.btnPrev.setFixedSize(30, 30)
        self.btnPrev.setCursor(Qt.PointingHandCursor)
        self.btnPrev.clicked.connect(self.prev_month)

        self.labelBulan = QLabel(self.current_date.toString("MMMM yyyy"))
        self.labelBulan.setObjectName("labelBulanStat")
        self.labelBulan.setAlignment(Qt.AlignCenter)
        self.labelBulan.setFixedWidth(200)

        self.btnNext = QPushButton(" > ")
        self.btnNext.setObjectName("btnNavMonthStat")
        self.btnNext.setFixedSize(30, 30)
        self.btnNext.setCursor(Qt.PointingHandCursor)
        self.btnNext.clicked.connect(self.next_month)

        nav_layout.addStretch()
        nav_layout.addWidget(self.btnPrev)
        nav_layout.addWidget(self.labelBulan)
        nav_layout.addWidget(self.btnNext)
        nav_layout.addStretch()
        
        # Spacer penyeimbang kapsul di tengah halaman
        center_nav = QHBoxLayout()
        center_nav.addStretch()
        center_nav.addWidget(self.nav_frame)
        center_nav.addStretch()
        main_layout.addLayout(center_nav)

        # ============================================================================
        # BAGIAN 3: AREA GRAFIK UTAMA
        # ============================================================================
        self.chart_container = QFrame()
        self.chart_container.setObjectName("chartContainer")
        chart_main_layout = QVBoxLayout(self.chart_container)
        
        self.pie_chart = ExpensePieChartWidget()
        chart_main_layout.addWidget(self.pie_chart)
        
        main_layout.addWidget(self.chart_container)
        self.setLayout(main_layout)

    # --- LOGIKA NAVIGASI ---
    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.refresh_statistics()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.refresh_statistics()

    def refresh_statistics(self):
        """Memperbarui visual data kartu ringkasan dan grafik secara serentak"""
        if self.user_id is None:
            return

        bulan = self.current_date.month()
        tahun = self.current_date.year()
        self.labelBulan.setText(self.current_date.toString("MMMM yyyy"))
        
        # 1. Ambil Nilai Card 1: Total Pengeluaran 
        try:
            total = self.db.get_total_monthly(self.user_id, bulan, tahun)
            if total is None:
                total = 0
            self.val_total.setText(f"Rp {total:,.0f}".replace(",", "."))
        except Exception as e:
            print(f"Error mengambil total bulanan: {e}")
            self.val_total.setText("Rp 0")
        
        # 2. Ambil Nilai Card 2: Jumlah Transaksi Bulanan
        try:
            expenses_data = self.db.get_expenses_by_month(self.user_id, bulan, tahun)
            total_transaksi = len(expenses_data) if expenses_data else 0
            self.val_count.setText(f"{total_transaksi} Transaksi")
        except Exception as e:
            print(f"Error menghitung jumlah transaksi: {e}")
            self.val_count.setText("0 Transaksi")
        
        # 3. Ambil Nilai Card 3: Kategori Dominan via DataFrame Pandas
        df = self.db.get_category_data_df(self.user_id, bulan, tahun)
        
        if df is not None and not df.empty:
            try:
                # Cari secara dinamis nama kolom agregasi nominal
                kolom_nominal = None
                for col in df.columns:
                    if col != 'nama_kategori':
                        kolom_nominal = col
                        break
                
                if kolom_nominal and kolom_nominal in df.columns:
                    id_maksimum = df[kolom_nominal].idxmax()
                    kategori_terbesar = df.loc[id_maksimum, 'nama_kategori']
                    self.val_dominant.setText(str(kategori_terbesar))
                else:
                    self.val_dominant.setText("-")
            except Exception as e:
                print(f"Error mencari kategori dominan: {e}")
                self.val_dominant.setText("-")
        else:
            self.val_dominant.setText("-")
        
        # 4. Perbarui Visualisasi Grafik Donut Matplotlib
        try:
            self.pie_chart.plot(df, f"Distribusi Kategori - {self.current_date.toString('MMMM yyyy')}")
        except Exception as e:
            print(f"Error merender grafik: {e}")

    def buat_efek_shadow(self, parent_widget):
            shadow = QGraphicsDropShadowEffect(parent_widget)
            shadow.setBlurRadius(15)                      # Kelembutan bayangan
            shadow.setXOffset(0)                          # Posisi bayangan X
            shadow.setYOffset(4)                          # Posisi bayangan Y (Turun ke bawah)
            shadow.setColor(QColor(0, 0, 0, 35))          # Warna hitam transparan (Alpha 35 dari 255)
            parent_widget.setGraphicsEffect(shadow)