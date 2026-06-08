class Validator:
    
    @staticmethod
    def validasi_username(username):
        """Return (True/False, pesan_error)"""
        if not username:
            return False, "Username tidak boleh kosong"
        if len(username) < 4:
            return False, "Username minimal 4 karakter"
        if " " in username:
            return False, "Username tidak boleh mengandung spasi"
        return True, ""
    
    @staticmethod
    def validasi_password(password):
        """Return (True/False, pesan_error)"""
        if not password:
            return False, "Password tidak boleh kosong"
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
        return True, ""
    
    @staticmethod
    def validasi_nama(nama):
        """Return (True/False, pesan_error)"""
        # 1. Cek apakah kosong
        if not nama or len(nama.strip()) == 0:
            return False, "Nama lengkap tidak boleh kosong"
        
        # 2. Cek panjang minimal (misal 3 karakter)
        if len(nama) < 3:
            return False, "Nama lengkap minimal 3 karakter"
        
        # 3. Cek panjang maksimal (opsional, misal 50 karakter)
        if len(nama) > 50:
            return False, "Nama lengkap terlalu panjang (maksimal 50 karakter)"
            
        # 4. Cek apakah mengandung angka (Opsional, nama biasanya hanya huruf & spasi)
        # Gunakan list comprehension untuk cek setiap karakter
        if any(char.isdigit() for char in nama):
            return False, "Nama tidak boleh mengandung angka"
            
        return True, ""