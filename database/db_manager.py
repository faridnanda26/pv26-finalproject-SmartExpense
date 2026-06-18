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
        Return: (True/False)
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
        
    def get_all_categories(self):
        """
        Mengambil semua daftar kategori dari tabel kategori.
        Return: List of sqlite3.Row (berisi id dan nama_kategori)
        """
        try:
            with self.get_connection() as conn:
                # Ambil id untuk data transaksi dan nama untuk tampilan UI
                cursor = conn.execute('SELECT id, nama_kategori FROM kategori ORDER BY nama_kategori ASC')
                return cursor.fetchall()
        except Exception as e:
            print(f"Error get_all_categories: {e}")
            return []
        
    def add_expense(self, user_id, kategori_id, nominal, deskripsi, tanggal):
        """
        Menyimpan data transaksi pengeluaran baru ke database.
        """
        try:
            with self.get_connection() as conn:
                query = '''
                    INSERT INTO pengeluaran (user_id, kategori_id, nominal, deskripsi, tanggal)
                    VALUES (?, ?, ?, ?, ?)
                '''
                # Mengeksekusi perintah insert
                conn.execute(query, (user_id, kategori_id, nominal, deskripsi, tanggal))
                
                # Commit wajib dilakukan untuk menyimpan perubahan secara permanen
                conn.commit()
                return True, "Data pengeluaran berhasil disimpan."
                
        except Exception as e:
            # Mengembalikan pesan error jika terjadi kegagalan (misal: database locked)
            return False, f"Gagal menyimpan data: {str(e)}"
        
    def delete_expense(self, expense_id):
        """Menghapus satu baris pengeluaran berdasarkan ID"""
        try:
            with self.get_connection() as conn:
                query = "DELETE FROM pengeluaran WHERE id = ?"
                conn.execute(query, (expense_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error delete_expense: {e}")
            return False
        
    def find_expense(self, user_id, key):
        """Mencari data berdasarkan ID, deskripsi, kategori, atau tanggal"""
        try:
            with self.get_connection() as conn:
                query = '''
                    SELECT p.id, p.tanggal, k.nama_kategori, p.nominal, p.deskripsi, p.kategori_id
                    FROM pengeluaran p
                    INNER JOIN kategori k ON p.kategori_id = k.id
                    WHERE p.user_id = ? AND (
                        CAST(p.id AS TEXT) LIKE ? OR 
                        p.deskripsi LIKE ? OR 
                        k.nama_kategori LIKE ? OR 
                        p.tanggal LIKE ?
                    )
                    ORDER BY p.tanggal DESC
                '''
                wildcard = f"%{key}%"
                # Karena ada 4 tanda tanya (?) di dalam kurung, kita kirim wildcard 4 kali
                cursor = conn.execute(query, (user_id, wildcard, wildcard, wildcard, wildcard))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error search: {e}")
            return []
        
    def update_expense(self, expense_id, kategori_id, nominal, deskripsi, tanggal):
        """Memperbarui data pengeluaran yang sudah ada"""
        try:
            with self.get_connection() as conn:
                query = '''
                    UPDATE pengeluaran 
                    SET kategori_id = ?, nominal = ?, deskripsi = ?, tanggal = ?
                    WHERE id = ?
                '''
                conn.execute(query, (kategori_id, nominal, deskripsi, tanggal, expense_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error update_expense: {e}")
            return False
        
    def get_expenses_by_month(self, user_id, bulan, tahun):
        try:
            with self.get_connection() as conn:
                bulan_str = str(bulan).zfill(2)
                tahun_str = str(tahun)
                
                query = '''
                    SELECT p.id, p.tanggal, k.nama_kategori, p.nominal, p.deskripsi, p.kategori_id
                    FROM pengeluaran p
                    INNER JOIN kategori k ON p.kategori_id = k.id
                    WHERE p.user_id = ? 
                    AND strftime('%m', p.tanggal) = ? 
                    AND strftime('%Y', p.tanggal) = ?
                    ORDER BY p.tanggal DESC
                '''
                cursor = conn.execute(query, (user_id, bulan_str, tahun_str))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error get_month: {e}")
            return []
        
    def get_all_expenses_by_user(self, user_id):
        query = """
            SELECT p.tanggal, k.nama_kategori, p.nominal, p.deskripsi
            FROM pengeluaran p
            JOIN kategori k ON p.kategori_id = k.id
            WHERE p.user_id = ?
            ORDER BY p.tanggal DESC
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, (user_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Database Error (Export): {e}")
            return []
        
    def get_category_data_df(self, user_id, month, year):
        """
        Mengambil data kategori dan mengembalikannya dalam bentuk Pandas DataFrame
        untuk kebutuhan grafik/statistik.
        """
        query = '''
            SELECT k.nama_kategori, SUM(p.nominal) as total
            FROM pengeluaran p
            JOIN kategori k ON p.kategori_id = k.id
            WHERE p.user_id = ? 
            AND strftime('%m', p.tanggal) = ? 
            AND strftime('%Y', p.tanggal) = ?
            GROUP BY k.nama_kategori
            ORDER BY total DESC
        '''
        
        bulan_str = str(month).zfill(2)
        tahun_str = str(year)

        try:
            # Gunakan context manager koneksi
            with self.get_connection() as conn:
                df = pd.read_sql(query, conn, params=(user_id, bulan_str, tahun_str))
                return df
        except Exception as e:
            print(f"Error Database Stats: {e}")
            return pd.DataFrame() # Kembalikan DF kosong jika gagal
        
    def get_total_monthly(self, user_id, month, year):
        query = '''
            SELECT SUM(nominal) 
            FROM pengeluaran 
            WHERE user_id = ? 
            AND strftime('%m', tanggal) = ? 
            AND strftime('%Y', tanggal) = ?
        '''
        bulan_str = str(month).zfill(2)
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, (user_id, bulan_str, str(year)))
                result = cursor.fetchone()
                return result[0] if result[0] else 0
        except Exception as e:
            print(f"Error total: {e}")
            return 0