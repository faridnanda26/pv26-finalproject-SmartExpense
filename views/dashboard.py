from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QMessageBox, QTableWidget, QDialog,
    QTableWidgetItem, QHeaderView, QComboBox, QFrame, QDateEdit
)
from PySide6.QtCore import Qt, QDate, Signal
from custom_dialog.dialogs import ExpenseInputDialog

class Dashboard(QWidget):

    go_to_stat = Signal()

    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.user_id = None
        self.selected_id = None
        self.user_nama = ""
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("dashboardPage")
        self.init_ui()

    def set_user_session(self, user_id, user_nama):
        """Menerima data user dari MainWindow setelah login sukses"""
        self.user_id = user_id
        self.user_nama = user_nama
        self.load_data()
        self.lblWelcome.setText(f"Selamat Datang, {self.user_nama} 👋")

    def init_ui(self):
        layout = QVBoxLayout(self) 
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Label selamat datang
        self.lblWelcome = QLabel(f"Selamat Datang, {self.user_nama} 👋")
        self.lblWelcome.setObjectName("welcomeLabel")
        layout.addWidget(self.lblWelcome)

        # Container untuk area pencarian & tombol (Toolbar)
        self.toolbar_frame = QFrame()
        self.toolbar_frame.setObjectName("toolbarFrame")
        toolbar_layout = QHBoxLayout(self.toolbar_frame)

        # Search bar
        self.leCari = QLineEdit()
        self.leCari.setObjectName("searchBar")
        self.leCari.setPlaceholderText('🔍 Cari tanggal, deskripsi, atau kategori...')
        self.leCari.textChanged.connect(self.cari_pengeluaran)
        toolbar_layout.addWidget(self.leCari)

        # Button CRUD
        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Tambah")
        self.btnAdd.clicked.connect(self.tambah_pengeluaran)
        self.btnAdd.setObjectName("btnAdd")
        
        self.btnUpdate = QPushButton("Edit")
        self.btnUpdate.clicked.connect(self.edit_pengeluaran)
        self.btnUpdate.setObjectName("btnUpdate")
        
        self.btnDelete = QPushButton("Hapus")
        self.btnDelete.clicked.connect(self.hapus_pengeluaran)
        self.btnDelete.setObjectName("btnDelete")
        
        btn_layout.addWidget(self.btnAdd)
        btn_layout.addWidget(self.btnUpdate)
        btn_layout.addWidget(self.btnDelete)
        
        toolbar_layout.addLayout(btn_layout)
        layout.addWidget(self.toolbar_frame)

        # Navigasi Bulan
        self.current_date = QDate.currentDate() 
        
        self.nav_layout = QHBoxLayout()
        
        # Tombol Prev
        self.btnPrev = QPushButton(" < ")
        self.btnPrev.setObjectName("btnNavMonth") 
        self.btnPrev.setFixedSize(30, 30)
        self.btnPrev.clicked.connect(self.prev_month)
        
        # Label Bulan
        self.labelBulan = QLabel(self.current_date.toString("MMMM yyyy"))
        self.labelBulan.setObjectName("labelBulan") 
        self.labelBulan.setAlignment(Qt.AlignCenter)
        
        # Tombol Next
        self.btnNext = QPushButton(" > ")
        self.btnNext.setObjectName("btnNavMonth") 
        self.btnNext.setFixedSize(30, 30)
        self.btnNext.clicked.connect(self.next_month)
        
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.btnPrev)
        self.nav_layout.addWidget(self.labelBulan)
        self.nav_layout.addWidget(self.btnNext)
        self.nav_layout.addStretch()
        
        layout.addLayout(self.nav_layout)

        # Tabel pengeluaran
        self.table = QTableWidget()  
        self.table.setObjectName("expenseTable")
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(["ID", "Nominal", "Kategori", "Deskripsi", "Tanggal"])
        
        self.table.verticalHeader().setDefaultSectionSize(40) 
        self.table.verticalHeader().setVisible(False)

        # PENGATURAN LEBAR KOLOM 
        header = self.table.horizontalHeader()
        
        # ID, Nominal, Kategori, dan Tanggal dibuat pas dengan isinya (ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # Deskripsi dibuat fleksibel memenuhi sisa ruang (Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        header.setStretchLastSection(False)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.clicked.connect(self.id_selection)

        layout.addWidget(self.table)

        stat_layout = QHBoxLayout()
        self.btnStatistik = QPushButton('Statistik ->')
        self.btnStatistik.setObjectName("btnStatistik")
        self.btnStatistik.clicked.connect(self.go_to_stat.emit)

        stat_layout.addStretch() 
        stat_layout.addWidget(self.btnStatistik)

        layout.addLayout(stat_layout)
        self.setLayout(layout)

    def id_selection(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text()) # Menangkap id data yang di select

    def load_data(self):
        """Logika pusat untuk memperbarui label bulan dan isi tabel"""
        # 1. Update teks label bulan (misal: "Mei 2026")
        self.labelBulan.setText(self.current_date.toString("MMMM yyyy"))
        
        # 2. Ambil parameter bulan dan tahun dari state current_date
        bulan = self.current_date.month()
        tahun = self.current_date.year()
        
        # 3. Ambil data spesifik bulan tersebut dari DB
        data = self.db.get_expenses_by_month(self.user_id, bulan, tahun)
        
        # 4. Tampilkan ke tabel
        self.show_to_table(data)

    # masukkan ke tabel
    def show_to_table(self, data):
        self.table.setRowCount(0)
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
            try:
                nominal_val = float(row_data['nominal'])
                formatted_nominal = f"Rp {nominal_val:,.0f}".replace(",", ".")
            except:
                formatted_nominal = str(row_data['nominal'])
                
            self.table.setItem(row, 1, QTableWidgetItem(formatted_nominal))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data['nama_kategori'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(row_data['deskripsi'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(row_data['tanggal'])))
            self.table.item(row, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def tambah_pengeluaran(self):
        dialog = ExpenseInputDialog(self.db, self) 
        
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                success, message = self.db.add_expense(
                    self.user_id, 
                    data["kategori_id"], 
                    float(data["nominal"]), 
                    data["deskripsi"], 
                    data["tanggal"] # Formatnya "YYYY-MM-DD"
                )
                
                if success:
                    # 1. Konversi string tanggal dari input ke objek QDate
                    # Pastikan format "yyyy-MM-dd" sesuai dengan yang dikirim dialog
                    new_date = QDate.fromString(data["tanggal"], "yyyy-MM-dd")
                    
                    if new_date.isValid():
                        # 2. Ubah current_date dashboard ke tanggal baru tersebut
                        self.current_date = new_date
                    
                    QMessageBox.information(self, "Berhasil", "Data pengeluaran berhasil disimpan!")
                    
                    # 3. Refresh tabel (load_data sekarang akan memuat bulan dari data baru)
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Gagal", message)
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")

    def hapus_pengeluaran(self):
        # 1. Cek apakah ada baris yang dipilih
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            QMessageBox.warning(
                self, 
                "Peringatan",
                "Silakan pilih baris data yang ingin dihapus terlebih dahulu."
            )
            return
        
        # 2. Konfirmasi penghapusan
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Konfirmasi Hapus")
        msg_box.setText("Apakah Anda yakin ingin menghapus data ini?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            # 3. Eksekusi hapus di database
            success = self.db.delete_expense(self.selected_id)
            
            if success:
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
                # 4. Reset selected_id dan refresh tabel
                self.selected_id = None 
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus data dari database.")

    def cari_pengeluaran(self, text):
        if text.strip():
            # Cari data berdasarkan keyword
            searched_data = self.db.find_expense(self.user_id, text)
            self.show_to_table(searched_data)
        else:
            # Jika kosong, kembali tampilkan semua data milik user
            self.load_data()

    def edit_pengeluaran(self):
        if not self.selected_id: # cek id yang di select
            QMessageBox.warning(
                self, 
                "Warning",
                "Pilih Pengeluaran yang Ingin di Edit"
            )
            return
        
        data = self.db.find_expense(self.user_id, self.selected_id) # cari data yg mau di update
        data_dict = data[0]

        dialog = ExpenseInputDialog(self.db, self, data_dict)
        
        if dialog.exec() == QDialog.Accepted:
            data_dialog = dialog.get_data()
            try:
                self.db.update_expense(
                    data_dict["id"], 
                    data_dialog["kategori_id"], 
                    data_dialog["nominal"], 
                    data_dialog["deskripsi"], 
                    data_dialog["tanggal"]
                )
                QMessageBox.information(self, "Sukses", "Data berhasil diperbarui!")
                self.selected_id = None
                self.load_data()
            
            except Exception as e:
                QMessageBox.critical(self, "System Error", f"An unexpected error occurred: {str(e)}")

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.load_data()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.load_data()