def eposta_denetle(adres):
    if adres.count("@") != 1:
        return "Tam olarak bir @ olmalı"
    if ".."in adres:
        return "Nokta ile başlayamaz/bitemez"
    at_konum = adres.find("@")
    kullanici = adres[:at_konum]
    alan = adres[at_konum + 1:]
    if len(kullanici) == 0:
        return "Geçersiz kullanıcı adı"

    for ch in kullanici:
        if not (ch.isalnum() or ch == "." or ch == "_" or ch == "-"):
            return f"Geçersiz karakter: '{ch}'"
    if kullanici.startswith(".") or kullanici.endswith("."):
        return "Nokta ile başlayamaz/bitemez"
    if alan.find(".") == -1 or alan.startswith(".") or alan.endswith("."):
        return "Alan adı hatalı"

    return "Geçerli"
    if __name__ == "__main__":
    print(eposta_denetle("ece.yilmaz@nisantasi.edu.tr"))
    print(eposta_denetle("ece@@mail.com"))
    print(eposta_denetle("ece yilmaz@mail.com"))
    print(eposta_denetle(".ece@mail.com"))
    print(eposta_denetle("ece@mail"))

    RAKAM = "0123456789ABCDEF"


def onluktan(n, taban):
    """Onluk tabandaki n tam sayisini (2-16 arasi) istenen tabana cevirir."""
    if taban < 2 or taban > 16:
        raise ValueError("Taban 2 ile 16 arasında olmalıdır.")

    if n == 0:
        return "0"

    isaret = ""
    if n < 0:
        isaret = "-"
        n = -n

    sonuc = ""
    while n > 0:
        kalan = n % taban
        sonuc = RAKAM[kalan] + sonuc
        n //= taban

    return isaret + sonuc


def onluga(metin, taban):
    """Verilen tabandaki metni Horner yontemiyle onluk tam sayiya cevirir."""
    if taban < 2 or taban > 16:
        raise ValueError("Taban 2 ile 16 arasında olmalıdır.")

    temiz = metin.strip().upper()
    if len(temiz) == 0:
        raise ValueError("Boş metin dönüştürülemez.")

    isaret = 1
    baslangic = 0
    if temiz.startswith("-"):
        isaret = -1
        baslangic = 1

    toplam = 0
    i = baslangic
    while i < len(temiz):
        ch = temiz[i]
        basamak_degeri = RAKAM.find(ch)
        if basamak_degeri < 0 or basamak_degeri >= taban:
            raise ValueError(f"'{ch}' karakteri {taban} tabanı için geçersiz.")
        toplam = toplam * taban + basamak_degeri
        i += 1

    return isaret * toplam


if __name__ == "__main__":
    sayi = 2026
    ikilik = onluktan(sayi, 2)
    sekizlik = onluktan(sayi, 8)
    onaltilik = onluktan(sayi, 16)
    print(f"{sayi} -> ikilik {ikilik} · sekizlik {sekizlik} · onaltılık {onaltilik}")

    assert onluga("7ea", 16) == int("7ea", 16)
    assert onluga("11111101010", 2) == int(bin(sayi)[2:], 2)
    assert onluga("3752", 8) == sayi
    print("Doğrulama başarılı:", onluga("7ea", 16))

def _harf_indeksi(ch):
    """A/a -> 0, B/b -> 1, ..., Z/z -> 25 degerini dondurur."""
    if "A" <= ch <= "Z":
        return ord(ch) - ord("A")
    if "a" <= ch <= "z":
        return ord(ch) - ord("a")
    return -1


def vigenere(metin, anahtar, yon=1):
    """Metni Vigenere algoritmasiyla sifirler (yon=1) veya cozer (yon=-1)."""
    if yon not in (1, -1):
        raise ValueError("yon parametresi 1 veya -1 olmalıdır.")

    temiz_anahtar = ""
    for ch in anahtar:
        if _harf_indeksi(ch) != -1:
            temiz_anahtar += ch.upper()

    if len(temiz_anahtar) == 0:
        raise ValueError("Anahtar en az bir İngiliz alfabesi harfi içermelidir.")

    m = len(temiz_anahtar)
    sonuc = ""
    j = 0

    for ch in metin:
        p = _harf_indeksi(ch)
        if p == -1:
            sonuc += ch
        else:
            k = _harf_indeksi(temiz_anahtar[j % m])
            yeni_indeks = (p + yon * k) % 26
            if ch.isupper():
                sonuc += chr(ord("A") + yeni_indeks)
            else:
                sonuc += chr(ord("a") + yeni_indeks)
            j += 1

    return sonuc


if __name__ == "__main__":
    sifreli = vigenere("Attack at dawn", "LEMON")
    cozulen = vigenere(sifreli, "LEMON", -1)
    print(sifreli)
    print(cozulen)

    def _obeb(a, b):
    """Oklid algoritmasi ile en buyuk ortak boleni hesaplar."""
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a if a != 0 else 1


class Kesir:
    """Sade halini koruyan ve karsilastirma/aritmetik ozel metotlari iceren kesir sinifi."""

    def __init__(self, pay, payda=1):
        """Pay ve paydayi alarak sadelestirilmis kesir olusturur."""
        if payda == 0:
            raise ZeroDivisionError("Payda sıfır olamaz.")
        if payda < 0:
            pay = -pay
            payda = -payda
        ortak = _obeb(pay, payda)
        self.pay = pay // ortak
        self.payda = payda // ortak

    def __str__(self):
        """Kesri okunabilir metin ('pay/payda' veya tam sayi) olarak dondurur."""
        if self.payda == 1:
            return str(self.pay)
        return f"{self.pay}/{self.payda}"

    def __add__(self, diger):
        """Iki kesri toplayip yeni ve sade bir Kesir dondurur."""
        yeni_pay = self.pay * diger.payda + diger.pay * self.payda
        yeni_payda = self.payda * diger.payda
        return Kesir(yeni_pay, yeni_payda)

    def __sub__(self, diger):
        """Iki kesrin farkini alip yeni ve sade bir Kesir dondurur."""
        yeni_pay = self.pay * diger.payda - diger.pay * self.payda
        yeni_payda = self.payda * diger.payda
        return Kesir(yeni_pay, yeni_payda)

    def __mul__(self, diger):
        """Iki kesri carpip yeni ve sade bir Kesir dondurur."""
        return Kesir(self.pay * diger.pay, self.payda * diger.payda)

    def __truediv__(self, diger):
        """Iki kesri bolup yeni ve sade bir Kesir dondurur."""
        if diger.pay == 0:
            raise ZeroDivisionError("Sıfıra bölme hatası.")
        return Kesir(self.pay * diger.payda, self.payda * diger.pay)

    def __eq__(self, diger):
        """Capraz carpim ile esitlik kontrolu yapar."""
        if not isinstance(diger, Kesir):
            return False
        return self.pay * diger.payda == diger.pay * self.payda

    def __lt__(self, diger):
        """Capraz carpim ile 'kucuktur' (<) karsilastirmasi yapar."""
        return self.pay * diger.payda < diger.pay * self.payda

    def __le__(self, diger):
        """Capraz carpim ile 'kucuk veya esittir' (<=) karsilastirmasi yapar."""
        return self.pay * diger.payda <= diger.pay * self.payda

    def __float__(self):
        """Kesrin ondalik (float) degerini dondurur."""
        return self.pay / self.payda


if __name__ == "__main__":
    print("Kesir(6, 8) == Kesir(3, 4) ->", Kesir(6, 8) == Kesir(3, 4))
    print("Kesir(3, 4) / Kesir(3, 8) ->", Kesir(3, 4) / Kesir(3, 8))

    # (a) n=2..10 icin (1 - 1/n) carpimi
    carpim = Kesir(1, 1)
    for n in range(2, 11):
        carpim = carpim * (Kesir(1, 1) - Kesir(1, n))

    # (b) 3/7, 5/12, 2/5, 4/9, 3/8 arasindan yalnizca '<' kullanarak en buyugu bulma
    k1 = Kesir(3, 7)
    k2 = Kesir(5, 12)
    k3 = Kesir(2, 5)
    k4 = Kesir(4, 9)
    k5 = Kesir(3, 8)

    en_buyuk = k1
    if en_buyuk < k2:
        en_buyuk = k2
    if en_buyuk < k3:
        en_buyuk = k3
    if en_buyuk < k4:
        en_buyuk = k4
    if en_buyuk < k5:
        en_buyuk = k5

    print(f"Çarpım: {carpim} En büyük: {en_buyuk}")
ALFABE = "abcçdefgğhıijklmnoöprsştuüvyz"


def _turkce_kucult(metin):
    """Metni once I->ı ve İ->i kurallarina gore Turkce kucuk harfe cevirir."""
    s = metin.replace("I", "ı").replace("İ", "i")
    s = s.replace("Ç", "ç").replace("Ğ", "ğ").replace("Ö", "ö")
    s = s.replace("Ş", "ş").replace("Ü", "ü")
    return s.lower()


def _turkce_buyut(metin):
    """Metni Turkce buyuk harfe cevirir (i->İ, ı->I vb.)."""
    s = metin.replace("i", "İ").replace("ı", "I")
    s = s.replace("ç", "Ç").replace("ğ", "Ğ").replace("ö", "Ö")
    s = s.replace("ş", "Ş").replace("ü", "Ü")
    return s.upper()


class TrKelime:
    """Turkce alfabe siralamasi ve ozel metotlari destekleyen kelime sinifi."""

    def __init__(self, metin):
        """Metni Turkce kucuk harf formunda saklar."""
        self.metin = _turkce_kucult(str(metin))

    def __str__(self):
        """Kelimenin kucuk harfli metin temsilini dondurur."""
        return self.metin

    def __len__(self):
        """Kelimedeki karakter sayisini dondurur."""
        return len(self.metin)

    def __getitem__(self, indeks):
        """Indeks veya dilim erisimi saglar."""
        if isinstance(indeks, slice):
            return TrKelime(self.metin[indeks])
        return self.metin[indeks]

    def __contains__(self, parca):
        """Alt metin icerip icermedigini Turkce kucultme ile denetler."""
        aranan = parca.metin if isinstance(parca, TrKelime) else _turkce_kucult(str(parca))
        return aranan in self.metin

    def __eq__(self, diger):
        """Iki TrKelime nesnesinin esitligini kontrol eder."""
        if not isinstance(diger, TrKelime):
            return False
        return self.metin == diger.metin

    def __lt__(self, diger):
        """ALFABE.find sirasina gore kucukluk karsilastirmasi yapar."""
        min_uzunluk = len(self.metin) if len(self.metin) < len(diger.metin) else len(diger.metin)
        i = 0
        while i < min_uzunluk:
            ch1 = self.metin[i]
            ch2 = diger.metin[i]
            if ch1 != ch2:
                idx1 = ALFABE.find(ch1)
                idx2 = ALFABE.find(ch2)
                if idx1 != -1 and idx2 != -1:
                    return idx1 < idx2
                return ch1 < ch2
            i += 1
        return len(self.metin) < len(diger.metin)

    def buyuk(self):
        """Kelimeyi Turkce buyuk harf kurallarina gore dondurur."""
        return _turkce_buyut(self.metin)


if __name__ == "__main__":
    print("çay < dağ Türkçe:", TrKelime("çay") < TrKelime("dağ"), "Python str:", "çay" < "dağ")
    print("ılık < iğne Türkçe:", TrKelime("ılık") < TrKelime("iğne"), "Python str:", "ılık" < "iğne")
    print("ördek < pasta Türkçe:", TrKelime("ördek") < TrKelime("pasta"), "Python str:", "ördek" < "pasta")
    print('TrKelime("Işık") == TrKelime("ışık") ->', TrKelime("Işık") == TrKelime("ışık"))

    k = TrKelime("İSTANBUL")
    print(k, "len(k) ->", len(k))
    print('"tan" in k ->', "tan" in k, "k.buyuk() ->", k.buyuk())

def _roma_tek_deger(ch):
    """Tek bir Roma rakami karakterinin onluk karsiligini dondurur."""
    if ch == "I":
        return 1
    if ch == "V":
        return 5
    if ch == "X":
        return 10
    if ch == "L":
        return 50
    if ch == "C":
        return 100
    if ch == "D":
        return 500
    if ch == "M":
        return 1000
    raise ValueError(f"Geçersiz Roma rakamı: '{ch}'")


def onluktan_roma(n):
    """1-3999 arasi onluk sayiyi Roma rakamina cevirir."""
    if n <= 0 or n >= 4000:
        raise ValueError("Sayı 1 ile 3999 arasında olmalıdır.")

    sonuc = ""
    while n >= 1000:
        sonuc += "M"
        n -= 1000
    if n >= 900:
        sonuc += "CM"
        n -= 900
    if n >= 500:
        sonuc += "D"
        n -= 500
    if n >= 400:
        sonuc += "CD"
        n -= 400
    while n >= 100:
        sonuc += "C"
        n -= 100
    if n >= 90:
        sonuc += "XC"
        n -= 90
    if n >= 50:
        sonuc += "L"
        n -= 50
    if n >= 40:
        sonuc += "XL"
        n -= 40
    while n >= 10:
        sonuc += "X"
        n -= 10
    if n >= 9:
        sonuc += "IX"
        n -= 9
    if n >= 5:
        sonuc += "V"
        n -= 5
    if n >= 4:
        sonuc += "IV"
        n -= 4
    while n >= 1:
        sonuc += "I"
        n -= 1

    return sonuc


def romadan_onluga(roma):
    """Roma rakami metnini onluk tam sayiya cevirir."""
    s = roma.strip().upper()
    toplam = 0
    i = 0
    while i < len(s):
        su_anki = _roma_tek_deger(s[i])
        if i + 1 < len(s):
            sonraki = _roma_tek_deger(s[i + 1])
            if su_anki < sonraki:
                toplam += sonraki - su_anki
                i += 2
                continue
        toplam += su_anki
        i += 1
    return toplam


if __name__ == "__main__":
    print(onluktan_roma(2026))   # MMXXVI
    print(onluktan_roma(1994))   # MCMXCIV
    print(romadan_onluga("XLII"))  # 42