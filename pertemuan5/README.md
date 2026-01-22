ANALISIS PROSES MENGGAMBAR (Garis, Lingkaran, dan Poligon menggunakan Python Turtle)

1. Analisis Proses Menggambar Garis (Algoritma DDA)

Prinsip Dasar

Algoritma Digital Differential Analyzer (DDA) digunakan untuk menggambar garis lurus dengan cara menghitung perubahan koordinat secara bertahap dari titik awal ke titik akhir.

Garis dianggap sebagai sekumpulan titik yang posisinya dihitung satu per satu berdasarkan selisih koordinat.

Tahapan Proses

1. Menentukan dua titik awal dan akhir (x1, y1) dan (x2, y2).
2. Menghitung selisih:
   dx = x2 − x1
   dy = y2 − y1
3. Menentukan jumlah langkah (steps) berdasarkan selisih terbesar:
   steps = max(|dx|, |dy|)
4. Menghitung pertambahan tiap langkah:
   x_inc = dx / steps
   y_inc = dy / steps
5. Turtle digerakkan sedikit demi sedikit dengan:
   x = x + x_inc
   y = y + y_inc
6. Setiap posisi dibulatkan dan digambar sebagai titik garis.

Analisis

* Garis terbentuk dari **kumpulan titik yang berdekatan**
* Turtle hanya berfungsi sebagai alat penampil
* Akurasi garis bergantung pada jumlah langkah
* Penggunaan bilangan pecahan membuat DDA mudah dipahami namun kurang efisien

2. Analisis Proses Menggambar Lingkaran (Midpoint Circle Algorithm)

Prinsip Dasar

Algoritma Midpoint Circle menggambar lingkaran tanpa menggunakan fungsi trigonometri.
Algoritma ini bekerja dengan menentukan posisi titik lingkaran berdasarkan posisi titik tengah (midpoint) antara dua kandidat piksel.

Lingkaran memiliki sifat simetri 8 arah, sehingga cukup menghitung 1 bagian dan menyalinnya ke bagian lain.

Tahapan Proses

1. Menentukan:

   * Titik pusat (xc, yc)
   * Jari-jari r
2. Memulai dari titik atas lingkaran:
   x = 0
   y = r
3. Menghitung parameter keputusan awal:
   p = 1 − r
4. Setiap iterasi:

   * Jika p < 0, titik berikutnya berada di arah horizontal
   * Jika p ≥ 0, titik bergerak diagonal
5. Untuk setiap titik (x, y), ditampilkan 8 titik simetris.
6. Proses berhenti ketika x ≥ y.
7. 
Analisis

* Menggunakan perhitungan integer, lebih efisien
* Tidak membutuhkan sin atau cos
* Lingkaran dibentuk dari titik diskret
* Simetri membuat proses menjadi cepat dan konsisten

3. Analisis Proses Menggambar Poligon

Prinsip Dasar

Poligon adalah bangun tertutup yang tersusun dari beberapa garis lurus.
Dalam implementasi ini, poligon tidak memiliki algoritma khusus, melainkan dibentuk dari gabungan algoritma garis (DDA).


Tahapan Proses

1. Menentukan daftar titik sudut (vertex):

   (x1, y1), (x2, y2), ..., (xn, yn)
   
2. Menghubungkan:

   * Titik ke-1 → ke-2
   * Titik ke-2 → ke-3
   * Titik terakhir → kembali ke titik pertama
3. Setiap sisi digambar menggunakan algoritma garis DDA.
4. Turtle berpindah titik demi titik hingga seluruh sisi terbentuk.

