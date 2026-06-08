import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name='ExpenseTracker.db'):
        self.db_name = db_name
        self.create_tables()
        self.add_kategori()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        # Mengaktifkan foreign key agar relasi antar tabel bekerja
        conn.execute('PRAGMA foreign_keys = ON')
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        with self.get_connection() as conn:
            # 1. Tabel Users
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    nama_lengkap TEXT
                )
            ''')
            
            # 2. Tabel Kategori
            conn.execute('''
                CREATE TABLE IF NOT EXISTS kategori (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_kategori TEXT NOT NULL UNIQUE
                )
            ''')
            
            # 3. Tabel Pengeluaran (Relasi ke Users dan Kategori)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pengeluaran (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    kategori_id INTEGER,
                    nominal REAL NOT NULL,
                    deskripsi TEXT,
                    tanggal TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (kategori_id) REFERENCES kategori(id) ON DELETE SET NULL
                )
            ''')

    def add_kategori(self):
        """Memasukkan kategori default ke database."""
        kategori_default = [
            ('Makanan',),
            ('Minuman',),
            ('Pakaian',),
            ('Transportasi',),
            ('Hiburan',),
            ('Tagihan & Listrik',),
            ('Edukasi',),
            ('Kesehatan',)
        ]
        
        with self.get_connection() as conn:
            conn.executemany(
                'INSERT OR IGNORE INTO kategori (nama_kategori) VALUES (?)', 
                kategori_default
            )
            conn.commit() 

    def check_login(self, username, password):
        """
        Memverifikasi login pengguna.
        Return: sqlite3.Row object jika sukses, None jika gagal.
        """
        try:
            with self.get_connection() as conn:
                # Menggunakan baris (Row) agar bisa diakses lewat nama kolom
                cursor = conn.execute(
                    'SELECT id, username, nama_lengkap FROM users WHERE username = ? AND password = ?',
                    (username, password)
                )
                return cursor.fetchone()
        except Exception as e:
            print(f"Error pada check_login: {e}")
            return None
        
    def register_user(self, username, password, nama):
        """
        Mendaftarkan user baru ke tabel users.
        Return: (True/False, pesan_error/sukses)
        """
        try:
            with self.get_connection() as conn:
                # 1. Jalankan query insert
                conn.execute(
                    'INSERT INTO users (username, password, nama_lengkap) VALUES (?, ?, ?)',
                    (username, password, nama)
                )
                # 2. Simpan perubahan secara permanen
                conn.commit()
                return True, "Akun berhasil dibuat!"
                
        except sqlite3.IntegrityError:
            # Error ini muncul jika username sudah ada (karena constraint UNIQUE)
            return False, "Username sudah digunakan, silakan pilih yang lain."
            
        except Exception as e:
            # Error lainnya (masalah koneksi, database terkunci, dll)
            return False, f"Terjadi kesalahan: {str(e)}"