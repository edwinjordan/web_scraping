# Tokopedia Product Scraper

Aplikasi Python untuk scraping halaman dinamis Tokopedia menggunakan Selenium WebDriver.

## Fitur

- Scraping produk dari halaman pencarian Tokopedia
- Mengambil data: nama produk, harga, dan rating
- Chrome WebDriver dalam mode headless
- Auto-scroll untuk memuat minimal 30 produk
- Jeda waktu antar scroll untuk menghindari deteksi bot
- Output disimpan dalam format CSV

## Persyaratan

- Python 3.7 atau lebih tinggi
- Chrome browser (untuk WebDriver)

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/edwinjordan/web_scraping.git
cd web_scraping
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

Jalankan scraper dengan perintah:
```bash
python tokopedia_scraper.py
```

Scraper akan:
1. Membuka halaman pencarian Tokopedia untuk keyword "laptop"
2. Melakukan scroll otomatis untuk memuat produk
3. Mengambil minimal 30 produk
4. Menyimpan hasil ke file `tokopedia_products.csv`

## Struktur Kode

Script `tokopedia_scraper.py` terdiri dari fungsi-fungsi berikut:

- `init_driver()`: Inisialisasi Chrome WebDriver dalam headless mode
- `scrape_data(driver, url, min_products)`: Scraping data produk dari halaman
- `save_to_csv(data, filename)`: Menyimpan data ke file CSV
- `main()`: Fungsi utama yang mengatur proses scraping

## Output

File CSV yang dihasilkan memiliki kolom:
- `name`: Nama produk
- `price`: Harga produk
- `rating`: Rating produk (jika ada)

## Catatan

- Scraper menggunakan mode headless untuk efisiensi
- Delay antar scroll diatur untuk menghindari deteksi bot
- WebDriver dikelola otomatis menggunakan webdriver-manager
- User agent disetel untuk mensimulasikan browser normal

## Lisensi

MIT License