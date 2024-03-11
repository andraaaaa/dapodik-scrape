# dapodik-scrape
Scraper Informasi Sekolah Melalui Web Pauddikdasmen menurut Wilayah.

## Fungsi
- **ambil_sekolah()** untuk mengambil data sekolah di kecamatan tertentu
  
  | Parameter | Tipe Data | Deskripsi |
  | --------- | --------- | --------- |
  | kec | String | Kode Kecamatan. List bisa dilihat di file JSON master_negara_1.json |
  | thn | Integer | Tahun Ajaran |
  | smt | Integer, 1 atau 2 | Semester. Isi 1 untuk Ganjil dan 2 untuk Genap |
  | j | String | Jenjang Pendidikan<br>```j = ["tk", "kb", "sd", "smp", "sma", "smk"] ``` |

  
- [OPTIONAL] **reconnect()** sebagai opsi reconnect apabila jaringan kurang stabil

  | Parameter | Tipe Data | Deskripsi |
  | --------- | --------- | --------- |
  | u | String | Alamat URL |
  | max_att | Integer, minimal 1 | Maksimal Percobaan untuk akses URL jika gagal mengambil data |

**Versi 1.3.1 dibuat dengan Python 3.10** 
