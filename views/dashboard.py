from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QMessageBox, QTableWidget, QDialog,
    QTableWidgetItem, QHeaderView, QFrame
)
from PySide6.QtCore import Qt, QDate
from custom_dialog.dialogs import ExpenseInputDialog

class Dashboard(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.user_id = None
        self.selected_id = None
        self.user_nama = ""

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("contentArea") 
        self.init_ui()

    def set_user_session(self, user_id, user_nama):
        """Menerima data user dari MainWindow setelah login sukses"""
        self.user_id = user_id
        self.user_nama = user_nama
        self.load_data()
        self.lblWelcome.setText(f"Selamat Datang, {self.user_nama} 👋")

    def init_ui(self):
        # Layout Utama Vertikal Konten
        content_layout = QVBoxLayout(self)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(15)

        # Header: Label selamat datang
        self.lblWelcome = QLabel(f"Selamat Datang, {self.user_nama} 👋")
        self.lblWelcome.setObjectName("welcomeLabel")
        content_layout.addWidget(self.lblWelcome)

        # Card Toolbar (Pencarian & Aksi CRUD)
        self.toolbar_frame = QFrame()
        self.toolbar_frame.setObjectName("toolbarFrame")
        toolbar_layout = QHBoxLayout(self.toolbar_frame)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)

        # Search bar
        self.leCari = QLineEdit()
        self.leCari.setObjectName("searchBar")
        self.leCari.setPlaceholderText('🔍 Cari tanggal, deskripsi, atau kategori...')
        self.leCari.textChanged.connect(self.cari_pengeluaran)
        toolbar_layout.addWidget(self.leCari)

        # Button CRUD Layout
        btn_layout = QHBoxLayout()
        self.btnAdd = QPushButton("Tambah")
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.setCursor(Qt.PointingHandCursor)
        self.btnAdd.clicked.connect(self.tambah_pengeluaran)
        
        self.btnUpdate = QPushButton("Edit")
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnUpdate.setCursor(Qt.PointingHandCursor)
        self.btnUpdate.clicked.connect(self.edit_pengeluaran)
        
        self.btnDelete = QPushButton("Hapus")
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setCursor(Qt.PointingHandCursor)
        self.btnDelete.clicked.connect(self.hapus_pengeluaran)
        
        btn_layout.addWidget(self.btnAdd)
        btn_layout.addWidget(self.btnUpdate)
        btn_layout.addWidget(self.btnDelete)
        
        toolbar_layout.addLayout(btn_layout)
        content_layout.addWidget(self.toolbar_frame)

        # Navigasi Paginasi Bulan
        self.current_date = QDate.currentDate() 
        self.nav_frame = QFrame()
        self.nav_frame.setObjectName("navFrameDashboard")
        
        nav_layout = QHBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(10, 5, 10, 5)

        # Tombol Pasif Prev (<)
        self.btnPrev = QPushButton(" < ")
        self.btnPrev.setObjectName("btnNavMonthDash") 
        self.btnPrev.setFixedSize(30, 30)
        self.btnPrev.setCursor(Qt.PointingHandCursor)
        self.btnPrev.clicked.connect(self.prev_month)
        
        # Label Nama Bulan
        self.labelBulan = QLabel(self.current_date.toString("MMMM yyyy"))
        self.labelBulan.setObjectName("labelBulanDash") 
        self.labelBulan.setAlignment(Qt.AlignCenter)
        self.labelBulan.setFixedWidth(200)
        
        # Tombol Pasif Next (>)
        self.btnNext = QPushButton(" > ")
        self.btnNext.setObjectName("btnNavMonthDash") 
        self.btnNext.setFixedSize(30, 30)
        self.btnNext.setCursor(Qt.PointingHandCursor)
        self.btnNext.clicked.connect(self.next_month)
        
        nav_layout.addStretch()
        nav_layout.addWidget(self.btnPrev)
        nav_layout.addWidget(self.labelBulan)
        nav_layout.addWidget(self.btnNext)
        nav_layout.addStretch()
        
        # Penyeimbang Kapsul Navigasi agar presisi di tengah layar
        center_nav_layout = QHBoxLayout()
        center_nav_layout.addStretch()
        center_nav_layout.addWidget(self.nav_frame)
        center_nav_layout.addStretch()
        
        content_layout.addLayout(center_nav_layout)

        # Tabel Pengeluaran Utama
        self.table = QTableWidget()  
        self.table.setObjectName("expenseTable")
        self.table.setColumnCount(5) 
        self.table.setHorizontalHeaderLabels(["ID", "Nominal", "Kategori", "Deskripsi", "Tanggal"])
        self.table.verticalHeader().setDefaultSectionSize(40) 
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setStretchLastSection(False)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.clicked.connect(self.id_selection)

        content_layout.addWidget(self.table)

    def id_selection(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())

    def load_data(self):
        """Logika pusat untuk memperbarui label bulan dan isi tabel"""
        self.labelBulan.setText(self.current_date.toString("MMMM yyyy"))
        bulan = self.current_date.month()
        tahun = self.current_date.year()
        data = self.db.get_expenses_by_month(self.user_id, bulan, tahun)
        self.show_to_table(data)

    def show_to_table(self, data):
        """Merender baris data SQLite ke tabel"""
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            item_id = QTableWidgetItem(str(row_data['id']))
            try:
                nominal_val = float(row_data['nominal'])
                formatted_nominal = f"Rp {nominal_val:,.0f}".replace(",", ".")
            except:
                formatted_nominal = str(row_data['nominal'])
                
            item_nominal = QTableWidgetItem(formatted_nominal)
            item_kategori = QTableWidgetItem(str(row_data['nama_kategori']))
            item_deskripsi = QTableWidgetItem(str(row_data['deskripsi']))
            item_tanggal = QTableWidgetItem(str(row_data['tanggal']))
            
            # Mematikan pemicu input editor ketik di dalam sel tabel secara total
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
            item_id.setFlags(flags)
            item_nominal.setFlags(flags)
            item_kategori.setFlags(flags)
            item_deskripsi.setFlags(flags)
            item_tanggal.setFlags(flags)

            self.table.setItem(row, 0, item_id)
            self.table.setItem(row, 1, item_nominal)
            self.table.setItem(row, 2, item_kategori)
            self.table.setItem(row, 3, item_deskripsi)
            self.table.setItem(row, 4, item_tanggal)
            self.table.item(row, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def tambah_pengeluaran(self):
        dialog = ExpenseInputDialog(self.db, self) 
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            try:
                success, message = self.db.add_expense(
                    self.user_id, data["kategori_id"], float(data["nominal"]), data["deskripsi"], data["tanggal"]
                )
                if success:
                    new_date = QDate.fromString(data["tanggal"], "yyyy-MM-dd")
                    if new_date.isValid():
                        self.current_date = new_date
                    QMessageBox.information(self, "Berhasil", "Data pengeluaran berhasil disimpan!")
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Gagal", message)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan: {str(e)}")

    def hapus_pengeluaran(self):
        if not hasattr(self, 'selected_id') or self.selected_id is None:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih baris data yang ingin dihapus terlebih dahulu.")
            return
        
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Konfirmasi Hapus")
        msg_box.setText("Apakah Anda yakin ingin menghapus data ini?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg_box.exec() == QMessageBox.Yes:
            if self.db.delete_expense(self.selected_id):
                QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
                self.selected_id = None 
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", "Gagal menghapus data dari database.")

    def cari_pengeluaran(self, text):
        if text.strip():
            searched_data = self.db.find_expense(self.user_id, text)
            self.show_to_table(searched_data)
        else:
            self.load_data()

    def edit_pengeluaran(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Warning", "Pilih Pengeluaran yang Ingin di Edit")
            return
        
        data = self.db.find_expense(self.user_id, self.selected_id)
        data_dict = data[0]
        dialog = ExpenseInputDialog(self.db, self, data_dict)
        
        if dialog.exec() == QDialog.Accepted:
            data_dialog = dialog.get_data()
            try:
                self.db.update_expense(
                    data_dict["id"], data_dialog["kategori_id"], data_dialog["nominal"], data_dialog["deskripsi"], data_dialog["tanggal"]
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