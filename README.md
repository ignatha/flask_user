# ignatha/flask_user


Flask-user adalah sebuah paket di flask untuk mempermudah membuat sebuah authentikasi dan manajemen hak akases. Di repo ini saya mencoba membuat sebuah sistem login beserta hak akses role


## Install

Install package yang dibutuhkan ke dalam environment, disarankan menggunakan virtual environment seperti `virtualenv` atau `virtualenvwraper`

```bash
pip install -r requirements.txt
```

## Copy file configurasi
Copy file konfigurasi, dan konfigurasikan sesuai kebutuhan

```bash
cp config.ex.py config.py
```

## Jalankan main.py
jalankan dengan perintah berikut

```bash
python main.py
```

## NB
- Setting SMTP agar menu register bisa konfirmasi email
- Setting user admin di file `config.py` 
- Registrasi menggunakan Email Aktif
- SOAL NO 3 ( its dangerous .. saya terapkan pada data di menu `User`, pada menu hapus HANYA USER ADMIN yang akan memanggil data user sesuai id yang di enkripsikan )
- Soal no 4 konversi ada di menu `Konversi Gambar`
