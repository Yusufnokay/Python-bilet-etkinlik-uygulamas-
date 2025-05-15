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
        return f"Bilet ID: {self.bilet_id} - Etkinlik ID: {self.etkinlik_id} - Müþteri: {self.musteri_adi} - Koltuk: {self.koltuk_no} - Fiyat: {self.fiyat} TL"


class BiletSatisSistemi:
    def __init__(self):
        self.etkinlikler = []
        self.tum_biletler = []
        self.ornek_etkinlikler_olustur()

    def ornek_etkinlikler_olustur(self):
        self.etkinlikler = [
            Etkinlik(1, "Rock Konseri", "15/05/2025", "Ýstanbul Arena", 100, 250.0),
            Etkinlik(2, "Jazz Festivali", "20/05/2025", "Ankara Kongre Merkezi", 75, 175.0),
            Etkinlik(3, "Tiyatro Gösterisi", "25/05/2025", "Ýzmir Sanat", 50, 150.0),
            Etkinlik(4, "Sinema Galasý", "30/05/2025", "Antalya Kültür Merkezi", 120, 100.0),
        ]

    def ekrani_temizle(self):
        """Ekraný temizler"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def ana_menu_goster(self):
        """Ana menüyü gösterir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' ETKÝNLÝK BÝLET SATIÞ SÝSTEMÝ ':=^50}")
        print("=" * 50)
        print("1. Etkinlikleri Görüntüle")
        print("2. Bilet Satýn Al")
        print("3. Bilet Ýptali")
        print("4. Satýn Alýnan Biletleri Görüntüle")
        print("5. Yeni Etkinlik Ekle")
        print("0. Çýkýþ")
        print("=" * 50)

    def etkinlikleri_goster(self):
        """Tüm etkinlikleri listeler"""
        self.ekrani_temizle()
        print("\n" + "=" * 70)
        print(f"{' ETKÝNLÝK LÝSTESÝ ':=^70}")
        print("=" * 70)

        if not self.etkinlikler:
            print("Hiç etkinlik bulunmuyor!")
        else:
            for etkinlik in self.etkinlikler:
                print(etkinlik)

        input("\nAna menüye dönmek için ENTER tuþuna basýn...")

    def bilet_satin_al(self):
        """Bilet satýn alma iþlemini gerçekleþtirir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' BÝLET SATIN ALMA ':=^50}")
        print("=" * 50)

        # Etkinlikleri göster
        for etkinlik in self.etkinlikler:
            print(etkinlik)

        try:
            etkinlik_id = int(input("\nEtkinlik ID'sini girin (Ýptal için 0): "))
            if etkinlik_id == 0:
                return

            # Etkinliði bul
            etkinlik = next((e for e in self.etkinlikler if e.id == etkinlik_id), None)
            if not etkinlik:
                print("Geçersiz etkinlik ID!")
                time.sleep(2)
                return

            if etkinlik.kalan_koltuk <= 0:
                print("Bu etkinlik için bilet kalmadý!")
                time.sleep(2)
                return

            musteri_adi = input("Müþteri adý: ")
            if not musteri_adi.strip():
                print("Müþteri adý boþ olamaz!")
                time.sleep(2)
                return

            bilet_adedi = int(input("Bilet adedi: "))
            if bilet_adedi <= 0:
                print("Geçersiz bilet adedi!")
                time.sleep(2)
                return

            if bilet_adedi > etkinlik.kalan_koltuk:
                print(f"Üzgünüz, sadece {etkinlik.kalan_koltuk} adet koltuk kaldý!")
                time.sleep(2)
                return

            toplam_fiyat = bilet_adedi * etkinlik.bilet_fiyati
            print(f"\nToplam Fiyat: {toplam_fiyat} TL")
            onay = input("Satýn almayý onaylýyor musunuz? (E/H): ").upper()

            if onay == 'E':
                for i in range(bilet_adedi):
                    koltuk_no = etkinlik.toplam_koltuk - etkinlik.kalan_koltuk + 1 + i
                    yeni_bilet = Bilet(etkinlik.id, musteri_adi, koltuk_no, etkinlik.bilet_fiyati)
                    self.tum_biletler.append(yeni_bilet)
                    etkinlik.satilan_biletler.append(yeni_bilet)

                etkinlik.kalan_koltuk -= bilet_adedi
                print(f"\n{bilet_adedi} adet bilet baþarýyla satýn alýndý!")
                print("Bilet detaylarý:")
                for bilet in self.tum_biletler[-bilet_adedi:]:
                    print(bilet)
            else:
                print("Bilet satýn alma iþlemi iptal edildi.")

            input("\nAna menüye dönmek için ENTER tuþuna basýn...")

        except ValueError:
            print("Lütfen geçerli bir sayý girin!")
            time.sleep(2)

    def bilet_iptali(self):
        """Bilet iptal iþlemini gerçekleþtirir"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' BÝLET ÝPTALÝ ':=^50}")
        print("=" * 50)

        bilet_id = input("Ýptal edilecek Bilet ID'sini girin (Ýptal için 0): ")
        if bilet_id == "0":
            return

        bilet = next((b for b in self.tum_biletler if b.bilet_id == bilet_id), None)
        if not bilet:
            print("Geçersiz Bilet ID!")
            time.sleep(2)
            return

        # Ýlgili etkinliði bul
        etkinlik = next((e for e in self.etkinlikler if e.id == bilet.etkinlik_id), None)
        if not etkinlik:
            print("Etkinlik bulunamadý! Bilet iptal edilemedi.")
            time.sleep(2)
            return

        print("\nBilet Bilgileri:")
        print(bilet)

        onay = input("\nBu bileti iptal etmek istediðinize emin misiniz? (E/H): ").upper()
        if onay == 'E':
            self.tum_biletler.remove(bilet)
            etkinlik.satilan_biletler.remove(bilet)
            etkinlik.kalan_koltuk += 1
            print("Bilet baþarýyla iptal edildi!")
        else:
            print("Bilet iptal iþlemi iptal edildi.")

        input("\nAna menüye dönmek için ENTER tuþuna basýn...")

    def biletleri_goruntule(self):
        """Satýn alýnan tüm biletleri görüntüle"""
        self.ekrani_temizle()
        print("\n" + "=" * 80)
        print(f"{' SATIN ALINAN BÝLETLER ':=^80}")
        print("=" * 80)

        if not self.tum_biletler:
            print("Henüz satýn alýnmýþ bilet bulunmuyor!")
        else:
            for bilet in self.tum_biletler:
                # Etkinlik adýný bul
                etkinlik = next((e for e in self.etkinlikler if e.id == bilet.etkinlik_id), None)
                etkinlik_adi = etkinlik.isim if etkinlik else "Bilinmeyen Etkinlik"
                print(f"Bilet ID: {bilet.bilet_id} - Etkinlik: {etkinlik_adi} - Müþteri: {bilet.musteri_adi} - "
                      f"Koltuk: {bilet.koltuk_no} - Fiyat: {bilet.fiyat} TL - Satýþ: {bilet.satis_tarihi}")

        input("\nAna menüye dönmek için ENTER tuþuna basýn...")

    def yeni_etkinlik_ekle(self):
        """Yeni etkinlik ekleme"""
        self.ekrani_temizle()
        print("\n" + "=" * 50)
        print(f"{' YENÝ ETKÝNLÝK EKLE ':=^50}")
        print("=" * 50)

        try:
            etkinlik_id = len(self.etkinlikler) + 1
            isim = input("Etkinlik Adý: ")
            if not isim.strip():
                print("Etkinlik adý boþ olamaz!")
                time.sleep(2)
                return

            tarih = input("Tarih (GG/AA/YYYY): ")
            yer = input("Yer: ")
            toplam_koltuk = int(input("Toplam Koltuk Sayýsý: "))
            bilet_fiyati = float(input("Bilet Fiyatý (TL): "))

            yeni_etkinlik = Etkinlik(etkinlik_id, isim, tarih, yer, toplam_koltuk, bilet_fiyati)
            self.etkinlikler.append(yeni_etkinlik)

            print(f"\n'{isim}' etkinliði baþarýyla eklendi!")

        except ValueError:
            print("Lütfen geçerli deðerler girin!")

        input("\nAna menüye dönmek için ENTER tuþuna basýn...")

    def calistir(self):
        """Ana program döngüsü"""
        while True:
            self.ana_menu_goster()
            secim = input("\nSeçiminiz (0-5): ")

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
                print("\nProgram sonlandýrýlýyor...")
                print("Teþekkür ederiz!")
                break
            else:
                print("Geçersiz seçim! Lütfen tekrar deneyin.")
                time.sleep(1)


if __name__ == "__main__":
    bilet_sistemi = BiletSatisSistemi()
    bilet_sistemi.calistir()
