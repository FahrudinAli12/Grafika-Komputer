UTS
a. Judul ProyekJudul proyek ini adalah "Feeding Frenzy" (atau sesuai dengan caption di baris kode: "Feeding Frenzy - Fix Victory & Crunch").
b. Konsep Grafika yang DigunakanProgram ini tidak menggunakan gambar (sprite) untuk objek utamanya, melainkan menggunakan konsep Grafika Vektor Berbasis Piksel.
*Setiap bentuk dibuat dari koordinat matematika yang dihitung secara real-time.Konsep utamanya meliputi:
*Sistem Koordinat Kartesius: Mengatur posisi benda berdasarkan sumbu $X$ (horizontal) dan $Y$ (vertical). Di layar ini, titik $(0,0)$ berada di pojok kiri atas.
*Double Buffering: Menggunakan pygame.display.flip() untuk memastikan perpindahan antar bingkai (frame) terlihat mulus tanpa berkedip.
*Rendering Loop: Proses menghapus layar, menghitung posisi baru, dan menggambar ulang objek secara terus-menerus (60 kali per detik).
*Z-Ordering Sederhana: Mengatur urutan gambar (misal: gelembung digambar di belakang, ikan di depan) agar menciptakan kedalaman.
c. Algoritma yang DipakaiAda empat algoritma grafika pada kode ini:
*Algoritma DDA (Digital Differential Analyzer):Digunakan untuk menggambar garis lurus pada bar UI dan indikator level. Algoritma ini bekerja dengan menghitung perubahan posisi secara bertahap (inkremental) antar piksel.
*Algoritma Midpoint Circle:Digunakan untuk menggambar mata ikan, gelembung, dan lingkaran efek. Algoritma ini sangat efisien karena hanya menghitung posisi piksel pada 1/8 bagian lingkaran, lalu menduplikasinya ke sisi lain menggunakan prinsip simetri.
*Algoritma Scan-Line Polygon Fill:Digunakan untuk mewarnai tubuh ikan dan hiu. Karena ikan dibentuk dari titik-titik (poligon), algoritma ini bekerja seperti alat "Fill Bucket" yang mengisi warna pada setiap baris horizontal di dalam batasan titik tersebut.
*Transformasi Geometris 2D:Fungsi transform_all menggunakan rumus matematika untuk:
*Translasi: Memindahkan objek ke koordinat tertentu.
*Rotasi: Memutar bintang laut menggunakan fungsi sin dan cos.
*Skala: Memperbesar ukuran ikan saat naik level.
*Refleksi: Membalik arah hadap ikan (kiri/kanan) dengan mengubah tanda koordinatnya.
d. Cara Menjalankan ProgramUntuk menjalankan program ini, ikuti langkah-langkah berikut:
*Instalasi Python: Pastikan Python sudah terinstal di komputer Anda.
*Instalasi Library Pygame: Buka terminal atau Command Prompt, lalu ketik:Bashpip install pygame
*Menyiapkan Asset (Opsional): Jika Anda memiliki gambar latar belakang, beri nama background1.jpg di folder yang sama. Jika tidak ada, program akan otomatis menggunakan latar belakang warna biru laut.
*Eksekusi: Simpan kode ke dalam file (misal: main.py), lalu jalankan dengan perintah:Bashpython main.py
*Kontrol Game:
-Tombol Panah: Menggerakkan ikan ke atas, bawah, kiri, dan kanan.
-Tombol R: Mengulang permainan jika kalah (Game Over).
-Tombol Q: Keluar dari permainan.
