import sqlite3
# üyelik veritabanı bağlantısını oluştur

class Kullanici:
    def __init__(self):
        
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Kullanici_Adi TEXT NOT NULL,
                                Kullanici_Soyadi TEXT NOT NULL,
                                Sifre TEXT NOT NULL
                                )''')

    def kaydet(self, kullanici_adi, kullanici_soyadi, sifre):
        # Her işlemde yeni bağlantı ve cursor kullan
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kullanicilar (Kullanici_Adi, Kullanici_Soyadi, Sifre) VALUES (?, ?, ?)",
                           (kullanici_adi, kullanici_soyadi, sifre))
            conn.commit()

    @staticmethod
    def kullanici_var_mi(kullanici_adi, kullanici_sifre):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE Kullanici_Adi=? and Sifre=?", (kullanici_adi, kullanici_sifre))
            return cursor.fetchone() is not None
    def kullanici_bilgileri_getir(self, kullanici_adi):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE Kullanici_Adi=?", (kullanici_adi,))
            return cursor.fetchone()
    def toplam_uye_sayisi(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM kullanicilar")
            return cursor.fetchone()[0]
# kullanıcının siparis veri tabanı

class kullanıcı_siparisleri:
    def __init__(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS siparisler
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Kullanici_Adi TEXT NOT NULL,
                                Siparis TEXT NOT NULL,
                                Tarih   DATETIME NOT NULL,
                                DURUM CHAR(20) NOT NULL,
                                HARCAMA INTEGER NOT NULL,
                                FOREIGN KEY (Kullanici_Adi) REFERENCES kullanicilar(Kullanici_Adi)
                                )''')

    def siparis_ekle(self, kullanici_adi, siparis,tarih,durum,HARCAMA):
         try:
          with sqlite3.connect('kafe.db', timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO siparisler (Kullanici_Adi, Siparis, Tarih, DURUM, HARCAMA)
                VALUES (?, ?, ?, ?, ?)''',
                (kullanici_adi, siparis, tarih, durum, HARCAMA))
            conn.commit()
         except sqlite3.OperationalError as e:
             print("Veritabanı hatası:", e)
    def siparisleri_getir(self, kullanici_adi):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Siparis,Tarih,Durum FROM siparisler WHERE Kullanici_Adi=?", (kullanici_adi,))
            return cursor.fetchall()
    def siparis_sil(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            siparis_var_mi=cursor.execute("select count(*) from siparisler").fetchone()[0]
            if siparis_var_mi==0:
                return 0
            siparis_beklemede_mi=cursor.execute(
        "SELECT DURUM FROM siparisler WHERE id = (SELECT id FROM siparisler ORDER BY id DESC LIMIT 1)"
    ).fetchone()[0]
            if siparis_beklemede_mi!="beklemede":
                return 0
            cursor.execute("DELETE FROM siparisler WHERE id = (SELECT id FROM siparisler ORDER BY id DESC LIMIT 1)")
            return 1
    def toplam_harcama(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT SUM(HARCAMA) FROM siparisler").fetchone()[0]
    def toplam_fiyat(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            return cursor.execute("SELECT HARCAMA FROM siparisler WHERE DURUM='beklemede'").fetchone()[0]

        
    def bekleyen(selfs):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            beklenen_siparisler=cursor.execute("SELECT COUNT(DURUM) FROM siparisler where DURUM = 'beklemede' ").fetchone()[0]
            tum_siparisler=cursor.execute("SELECT COUNT(DURUM) FROM siparisler ").fetchone()[0]
            tamamlanan_siparisler=int(tum_siparisler)-int(beklenen_siparisler) 
            if tamamlanan_siparisler<0: tamamlanan_siparisler=0
            return beklenen_siparisler,tamamlanan_siparisler,tum_siparisler
    


             
        


import sqlite3

class GREEN_MONEY:
    def __init__(self):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS GREEN_MONEY (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Kullanici_Adi TEXT NOT NULL,
                    MONEY INTEGER NOT NULL,
                    SIFRE TEXT NOT NULL,
                    FOREIGN KEY (Kullanici_Adi) REFERENCES kullanicilar(Kullanici_Adi)
                )
            """)

    def money_insert(self, kullanici_adi,sifre, artis):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE GREEN_MONEY SET MONEY = MONEY + ? WHERE Kullanici_Adi = ? AND SIFRE=?", 
                (10 * artis, kullanici_adi,sifre)
            )
            conn.commit()

    def money_show(self, kullanici_adi,sifre):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                "SELECT MONEY FROM GREEN_MONEY WHERE Kullanici_Adi = ? AND SIFRE=?", 
                (kullanici_adi,sifre,)
            ).fetchone()
            if result:
                return result[0]
            else:
                return None  

    def money_using(self, kullanici_adi,sifre, harcama):
        with sqlite3.connect('kafe.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE GREEN_MONEY SET MONEY = MONEY - ? WHERE Kullanici_Adi = ? AND SIFRE=?", 
                (harcama, kullanici_adi,sifre)
            )
            conn.commit()
    def user_insert(self,kullanici_adi,sifre):
        
     with sqlite3.connect('kafe.db') as conn:
        cursor = conn.cursor()

        # Önce kullanıcı var mı kontrol et
        cursor.execute("SELECT 1 FROM GREEN_MONEY WHERE Kullanici_Adi = ?", (kullanici_adi,))
        if cursor.fetchone():
            print("Bu kullanıcı zaten var.")
            return False
        
        # Yoksa ekle
        cursor.execute(
            "INSERT INTO GREEN_MONEY (Kullanici_Adi, SIFRE, MONEY) VALUES (?, ?, ?)",
            (kullanici_adi, sifre, 0)
        )
        conn.commit()
        return True
