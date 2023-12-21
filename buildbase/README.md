# Digital Clock Library for Tkinter

Digital Clock Library adalah sebuah modul sederhana yang menyediakan fungsionalitas untuk menampilkan jam digital secara real-time dalam aplikasi yang menggunakan Tkinter sebagai GUI toolkit-nya. Library ini memungkinkan pengguna untuk dengan mudah menambahkan dan menampilkan jam digital yang dapat diperbarui secara otomatis pada aplikasi berbasis Tkinter.APOD) API.

## Installastion

```
pip install digital-clock
```
## Penggunaan


Library ini memudahkan pengguna untuk menambahkan jam digital ke dalam aplikasi Tkinter dengan langkah-langkah sederhana:

Inisialisasi objek DigitalClock dengan menentukan parameter seperti `container`, `lebar`, `tinggi`, `warna latar belakang`, `warna tek`s, dan `ukuran font`.
Memanggil metode `create_clock()` untuk membuat tampilan jam digital dengan parameter yang diinginkan.
Memanggil metode `update_time()` untuk memulai pembaruan waktu secara real-time.


## Implementasi

```python
import tkinter as tk
from digital_clock import DigitalClock

root = tk.Tk()
clock_frame = tk.Frame(root, bg="yellow")
clock_frame.pack()

clock = DigitalClock(clock_frame, 200, 100, "yellow", "black", 15)
clock.create_clock(200, 100, "yellow", "black", 15)
clock.update_time()

root.mainloop()
```
