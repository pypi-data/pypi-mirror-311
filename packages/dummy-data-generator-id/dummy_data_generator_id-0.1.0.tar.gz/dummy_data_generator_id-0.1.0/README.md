# Dummy Data Generator Indonesia

## 🚀 Deskripsi
`dummy-data-generator-id` adalah library Python canggih untuk menghasilkan data dummy Indonesia secara acak dan realistis.

## ✨ Fitur Utama
- Generate nama lengkap (dengan pilihan gender)
- Pembangkit email otomatis
- Nomor telepon Indonesia
- Alamat lengkap
- Pekerjaan dan perusahaan palsu
- Tanggal lahir dengan rentang umur
- Kartu kredit dengan validasi Luhn
- Generate data pengguna utuh

## 🛠️ Instalasi

```bash
pip install dummy-data-generator-id
```

## 💻 Penggunaan Dasar

### Generate Satu Pengguna
```python
from dummy_data_generator import DummyDataGenerator

# Generate satu pengguna
single_user = DummyDataGenerator.generate_user_data()
print(single_user)
```

### Generate Beberapa Pengguna
```python
# Generate 5 pengguna sekaligus
multiple_users = DummyDataGenerator.generate_user_data(5)
```

## 🔍 Metode Tersedia

### Data Pengguna
- `generate_user_data(count=1)`: Generate data pengguna lengkap
- `generate_name(gender=None)`: Generate nama
- `generate_email(name=None)`: Generate email
- `generate_phone()`: Generate nomor telepon
- `generate_address()`: Generate alamat
- `generate_birthdate()`: Generate tanggal lahir
- `generate_job()`: Generate pekerjaan
- `generate_company()`: Generate nama perusahaan

### Data Tambahan
- `generate_credit_card()`: Generate kartu kredit
- `generate_uuid()`: Generate UUID unik
- `generate_username()`: Generate username

## 🤝 Kontribusi
Kami terbuka untuk kontribusi! Silakan buka issue atau kirim pull request.

## 📝 Lisensi
Dilisensikan di bawah MIT License.
