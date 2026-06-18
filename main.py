import sys
import os
from PySide6.QtWidgets import QApplication

from database.db_manager import DatabaseManager
from views.main_window import MainWindow
from views.splash_screen import SplashScreen 

def load_stylesheet(app, filepath):
    """Menerapkan QSS ke aplikasi jika file ditemukan."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Gagal membaca file QSS: {e}")
    else:
        print(f"Peringatan: File {filepath} tidak ditemukan. Menggunakan tema default.")

def main():
    # 1. Inisialisasi Aplikasi
    app = QApplication(sys.argv)
    
    # 2. Path Konfigurasi
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "assets", "style.qss")

    # 3. Terapkan Stylesheet 
    load_stylesheet(app, qss_path)
    
    # 4. Inisialisasi Database
    db = DatabaseManager('ExpenseTracker.db')
    
    # 5. Inisialisasi Window Utama 
    window = MainWindow(db)
    
    # 6. Jalankan Splash Screen 
    splash = SplashScreen()
    splash.showFullScreen()
    
    # Logika Interseptor: Jalankan MainWindow HANYA setelah animasi splash selesai
    splash.animasi_selesai.connect(window.showFullScreen)
    
    # 7. Main Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()