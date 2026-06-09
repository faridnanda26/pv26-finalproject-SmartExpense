from PySide6.QtWidgets import (
    QVBoxLayout, QDialog, QDialogButtonBox,
    QLineEdit, QComboBox, QSpinBox, QFormLayout,
    QTimeEdit, QMessageBox, QDateEdit
)

from PySide6.QtCore import Qt, QDate  

from logic.validator import Validator

# Dialog input data
class ExpenseInputDialog(QDialog):
    def __init__(self, db, parent=None, data_edit=None):
        super().__init__(parent)
        self.db = db
        self.data_edit = data_edit
        self.setWindowTitle("Tambah Pengeluaran")
        self.setMinimumWidth(400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # 1. Nominal 
        self.nominal_input = QLineEdit()
        self.nominal_input.setPlaceholderText("Contoh: 50000")
        form_layout.addRow("Nominal:", self.nominal_input)

        # 2. Kategori 
        self.items = self.db.get_all_categories()
        self.kategori_input = QComboBox()
        for row in self.items:
            self.kategori_input.addItem(row['nama_kategori'], row['id'])
        form_layout.addRow("Kategori:", self.kategori_input)

        # 3. Deskripsi / Keterangan
        self.deskripsi_input = QLineEdit()
        self.deskripsi_input.setPlaceholderText("Makan siang, bensin, dll.")
        form_layout.addRow("Keterangan:", self.deskripsi_input)

        # 4. Tanggal
        self.tanggal_input = QDateEdit()
        self.tanggal_input.setCalendarPopup(True) # Menampilkan kalender saat diklik
        self.tanggal_input.setDate(QDate.currentDate()) # Set otomatis ke tanggal hari ini
        self.tanggal_input.setDisplayFormat("dd/MM/yyyy") # Format tampilan di UI
        form_layout.addRow("Tanggal:", self.tanggal_input)
        
        # Tambahkan form_layout ke layout utama
        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

        if self.data_edit:
            # 1. Isi Nominal
            self.nominal_input.setText(str(int(self.data_edit['nominal'])))

            # 2. Isi Deskripsi
            self.deskripsi_input.setText(self.data_edit['deskripsi'])

            # 3. Isi Tanggal 
            tanggal_db = self.data_edit['tanggal'] 
            self.tanggal_input.setDate(QDate.fromString(tanggal_db, "yyyy-MM-dd")) 

            # 4. Pilih Kategori
            id_kategori = self.data_edit['kategori_id']
            idx = self.kategori_input.findData(id_kategori)
            if idx >= 0:
                self.kategori_input.setCurrentIndex(idx)

    # Validasi data yang diinputkan
    def validate_and_accept(self):
        valid, error = Validator.validasi_nominal(self.nominal_input.text())

        if not valid:
            QMessageBox.warning(
                self,
                "Warning",
                error
            )
            self.nominal_input.setFocus()
            return
        
        self.accept() # close dengan status accept bila valid

    # Mengambil data yang diinputkan
    def get_data(self):
        return {
            "nominal": self.nominal_input.text().strip(),
            "kategori_id": self.kategori_input.currentData(), 
            "deskripsi": self.deskripsi_input.text().strip(),
            "tanggal": self.tanggal_input.date().toString("yyyy-MM-dd")
        }