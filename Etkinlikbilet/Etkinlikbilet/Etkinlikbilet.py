import os
import datetime
import time
import uuid


class Etkinlik:
    def __init__(self, id, isim, tarih, yer, toplam_koltuk, bilet_fiyati):
        self.id = id
        self.isim = isim
        self.tarih = tarih
        self.yer = yer
        self.toplam_koltuk = toplam_koltuk
        self.kalan_koltuk = toplam_koltuk
        self.bilet_fiyati = bilet_fiyati
        self.satilan_biletler = []

    def __str__(self):
        return f"{self.id}) {self.isim} - {self.tarih} - {self.yer} - Kalan koltuk: {self.kalan_koltuk} - Fiyat: {self.bilet_fiyati} TL"


class Bilet:
    def __init__(self, etkinlik_id, musteri_adi, koltuk_no, fiyat):
        self.bilet_id = str(uuid.uuid4())[:8]  # Benzersiz bilet ID
        self.etkinlik_id = etkinlik_id
        self.musteri_adi = musteri_adi
        self.koltuk_no = koltuk_no
        self.fiyat = fiyat
        self.satis_tarihi = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def __str__(self):
        return f"Bilet ID: {self.bilet_id} - Etkinlik ID: {self.etkinlik_id} - M��teri: {self.musteri_adi} - Koltuk: {self.koltuk_no} - Fiyat: {self.fiyat} TL"


class BiletSatisSistemi:
    def __init__(self):
        self.etkinlikler = []
        self.tum_biletler = []
        self.ornek_etkinlikler_olustur()

    def ornek_etkinlikler_olustur(self):
        self.etkinlikler = [
            Etkinlik(1, "Rock Konseri", "15/05/2025", "�stanbul Arena", 100, 250.0),
            Etkinlik(2, "Jazz Festivali", "20/05/2025", "Ankara Kongre Merkezi", 75, 175.0),
            Etkinlik(3, "Tiyatro G�sterisi", "25/05/2025", "�zmir Sanat", 50, 150.0),
            Etkinlik(4, "Sinema Galas�", "30/05/2025", "Antalya K�lt�r Merkezi", 120, 100.0),
        ]

    def ekrani_temizle(self):
        """Ekran� temizler"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def ana_menu_goster(self):
        """Ana men�y� g�sterir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' ETK�NL�K B�LET SATI� S�STEM� ':=^50}")
        print("=" * 50)
        print("1. Etkinlikleri G�r�nt�le")
        print("2. Bilet Sat�n Al")
        print("3. Bilet �ptali")
        print("4. Sat�n Al�nan Biletleri G�r�nt�le")
        print("5. Yeni Etkinlik Ekle")
        print("0. ��k��")
        print("=" * 50)

    def etkinlikleri_goster(self):
        """T�m etkinlikleri listeler"""
        self.ekrani_temizle()
        print("\n" + "=" * 70)
        print(f"{' ETK�NL�K L�STES� ':=^70}")
        print("=" * 70)

        if not self.etkinlikler:
            print("Hi� etkinlik bulunmuyor!")
        else:
            for etkinlik in self.etkinlikler:
                print(etkinlik)

        input("\nAna men�ye d�nmek i�in ENTER tu�una bas�n...")

    def bilet_satin_al(self):
        """Bilet sat�n alma i�lemini ger�ekle�tirir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' B�LET SATIN ALMA ':=^50}")
        print("=" * 50)

        # Etkinlikleri g�ster
        for etkinlik in self.etkinlikler:
            print(etkinlik)

        try:
            etkinlik_id = int(input("\nEtkinlik ID'sini girin (�ptal i�in 0): "))
            if etkinlik_id == 0:
                return

            # Etkinli�i bul
            etkinlik = next((e for e in self.etkinlikler if e.id == etkinlik_id), None)
            if not etkinlik:
                print("Ge�ersiz etkinlik ID!")
                time.sleep(2)
                return

            if etkinlik.kalan_koltuk <= 0:
                print("Bu etkinlik i�in bilet kalmad�!")
                time.sleep(2)
                return

            musteri_adi = input("M��teri ad�: ")
            if not musteri_adi.strip():
                print("M��teri ad� bo� olamaz!")
                time.sleep(2)
                return

            bilet_adedi = int(input("Bilet adedi: "))
            if bilet_adedi <= 0:
                print("Ge�ersiz bilet adedi!")
                time.sleep(2)
                return

            if bilet_adedi > etkinlik.kalan_koltuk:
                print(f"�zg�n�z, sadece {etkinlik.kalan_koltuk} adet koltuk kald�!")
                time.sleep(2)
                return

            toplam_fiyat = bilet_adedi * etkinlik.bilet_fiyati
            print(f"\nToplam Fiyat: {toplam_fiyat} TL")
            onay = input("Sat�n almay� onayl�yor musunuz? (E/H): ").upper()

            if onay == 'E':
                for i in range(bilet_adedi):
                    koltuk_no = etkinlik.toplam_koltuk - etkinlik.kalan_koltuk + 1 + i
                    yeni_bilet = Bilet(etkinlik.id, musteri_adi, koltuk_no, etkinlik.bilet_fiyati)
                    self.tum_biletler.append(yeni_bilet)
                    etkinlik.satilan_biletler.append(yeni_bilet)

                etkinlik.kalan_koltuk -= bilet_adedi
                print(f"\n{bilet_adedi} adet bilet ba�ar�yla sat�n al�nd�!")
                print("Bilet detaylar�:")
                for bilet in self.tum_biletler[-bilet_adedi:]:
                    print(bilet)
            else:
                print("Bilet sat�n alma i�lemi iptal edildi.")

            input("\nAna men�ye d�nmek i�in ENTER tu�una bas�n...")

        except ValueError:
            print("L�tfen ge�erli bir say� girin!")
            time.sleep(2)

    def bilet_iptali(self):
        """Bilet iptal i�lemini ger�ekle�tirir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' B�LET �PTAL� ':=^50}")
        print("=" * 50)

        bilet_id = input("�ptal edilecek Bilet ID'sini girin (�ptal i�in 0): ")
        if bilet_id == "0":
            return

        bilet = next((b for b in self.tum_biletler if b.bilet_id == bilet_id), None)
        if not bilet:
            print("Ge�ersiz Bilet ID!")
            time.sleep(2)
            return

        # �lgili etkinli�i bul
        etkinlik = next((e for e in self.etkinlikler if e.id == bilet.etkinlik_id), None)
        if not etkinlik:
            print("Etkinlik bulunamad�! Bilet iptal edilemedi.")
            time.sleep(2)
            return

        print("\nBilet Bilgileri:")
        print(bilet)

        onay = input("\nBu bileti iptal etmek istedi�inize emin misiniz? (E/H): ").upper()
        if onay == 'E':
            self.tum_biletler.remove(bilet)
            etkinlik.satilan_biletler.remove(bilet)
            etkinlik.kalan_koltuk += 1
            print("Bilet ba�ar�yla iptal edildi!")
        else:
            print("Bilet iptal i�lemi iptal edildi.")

        input("\nAna men�ye d�nmek i�in ENTER tu�una bas�n...")

    def biletleri_goruntule(self):
        """Sat�n al�nan t�m biletleri g�r�nt�le"""
        self.ekrani_temizle()
        print("\n" + "=" * 80)
        print(f"{' SATIN ALINAN B�LETLER ':=^80}")
        print("=" * 80)

        if not self.tum_biletler:
            print("Hen�z sat�n al�nm�� bilet bulunmuyor!")
        else:
            for bilet in self.tum_biletler:
                # Etkinlik ad�n� bul
                etkinlik = next((e for e in self.etkinlikler if e.id == bilet.etkinlik_id), None)
                etkinlik_adi = etkinlik.isim if etkinlik else "Bilinmeyen Etkinlik"
                print(f"Bilet ID: {bilet.bilet_id} - Etkinlik: {etkinlik_adi} - M��teri: {bilet.musteri_adi} - "
                      f"Koltuk: {bilet.koltuk_no} - Fiyat: {bilet.fiyat} TL - Sat��: {bilet.satis_tarihi}")

        input("\nAna men�ye d�nmek i�in ENTER tu�una bas�n...")

    def yeni_etkinlik_ekle(self):
        """Yeni etkinlik ekleme"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' YEN� ETK�NL�K EKLE ':=^50}")
        print("=" * 50)

        try:
            etkinlik_id = len(self.etkinlikler) + 1
            isim = input("Etkinlik Ad�: ")
            if not isim.strip():
                print("Etkinlik ad� bo� olamaz!")
                time.sleep(2)
                return

            tarih = input("Tarih (GG/AA/YYYY): ")
            yer = input("Yer: ")
            toplam_koltuk = int(input("Toplam Koltuk Say�s�: "))
            bilet_fiyati = float(input("Bilet Fiyat� (TL): "))

            yeni_etkinlik = Etkinlik(etkinlik_id, isim, tarih, yer, toplam_koltuk, bilet_fiyati)
            self.etkinlikler.append(yeni_etkinlik)

            print(f"\n'{isim}' etkinli�i ba�ar�yla eklendi!")

        except ValueError:
            print("L�tfen ge�erli de�erler girin!")

        input("\nAna men�ye d�nmek i�in ENTER tu�una bas�n...")

    def calistir(self):
        """Ana program d�ng�s�"""
        while True:
            self.ana_menu_goster()
            secim = input("\nSe�iminiz (0-5): ")

            if secim == "1":
                self.etkinlikleri_goster()
            elif secim == "2":
                self.bilet_satin_al()
            elif secim == "3":
                self.bilet_iptali()
            elif secim == "4":
                self.biletleri_goruntule()
            elif secim == "5":
                self.yeni_etkinlik_ekle()
            elif secim == "0":
                self.ekrani_temizle()
                print("\nProgram sonland�r�l�yor...")
                print("Te�ekk�r ederiz!")
                break
            else:
                print("Ge�ersiz se�im! L�tfen tekrar deneyin.")
                time.sleep(1)


if __name__ == "__main__":
    bilet_sistemi = BiletSatisSistemi()
    bilet_sistemi.calistir()
