# DAPODIK SCRAPE 1.3.1
# (C) 2024 by Dhyandra Raka

from bs4 import BeautifulSoup # untuk instal run 'pip install bs4' di CMD
import requests # untuk instal run 'pip install requests' di CMD
from requests.exceptions import ConnectionError
import json, time, sys

arr_url = []
arr_sekolah_desa = []

# ganti pathfile untuk save berkas
berkas = "D:\\myrepocode\\dapodik-data\\"

# Kode Kecamatan bisa dilihat di file kaltim_norm.json (JSON)
# atau di file list_kec_kaltim.xlsx (XLSX)

# kode_kec mengikuti 4 angka kode_kab + nomor urut kecamatan
# Contoh kode_kec untuk Paser = ['160101','160109','160110','160102','160103','160104','160105','160106','160107','160108']
# Masukkan kode kec di bawah untuk satu kecamatan
#
kode_kecamatan_6401 = ['160101','160109','160110','160102','160103','160104','160105','160106','160107','160108']
kode_jenjang = ["tk", "kb", "sd", "smp", "sma", "smk"]

# Dikerenakan masalah koneksi yang cenderung kurang stabil, disertakan fungsi reconnect() untuk menghubungkan kembali ke URL
# reconnect() parameter :   - u -> String :: URL yang akan diakses
#                           - max_att -> Integer :: max percobaan untuk reconnect

def reconnect(u, max_att):
    if max_att == 0:
        print("Nilai minimal untuk max_iter adalah 1.")
    else:
        att_iter = 1
        while(att_iter <= max_att):
            try:
                print("Mencoba menghubungkan kembali ke URL : percobaan ke-%d"%(att_iter))
                r = requests.get(u)
                return r
            except ConnectionError:
                time.sleep(2)
                if att_iter <= max_att:
                    att_iter =+ 1
                else: # continue atau Isi pesan error atau TO-DO sebagai alternatif
                    print("Gagal : Timeout setelah %s percobaan."%(max_att))

# FUNGSI ambil_sekolah() -> untuk mengambil data sekolah
# ambil_sekolah() parameters : - kec -> String :: masukkan kode kecamatan yang akan diambil
#                              - thn -> Integer :: Masukkan tahun ajaran
#                              - smt -> Integer (1,2) ::                             
# - j -> String :: jenjang yang akan diambil -> "sd" untuk SD, "smp" untuk SMP, "sma" untuk SMA, dst

def ambil_sekolah(kec, thn, smt, j):
    flag_switcher = 0
    
    if smt == 1 | 2:
        nama_file = "%s_%s.json"%(kec, j)
        print("Mengambil JSON : %s"%(kec))
        sekolah_url = "https://dapo.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah=%s&semester_id=%s%s&bentuk_pendidikan_id=%s"%(kec, thn, smt, j)
        try:        
            r2 = requests.get(sekolah_url)
        except ConnectionError:
            r2 = reconnect(sekolah_url, 2)
        
        y = r2.content
        str_y = y.decode("utf-8")
        print("Parsing JSON : %s"%(kec))
        x = str(str_y)
        x = json.loads(x)
        i = 0

        if len(x) == 0:
            print("Data sekolah %s di Kecamatan %s tidak ada."%(j, kec))
        else:
        #iter link
            print("Mengambil data sekolah : %s"%(kec))
            while(i < len(x)):
                dt_web = x[i]['sekolah_id_enkrip']
                dt_web = dt_web.replace('                                                                                ','')
                dt_nama = x[i]['nama']
                dt_sekolah = x[i]['bentuk_pendidikan']
                guru = x[i]['ptk']
                pd = x[i]['pd']
                rombel = x[i]['rombel']
                status_sekolah = x[i]["status_sekolah"]
                induk_kec = x[i]['induk_kecamatan']

                pend_exp = ['SPS']

                if dt_sekolah not in pend_exp:
                    url_prefix = "https://dapo.kemdikbud.go.id/sekolah/%s"%(dt_web)
                    # Array temp adalah array informasi di depan, dimasukkan sebelum membuka setiap halaman sekolah 
                    temp = [dt_nama, url_prefix, guru, pd, rombel, status_sekolah]
                    arr_url.append(temp)
                i += 1
            '''except:
                print("Tidak bisa mengambil data sekolah kecamatan : %s"%(kec))
                sys.exit(0)'''
        print(arr_url)
        print("Membuat JSON sekolah ...")
        for w in arr_url:
            try:
                rq = requests.get(w[1])
            except ConnectionError:
                rq = reconnect(w[1], 2)
            
            bs = BeautifulSoup(rq.content, "html.parser")
            try:
                p1 = bs.find('div', {'id':'kontak'})
            except:
                print("Tidak dapat mengambil kontak sekolah : %s"%(w[0]))
            
            try:
                find_items = p1.find_all('p')
            except:
                print("Tidak dapat mengambil div kontak <p> dari %s"%(w[0]))
            
            try:
                alamat_fixed = find_items[0].get_text()
                alamat_fixed = alamat_fixed.replace("Alamat : ", '')
            except:
                alamat_fixed = ""
            
            try:
                deskel_fixed = find_items[3].get_text()
                deskel_fixed = deskel_fixed.replace("Desa / Kelurahan : ", '')
                deskel_fixed = deskel_fixed.lower()
            except:
                deskel_fixed = ""

            json_sekolah = {
                "sekolah_url": w[1], 
                "nama": w[0],
                "status_sekolah": w[5],
                "alamat": alamat_fixed,
                "deskel": deskel_fixed,
                "jml_PD": w[3],
                "jml_guru": w[2],
                "jml_rombel": w[4]
            }
            arr_sekolah_desa.append(json_sekolah)
            print(json_sekolah)
            time.sleep(2)
            flag_switcher = 1

        print("Menulis data ...")
        if flag_switcher == 1:
            try:
                with open(berkas+nama_file, 'w', encoding="utf-8") as f:
                    json.dump(arr_sekolah_desa, f)
                    #f.write("%s\n"%([v for v in arr_sekolah_desa]))
                    print("Data output %s selesai disimpan."%(nama_file))
                    f.close()
                    
            except:
                print("Gagal membuat file kecamatan pada jenjang : %s"%(j))
        else:
            print("Tidak ada data yang diambil. Menutup program ...")
            sys.exit(0)
            '''temp.clear()
            arr_sekolah_desa.clear()
            arr_url.clear()'''
    else:
        print("Input Semester tidak sesuai. Silakan input 1 jika semester ganjil dan 2 untuk semester genap")
        sys.exit(0)

# Contoh pemakaian :
print(ambil_sekolah('160101', 2023, 4, "sd"))