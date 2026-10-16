
"""
Pengurut Peringkat Lagu Berdasarkan Jumlah Pemutaran (Music Play-Count Ranker)

Cara menjalankan  : python pemeringkat_lagu.py
Uji statistik     : python pemeringkat_lagu.py --statistik   (iteratif vs rekursif, hanya di konsol)
Dataset opsional  : letakkan file "lagu.csv" (kolom: judul,penyanyi,pemutaran) di folder yang sama
                    untuk memakai dataset lagu asli milik Anda (mis. dari Kaggle/Spotify).

Hanya memakai pustaka standar Python (tkinter sudah bawaan).
"""

import csv
import os
import queue
import random
import sys
import threading
import time
import tkinter as tk
from collections import namedtuple
from tkinter import ttk

# =====================================================================
# 1. MODEL DATA & DATASET
# =====================================================================
# Setiap lagu memiliki properti: ID, Judul Lagu, Nama Penyanyi, Jumlah Pemutaran.
Lagu = namedtuple("Lagu", ["id", "judul", "penyanyi", "putar"])

# Katalog lagu nyata (judul, penyanyi). Dipakai sebagai sumber dataset.
KATALOG_LAGU = [
    ("Blinding Lights", "The Weeknd"), ("Shape of You", "Ed Sheeran"),
    ("Someone You Loved", "Lewis Capaldi"), ("Dance Monkey", "Tones and I"),
    ("Sunflower", "Post Malone"), ("As It Was", "Harry Styles"),
    ("Bad Guy", "Billie Eilish"), ("Stay", "The Kid LAROI & Justin Bieber"),
    ("Levitating", "Dua Lipa"), ("Watermelon Sugar", "Harry Styles"),
    ("Perfect", "Ed Sheeran"), ("Uptown Funk", "Mark Ronson ft. Bruno Mars"),
    ("Rockstar", "Post Malone"), ("One Dance", "Drake"),
    ("Closer", "The Chainsmokers"), ("Thinking Out Loud", "Ed Sheeran"),
    ("Counting Stars", "OneRepublic"), ("Havana", "Camila Cabello"),
    ("Believer", "Imagine Dragons"), ("Thunder", "Imagine Dragons"),
    ("Senorita", "Shawn Mendes & Camila Cabello"), ("Starboy", "The Weeknd"),
    ("Circles", "Post Malone"), ("Memories", "Maroon 5"),
    ("Girls Like You", "Maroon 5"), ("Sugar", "Maroon 5"),
    ("Happier", "Marshmello & Bastille"), ("Lovely", "Billie Eilish & Khalid"),
    ("Ocean Eyes", "Billie Eilish"), ("Don't Start Now", "Dua Lipa"),
    ("Save Your Tears", "The Weeknd"), ("Peaches", "Justin Bieber"),
    ("Good 4 U", "Olivia Rodrigo"), ("Drivers License", "Olivia Rodrigo"),
    ("Heat Waves", "Glass Animals"), ("Industry Baby", "Lil Nas X & Jack Harlow"),
    ("Montero", "Lil Nas X"), ("Old Town Road", "Lil Nas X"),
    ("Shallow", "Lady Gaga & Bradley Cooper"), ("Bad Romance", "Lady Gaga"),
    ("Rolling in the Deep", "Adele"), ("Hello", "Adele"),
    ("Someone Like You", "Adele"), ("Easy On Me", "Adele"),
    ("Shake It Off", "Taylor Swift"), ("Blank Space", "Taylor Swift"),
    ("Anti-Hero", "Taylor Swift"), ("Love Story", "Taylor Swift"),
    ("Cruel Summer", "Taylor Swift"), ("Flowers", "Miley Cyrus"),
    ("Unholy", "Sam Smith & Kim Petras"), ("Stay With Me", "Sam Smith"),
    ("Cheap Thrills", "Sia"), ("Chandelier", "Sia"),
    ("Titanium", "David Guetta ft. Sia"), ("Wake Me Up", "Avicii"),
    ("Levels", "Avicii"), ("Faded", "Alan Walker"),
    ("Alone", "Alan Walker"), ("Lean On", "Major Lazer & DJ Snake"),
    ("Despacito", "Luis Fonsi & Daddy Yankee"), ("Gangnam Style", "PSY"),
    ("Dynamite", "BTS"), ("Butter", "BTS"),
    ("Boy With Luv", "BTS ft. Halsey"), ("How You Like That", "BLACKPINK"),
    ("Kill This Love", "BLACKPINK"), ("Pink Venom", "BLACKPINK"),
    ("Bohemian Rhapsody", "Queen"), ("Don't Stop Me Now", "Queen"),
    ("We Will Rock You", "Queen"), ("Imagine", "John Lennon"),
    ("Hey Jude", "The Beatles"), ("Let It Be", "The Beatles"),
    ("Yesterday", "The Beatles"), ("Hotel California", "Eagles"),
    ("Stairway to Heaven", "Led Zeppelin"), ("Smells Like Teen Spirit", "Nirvana"),
    ("Sweet Child O' Mine", "Guns N' Roses"), ("November Rain", "Guns N' Roses"),
    ("Billie Jean", "Michael Jackson"), ("Thriller", "Michael Jackson"),
    ("Beat It", "Michael Jackson"), ("Every Breath You Take", "The Police"),
    ("Take On Me", "a-ha"), ("Livin' on a Prayer", "Bon Jovi"),
    ("In the End", "Linkin Park"), ("Numb", "Linkin Park"),
    ("Yellow", "Coldplay"), ("Viva la Vida", "Coldplay"),
    ("Fix You", "Coldplay"), ("Paradise", "Coldplay"),
    ("Radioactive", "Imagine Dragons"), ("Demons", "Imagine Dragons"),
    ("Mr. Brightside", "The Killers"), ("Seven Nation Army", "The White Stripes"),
    ("Creep", "Radiohead"), ("Wonderwall", "Oasis"),
    ("Zombie", "The Cranberries"), ("Chasing Cars", "Snow Patrol"),
    ("Photograph", "Ed Sheeran"), ("Bad Habits", "Ed Sheeran"),
    ("Lose Yourself", "Eminem"), ("Love The Way You Lie", "Eminem ft. Rihanna"),
    ("Umbrella", "Rihanna"), ("Diamonds", "Rihanna"),
    ("Work", "Rihanna ft. Drake"), ("Single Ladies", "Beyonce"),
    ("Halo", "Beyonce"), ("Formation", "Beyonce"),
    ("Firework", "Katy Perry"), ("Roar", "Katy Perry"),
    ("Dark Horse", "Katy Perry ft. Juicy J"), ("Toxic", "Britney Spears"),
    ("Baby", "Justin Bieber ft. Ludacris"), ("Sorry", "Justin Bieber"),
    ("Love Yourself", "Justin Bieber"), ("Treat You Better", "Shawn Mendes"),
    ("Stitches", "Shawn Mendes"), ("Attention", "Charlie Puth"),
    ("See You Again", "Wiz Khalifa ft. Charlie Puth"), ("We Don't Talk Anymore", "Charlie Puth"),
    ("Say You Won't Let Go", "James Arthur"), ("All of Me", "John Legend"),
    ("A Thousand Years", "Christina Perri"), ("Just the Way You Are", "Bruno Mars"),
    ("Locked Out of Heaven", "Bruno Mars"), ("Grenade", "Bruno Mars"),
    ("Treasure", "Bruno Mars"), ("24K Magic", "Bruno Mars"),
    ("God's Plan", "Drake"), ("Hotline Bling", "Drake"),
    ("HUMBLE.", "Kendrick Lamar"), ("Sicko Mode", "Travis Scott"),
    ("Goosebumps", "Travis Scott"), ("Mood", "24kGoldn ft. iann dior"),
    ("Positions", "Ariana Grande"), ("7 rings", "Ariana Grande"),
    ("Thank U, Next", "Ariana Grande"), ("Side to Side", "Ariana Grande"),
    ("Yellow Submarine", "The Beatles"), ("Komang", "Raim Laode"),
    ("Hati-Hati di Jalan", "Tulus"), ("Monokrom", "Tulus"),
    ("Pamit", "Tulus"), ("Sempurna", "Andra and the Backbone"),
    ("Separuh Aku", "NOAH"), ("Yang Terdalam", "Peterpan"),
    ("Bukan Cinta Biasa", "Siti Nurhaliza"), ("Cinta Luar Biasa", "Andmesh Kamaleng"),
    ("Tak Ingin Usai", "Keisya Levronka"), ("Lathi", "Weird Genius ft. Sara Fajira"),
    ("Mungkin Nanti", "Peterpan"), ("Kangen", "Dewa 19"),
    ("Pupus", "Dewa 19"), ("Risalah Hati", "Dewa 19"),
    ("Bento", "Iwan Fals"), ("Aku Milikmu Malam Ini", "Rhoma Irama"),
    ("Sebelum Cahaya", "Letto"), ("Ruang Rindu", "Letto"),
    ("Hampa", "Ari Lasso"), ("Cinta Sejati", "Bunga Citra Lestari"),
    ("Dia", "Anji"), ("Kemarin", "Seventeen"),
]

# Varian rilis yang umum dijumpai pada layanan streaming.
VARIAN_RILIS = [
    "", "", "", "", "", "",  # versi asli lebih sering muncul
    " (Live)", " (Acoustic)", " (Remastered)", " (Remix)",
    " (Radio Edit)", " (Sped Up)", " (Instrumental)", " (Cover)",
]


def buat_dataset(jumlah, berkas_csv="lagu.csv", seed=2024):
    """
    Generator dataset. Jika 'lagu.csv' tersedia, data asli dari berkas dipakai.
    Jika tidak, dataset dibentuk dari katalog lagu hingga `jumlah` baris
    (maksimal 100.000+), lengkap dengan ID unik dan jumlah pemutaran.
    """
    if os.path.exists(berkas_csv):
        data = _muat_csv(berkas_csv)
        if data:
            random.Random(seed).shuffle(data)
            return data[:jumlah]

    acak = random.Random(seed)
    data = []
    for i in range(1, jumlah + 1):
        judul, penyanyi = acak.choice(KATALOG_LAGU)
        judul += acak.choice(VARIAN_RILIS)
        # Distribusi log-normal menyerupai sebaran pemutaran dunia nyata.
        putar = int(acak.lognormvariate(13.0, 1.6))
        data.append(Lagu(i, judul, penyanyi, putar))
    return data


def _muat_csv(berkas):
    """Membaca dataset lagu asli dari CSV (judul, penyanyi, pemutaran)."""
    hasil = []
    try:
        with open(berkas, newline="", encoding="utf-8") as f:
            for no, baris in enumerate(csv.DictReader(f), start=1):
                hasil.append(Lagu(no, baris["judul"], baris["penyanyi"],
                                  int(float(baris["pemutaran"]))))
    except (OSError, KeyError, ValueError):
        return []
    return hasil


# =====================================================================
# 2. ALGORITMA PENGURUTAN (descending: pemutaran terbanyak -> tersedikit)
# =====================================================================
def quick_sort(data):
    """Quick Sort (3-way partition, pivot acak) - rata-rata O(n log n)."""
    if len(data) <= 1:
        return data
    pivot = data[random.randrange(len(data))].putar
    lebih = [x for x in data if x.putar > pivot]
    sama = [x for x in data if x.putar == pivot]
    kurang = [x for x in data if x.putar < pivot]
    return quick_sort(lebih) + sama + quick_sort(kurang)


def merge_sort(data):
    """Merge Sort - selalu O(n log n)."""
    if len(data) <= 1:
        return data
    tengah = len(data) // 2
    kiri = merge_sort(data[:tengah])
    kanan = merge_sort(data[tengah:])
    return _gabung(kiri, kanan)


def _gabung(kiri, kanan):
    hasil, i, j = [], 0, 0
    while i < len(kiri) and j < len(kanan):
        if kiri[i].putar >= kanan[j].putar:      # descending
            hasil.append(kiri[i]); i += 1
        else:
            hasil.append(kanan[j]); j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def selection_sort(data):
    """
    Selection Sort - O(n^2). Pada setiap langkah dipilih elemen dengan
    pemutaran terbesar dari bagian yang belum terurut, lalu ditukar ke depan.
    (Pencarian maksimum memakai max() bawaan agar tetap layak pada 100.000 data.)
    """
    arr = list(data)
    hitung = [x.putar for x in arr]
    n = len(arr)
    for i in range(n - 1):
        terbesar = max(hitung[i:])
        j = hitung.index(terbesar, i)
        if j != i:
            arr[i], arr[j] = arr[j], arr[i]
            hitung[i], hitung[j] = hitung[j], hitung[i]
    return arr


ALGORITMA = {
    "Quick Sort": (quick_sort, "O(n log n)"),
    "Merge Sort": (merge_sort, "O(n log n)"),
    "Selection Sort": (selection_sort, "O(n²)"),
}


def prosesPengurutan(nama_algoritma, data):
    """
    FUNGSI (mengembalikan nilai) yang mengurutkan data dan mencatat durasinya.
    Dipanggil oleh PROSEDUR tampilkanMenu() dan oleh halaman Uji Performa.
    Mengembalikan: (hasil_terurut, durasi_milidetik)
    """
    fungsi, _ = ALGORITMA[nama_algoritma]
    mulai = time.perf_counter()
    hasil = fungsi(list(data))
    durasi_ms = (time.perf_counter() - mulai) * 1000
    return hasil, durasi_ms


# =====================================================================
# 3. ITERATIF REKURSIF + BENCHMARK
# =====================================================================
def total_pemutaran_iteratif(data):
    """Versi ITERATIF: akumulasi total pemutaran memakai perulangan."""
    total = 0
    for lagu in data:
        total += lagu.putar
    return total


def total_pemutaran_rekursif(data, awal=0, akhir=None):
    """
    Versi REKURSIF: membagi daftar menjadi dua bagian (divide & conquer)
    sehingga kedalaman rekursi hanya ~log2(n) dan aman untuk 100.000 data.
    """
    if akhir is None:
        akhir = len(data)
    if akhir - awal == 0:
        return 0
    if akhir - awal == 1:
        return data[awal].putar
    tengah = (awal + akhir) // 2
    return (total_pemutaran_rekursif(data, awal, tengah)
            + total_pemutaran_rekursif(data, tengah, akhir))


def _ukur(fungsi, data, ulang=20):
    """Rata-rata waktu eksekusi (mikrodetik) dari beberapa kali pengulangan."""
    mulai = time.perf_counter()
    for _ in range(ulang):
        hasil = fungsi(data)
    rata = (time.perf_counter() - mulai) / ulang * 1_000_000
    return hasil, rata


def cetakHeader(judul):
    """PROSEDUR (tanpa nilai kembali): mencetak header ke konsol."""
    print("=" * 56)
    print(judul.center(56))
    print("=" * 56)


def benchmarkStatistik():
    """Fungsi lain yang memanggil prosedur cetakHeader() lalu membandingkan waktu."""
    cetakHeader("PERBANDINGAN ITERATIF vs REKURSIF")
    data = buat_dataset(100_000)
    total_i, waktu_i = _ukur(total_pemutaran_iteratif, data)
    total_r, waktu_r = _ukur(total_pemutaran_rekursif, data)
    print(f"{'Metode':<12}{'Total Pemutaran':>22}{'Waktu (µs)':>18}")
    print("-" * 56)
    print(f"{'Iteratif':<12}{total_i:>22,}{waktu_i:>18,.1f}")
    print(f"{'Rekursif':<12}{total_r:>22,}{waktu_r:>18,.1f}")
    print("-" * 56)
    print("Hasil sama:", total_i == total_r)


# =====================================================================
# 4. TAMPILAN (UI/UX) - tema hitam, biru, putih
# =====================================================================
HITAM = "#05070D"
PANEL = "#0B1220"
PANEL_2 = "#111B30"
BIRU = "#2563EB"
BIRU_TERANG = "#3B82F6"
BIRU_TUA = "#1E3A8A"
PUTIH = "#FFFFFF"
ABU = "#94A3B8"
FONT = "Segoe UI"


def fmt(angka):
    """Format angka dengan pemisah ribuan titik: 1234567 -> 1.234.567"""
    return f"{angka:,}".replace(",", ".")


def cetakHeaderUI(induk, judul):
    """
    PROSEDUR tampilan: membangun judul halaman (tanpa nilai kembali).
    Dipanggil oleh fungsi buatHalamanPeringkat() dan buatHalamanPerforma().
    """
    tk.Label(induk, text=judul, bg=HITAM, fg=PUTIH,
             font=(FONT, 22, "bold"), anchor="w").pack(fill="x", padx=32, pady=(28, 12))


def buatHalamanPeringkat(app):
    """FUNGSI: membangun halaman Peringkat dan mengembalikan frame-nya.
    Di dalamnya memanggil prosedur cetakHeaderUI()."""
    frame = tk.Frame(app.konten, bg=HITAM)
    cetakHeaderUI(frame, "Peringkat Lagu")        # fungsi memanggil prosedur

    bar = tk.Frame(frame, bg=HITAM)
    bar.pack(fill="x", padx=32, pady=(0, 14))

    app.var_cari = tk.StringVar()
    kotak = tk.Entry(bar, textvariable=app.var_cari, bg=PANEL_2, fg=PUTIH,
                     insertbackground=PUTIH, relief="flat", font=(FONT, 11),
                     highlightthickness=1, highlightbackground=BIRU_TUA,
                     highlightcolor=BIRU)
    kotak.pack(side="left", fill="x", expand=True, ipady=8)
    app.var_cari.trace_add("write", lambda *_: app.isiTabel())

    app.var_algo = tk.StringVar(value="Merge Sort")
    ttk.Combobox(bar, textvariable=app.var_algo, values=list(ALGORITMA),
                 state="readonly", width=14, font=(FONT, 10)).pack(side="left", padx=(12, 0), ipady=4)

    app.var_ukuran = tk.StringVar(value="100.000")
    ttk.Combobox(bar, textvariable=app.var_ukuran,
                 values=["1.000", "10.000", "100.000"],
                 state="readonly", width=8, font=(FONT, 10)).pack(side="left", padx=(8, 0), ipady=4)

    app.tombol_urut = tombol(bar, "Urutkan", app.urutkan)
    app.tombol_urut.pack(side="left", padx=(12, 0))

    app.status = tk.Label(frame, text="", bg=HITAM, fg=ABU, font=(FONT, 10), anchor="w")
    app.status.pack(fill="x", padx=32)

    kolom = ("rank", "judul", "penyanyi", "putar")
    app.tabel = ttk.Treeview(frame, columns=kolom, show="headings", style="Gelap.Treeview")
    for k, teks, lebar, rata in (("rank", "#", 70, "center"), ("judul", "Judul Lagu", 340, "w"),
                                 ("penyanyi", "Penyanyi", 260, "w"), ("putar", "Pemutaran", 140, "e")):
        app.tabel.heading(k, text=teks)
        app.tabel.column(k, width=lebar, anchor=rata)
    app.tabel.tag_configure("genap", background=PANEL)
    app.tabel.tag_configure("ganjil", background=HITAM)
    app.tabel.pack(fill="both", expand=True, padx=32, pady=(8, 28))
    return frame


def buatHalamanPerforma(app):
    """FUNGSI: membangun halaman Uji Performa (tabel perbandingan 3 algoritma)."""
    frame = tk.Frame(app.konten, bg=HITAM)
    cetakHeaderUI(frame, "Uji Performa")          # fungsi memanggil prosedur

    bar = tk.Frame(frame, bg=HITAM)
    bar.pack(fill="x", padx=32, pady=(0, 14))
    app.tombol_uji = tombol(bar, "Mulai Uji", app.jalankanBenchmark)
    app.tombol_uji.pack(side="left")
    tk.Label(bar, text="100.000 lagu", bg=HITAM, fg=ABU, font=(FONT, 11)).pack(side="left", padx=14)

    app.progres = ttk.Progressbar(frame, mode="indeterminate", style="Biru.Horizontal.TProgressbar")
    app.progres.pack(fill="x", padx=32, pady=(0, 6))
    app.status_uji = tk.Label(frame, text="", bg=HITAM, fg=ABU, font=(FONT, 10), anchor="w")
    app.status_uji.pack(fill="x", padx=32)

    kolom = ("algo", "kompleksitas", "ms", "us", "urutan")
    app.tabel_uji = ttk.Treeview(frame, columns=kolom, show="headings",
                                 style="Gelap.Treeview", height=3)
    for k, teks, lebar, rata in (("algo", "Algoritma", 200, "w"), ("kompleksitas", "Kompleksitas", 140, "center"),
                                 ("ms", "Waktu (ms)", 160, "e"), ("us", "Waktu (µs)", 200, "e"),
                                 ("urutan", "Peringkat", 110, "center")):
        app.tabel_uji.heading(k, text=teks)
        app.tabel_uji.column(k, width=lebar, anchor=rata)
    app.tabel_uji.tag_configure("tercepat", foreground=BIRU_TERANG)
    app.tabel_uji.pack(fill="x", padx=32, pady=(10, 0))
    return frame


def tombol(induk, teks, perintah):
    """Tombol biru bergaya modern dengan efek hover."""
    t = tk.Button(induk, text=teks, command=perintah, bg=BIRU, fg=PUTIH,
                  activebackground=BIRU_TERANG, activeforeground=PUTIH,
                  relief="flat", bd=0, cursor="hand2", font=(FONT, 10, "bold"),
                  padx=22, pady=9)
    t.bind("<Enter>", lambda e: t.config(bg=BIRU_TERANG) if str(t["state"]) != "disabled" else None)
    t.bind("<Leave>", lambda e: t.config(bg=BIRU) if str(t["state"]) != "disabled" else None)
    return t


def tampilkanMenu(app):
    """
    PROSEDUR utama (tanpa nilai kembali): membangun sidebar navigasi dan halaman.
    Di akhir, prosedur ini MEMANGGIL fungsi prosesPengurutan() untuk memuat
    peringkat awal (prosedur memanggil fungsi).
    """
    sidebar = tk.Frame(app, bg=PANEL, width=210)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="♪ Peringkat", bg=PANEL, fg=PUTIH,
             font=(FONT, 16, "bold"), anchor="w").pack(fill="x", padx=24, pady=(30, 28))

    app.konten = tk.Frame(app, bg=HITAM)
    app.konten.pack(side="left", fill="both", expand=True)

    app.halaman = {
        "peringkat": buatHalamanPeringkat(app),
        "performa": buatHalamanPerforma(app),
    }
    app.menu_btn = {}
    for kunci, label in (("peringkat", "Peringkat"), ("performa", "Uji Performa")):
        b = tk.Button(sidebar, text=label, anchor="w", relief="flat", bd=0,
                      bg=PANEL, fg=ABU, activebackground=BIRU_TUA, activeforeground=PUTIH,
                      font=(FONT, 11), padx=24, pady=12, cursor="hand2",
                      command=lambda k=kunci: app.bukaHalaman(k))
        b.pack(fill="x")
        app.menu_btn[kunci] = b

    app.bukaHalaman("peringkat")

    # Prosedur memanggil fungsi: peringkat awal dimuat lewat prosesPengurutan().
    app.hasil, durasi = prosesPengurutan("Merge Sort", app.dataset)
    app.isiTabel()
    app.status.config(text=f"Merge Sort  ·  {fmt(len(app.hasil))} lagu  ·  {durasi:,.1f} ms")


class AplikasiPeringkat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peringkat Lagu")
        self.geometry("1100x680")
        self.minsize(900, 560)
        self.configure(bg=HITAM)

        self.dataset = buat_dataset(100_000)
        self.hasil = []
        self.antrian = queue.Queue()
        self._atur_gaya()
        tampilkanMenu(self)
        self.after(100, self._periksa_antrian)

    # ---------- gaya ttk ----------
    def _atur_gaya(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Gelap.Treeview", background=HITAM, fieldbackground=HITAM,
                    foreground=PUTIH, rowheight=34, borderwidth=0, font=(FONT, 10))
        s.configure("Gelap.Treeview.Heading", background=BIRU_TUA, foreground=PUTIH,
                    font=(FONT, 10, "bold"), relief="flat", padding=8)
        s.map("Gelap.Treeview", background=[("selected", BIRU)],
              foreground=[("selected", PUTIH)])
        s.map("Gelap.Treeview.Heading", background=[("active", BIRU)])
        s.configure("TCombobox", fieldbackground=PANEL_2, background=PANEL_2,
                    foreground=PUTIH, arrowcolor=PUTIH, bordercolor=BIRU_TUA,
                    lightcolor=PANEL_2, darkcolor=PANEL_2)
        s.map("TCombobox", fieldbackground=[("readonly", PANEL_2)],
              foreground=[("readonly", PUTIH)])
        self.option_add("*TCombobox*Listbox.background", PANEL_2)
        self.option_add("*TCombobox*Listbox.foreground", PUTIH)
        self.option_add("*TCombobox*Listbox.selectBackground", BIRU)
        s.configure("Biru.Horizontal.TProgressbar", background=BIRU, troughcolor=PANEL_2,
                    bordercolor=HITAM, lightcolor=BIRU, darkcolor=BIRU)

    # ---------- navigasi ----------
    def bukaHalaman(self, kunci):
        for k, h in self.halaman.items():
            h.pack_forget()
            self.menu_btn[k].config(bg=PANEL, fg=ABU)
        self.halaman[kunci].pack(fill="both", expand=True)
        self.menu_btn[kunci].config(bg=BIRU_TUA, fg=PUTIH)

    # ---------- thread bantu agar UI tidak membeku ----------
    def _periksa_antrian(self):
        try:
            while True:
                callback, arg = self.antrian.get_nowait()
                callback(arg)
        except queue.Empty:
            pass
        self.after(80, self._periksa_antrian)

    # ---------- halaman peringkat ----------
    def isiTabel(self):
        """Menampilkan 100 baris teratas yang cocok dengan kata pencarian."""
        kata = self.var_cari.get().strip().lower()
        self.tabel.delete(*self.tabel.get_children())
        tampil = 0
        for rank, lagu in enumerate(self.hasil, start=1):
            if kata and kata not in lagu.judul.lower() and kata not in lagu.penyanyi.lower():
                continue
            self.tabel.insert("", "end", values=(rank, lagu.judul, lagu.penyanyi, fmt(lagu.putar)),
                              tags=("genap" if tampil % 2 == 0 else "ganjil",))
            tampil += 1
            if tampil >= 100:
                break

    def urutkan(self):
        nama = self.var_algo.get()
        ukuran = int(self.var_ukuran.get().replace(".", ""))
        data = self.dataset[:ukuran]
        self.tombol_urut.config(state="disabled", bg=BIRU_TUA)
        self.status.config(text=f"Mengurutkan dengan {nama}…")

        def kerja():
            # Thread latar memanggil fungsi prosesPengurutan()
            hasil, ms = prosesPengurutan(nama, data)
            self.antrian.put((self._selesai_urut, (nama, hasil, ms)))
        threading.Thread(target=kerja, daemon=True).start()

    def _selesai_urut(self, paket):
        nama, hasil, ms = paket
        self.hasil = hasil
        self.isiTabel()
        self.status.config(text=f"{nama}  ·  {fmt(len(hasil))} lagu  ·  {ms:,.1f} ms")
        self.tombol_urut.config(state="normal", bg=BIRU)

    # ---------- halaman uji performa ----------
    def jalankanBenchmark(self):
        self.tombol_uji.config(state="disabled", bg=BIRU_TUA)
        self.tabel_uji.delete(*self.tabel_uji.get_children())
        self.baris_uji = {}
        for nama, (_, kompleks) in ALGORITMA.items():
            self.baris_uji[nama] = self.tabel_uji.insert(
                "", "end", values=(nama, kompleks, "…", "…", "–"))
        self.progres.start(12)
        self.status_uji.config(text="Menjalankan pengujian…")
        data = self.dataset[:100_000]

        def kerja():
            durasi = {}
            for nama in ALGORITMA:
                _, ms = prosesPengurutan(nama, data)
                durasi[nama] = ms
                self.antrian.put((self._baris_uji, (nama, ms)))
            self.antrian.put((self._selesai_uji, durasi))
        threading.Thread(target=kerja, daemon=True).start()

    def _baris_uji(self, paket):
        nama, ms = paket
        self.tabel_uji.item(self.baris_uji[nama],
                            values=(nama, ALGORITMA[nama][1], f"{ms:,.2f}", f"{ms * 1000:,.0f}", "–"))

    def _selesai_uji(self, durasi):
        urut = sorted(durasi, key=durasi.get)
        for posisi, nama in enumerate(urut, start=1):
            ms = durasi[nama]
            self.tabel_uji.item(self.baris_uji[nama],
                                values=(nama, ALGORITMA[nama][1], f"{ms:,.2f}", f"{ms * 1000:,.0f}", posisi),
                                tags=("tercepat",) if posisi == 1 else ())
        self.progres.stop()
        self.status_uji.config(text=f"Tercepat: {urut[0]}")
        self.tombol_uji.config(state="normal", bg=BIRU)


# =====================================================================
# 5. TITIK MASUK
# =====================================================================
if __name__ == "__main__":
    if "--statistik" in sys.argv:
        benchmarkStatistik()          # perbandingan iteratif vs rekursif di konsol
    else:
        AplikasiPeringkat().mainloop()