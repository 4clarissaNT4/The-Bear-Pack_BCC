# 🛒 Sistem Promosi Otomatis untuk Supermarket Jack

## 📌 Deskripsi
Program ini merupakan **sistem rekomendasi otomatis** untuk merencanakan promosi harian di jaringan supermarket Jack.  
Algoritma menggunakan **data kategori produk, margin, elastisitas harga, serta kalender event Indonesia** untuk menghasilkan promosi yang:

- Mengoptimalkan **profit incremental harian**  
- Menjaga keseimbangan antara **Trade Promotion** (didukung pemasok) dan **In-Store Promotion** (inisiatif toko)  
- Memaksimalkan **ROI promosi** dengan memperhitungkan biaya diskon, biaya display, serta dukungan pemasok  

Output berupa file CSV rencana promosi harian dan ringkasan performa per toko.

---

## ⚙️ Fitur Utama
- 📊 Pemilihan produk promosi otomatis (berdasarkan elastisitas, margin, brand diversity)  
- 🗓️ Kalender event Indonesia (Payday, Ramadhan, Lebaran, Hari Kemerdekaan, Tanggal Kembar, Natal, dll.)  
- 💰 Perhitungan ROI & incremental profit tiap kampanye  
- 📂 Ekspor CSV otomatis untuk rencana promosi & ringkasan performa toko  
- 🔍 Analisis kategori & insights (profit rata-rata, ROI, uplift, Trade vs In-Store)  

---

## 🛠️ Persyaratan Sistem
- **Python 3.8+** → [Download](https://www.python.org/downloads/)  
  (centang *Add Python to PATH* saat instalasi)  
- Library standar (sudah ada di Python):  
  `argparse, dataclasses, datetime, csv, os, random`

---

## 🚀 Cara Menjalankan
1. Clone repository:  
   ```bash
   git clone https://github.com/4clarissaNT4/The-Bear-Pack_BCC.git
2. Masuk ke folder project:
    ```bash
    cd The-Bear-Pack_BCC

3. Jalankan program:
    ```bash
    python supermarket_optimizer.py

## 📂 Output

- promotion_plan_optimized.csv → berisi detail promosi per toko (kategori, tipe promosi, diskon, profit, ROI, dll.)

- promotion_summary_optimized.csv → ringkasan per toko (jumlah promosi, total incremental profit, rata-rata ROI)

## 👨‍💻 Author

Sistem dikembangkan untuk studi kasus CompfestMarket.
Dibuat oleh tim The Bear Pack.
