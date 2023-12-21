from tkinter import*
import os
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
import pygame
import sqlite3
from PIL import Image, ImageTk
import time
from datetime import datetime
from buildbase.digitalClock.digital_clock import DigitalClock

#===============main=====================
class Bill_App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1520x785+0+0")
        self.root.title("Sistem Kasir || GUI || By Kelompok 5")
        bg_color = "#87CEEB"
        title = Label(self.root, text="Sistem Kasir", 
        font=('calibri',30, 'bold'), pady=2, bd=12, bg="#87CEEB", fg="Black", relief=GROOVE)
        title.pack(fill=X)
    #==============input==========================        
        self.products = {} 
        pygame.mixer.init()
    #===============Product========================
        self.cap = None
        self.detected_barcodes = set() 
        self.black_screen = Image.new("RGB", (640, 480), (0, 0, 0))
        self.photo = ImageTk.PhotoImage(image=self.black_screen)
    # ==============Total product price================
        self.selected_products = {} 
        self.selected_indices = {} 
    # ==============Total product price================
        self.product_price = StringVar()
    # ===============Payment==========================
        self.tunai = StringVar()
    # ==============Customer==========================
        self.c_name = StringVar()
        self.member = StringVar()
        self.bill_no = StringVar()
        self.search_bill = StringVar()
    # =============customer retail details======================
        F1 = LabelFrame(self.root, text="Detail Pembeli", font=('calibri', 15, 'bold'), bd=10, fg="Black", bg="#87CEEB")
        F1.place(x=0, y=80, relwidth=1, height=95)

        cname_lbl = Label(F1, text="Kasir: ", bg=bg_color, font=('calibri', 15, 'bold'))
        cname_lbl.grid(row=0, column=0, padx=20, pady=5)
        cname_txt = Entry(F1, width=15, textvariable=self.c_name, font='arial 15', bd=7, relief=GROOVE)
        cname_txt.grid(row=0, column=1, pady=5, padx=10)

        cphn_lbl = Label(F1, text="Member: ", bg="#87CEEB", font=('calibri', 15, 'bold'))
        cphn_lbl.grid(row=0, column=2, padx=20, pady=5)
        cphn_txt = Entry(F1, width=15, textvariable=self.member, font='arial 15', bd=7, relief=GROOVE)
        cphn_txt.grid(row=0, column=3, pady=5, padx=10)

        clock_frame = Frame(F1, bg="yellow")
        clock_frame.grid(row=0, column=4, padx=600, pady=2)  # Atur posisi grid di dalam LabelFrame

        clock = DigitalClock(clock_frame, 200, 10, "#87CEEB", "black", 23)  # Objek DigitalClock harus diberi container yang tepat
        clock.create_clock(200, 30, "#87CEEB", "black", 23)
        clock.update_time()
    # =================Input barang=================
        F2 = LabelFrame(self.root, text="Scan Produk", font=('calibri', 15, 'bold'), bd=10, fg="Black", bg="#87CEEB")
        F2.place(x=5, y=180, width=325, height=485)

        self.label = Label(F2)
        self.label.place(x=10, y=10, width=285, height=150)

        btn_s = Frame(F2)
        btn_s.place(x=20, y=170)
        scan_btn = Button(btn_s, text="Start Scan", command=self.start_scan, width=10, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        scan_btn.grid(row=0, column=1)
        
        btn_ss = Frame(F2)
        btn_ss.place(x=160, y=170)
        stopscan_btn = Button(btn_ss, text="Stop Scan", command=self.stop_scan, width=10, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        stopscan_btn.grid(row=0, column=2)

        man_i = Frame(F2)
        man_i.place(x=10, y=240)
        man_j = Frame(F2)
        man_j.place(x=10, y=265)
        man_k = Frame(F2)
        man_k.place(x=235, y=265)

        manual_in = Label(man_i, text="Manual Input:", bg="#87CEEB", font=('calibri', 13, 'bold'))
        manual_in.grid(row=0, column=3)
        self.man_in = Entry(man_j, width=30, textvariable=self.search_product, font='arial 10', bd=7, relief=GROOVE)
        self.man_in.grid(row=0, column=4, pady=2)
        man_btn = Button(man_k, text="Cari", command=self.search_product, width=5, bd=7, font=('arial', 10, 'bold'), relief=GROOVE)
        man_btn.grid(row=0, column=5)

        search_box = Frame(F2)
        search_box.place(x=10, y=300, width=285, height=140)

        self.search_list = Listbox(search_box, width=39, height=8, font=('calibri', 10, 'bold'))
        self.search_list.pack(pady=1, padx=1)
        self.search_list.bind("<Double-Button-1>", self.add_product_from_search) 
    #=================List Pembelian=================
        F3 = LabelFrame(self.root, text="Daftar Pembelian", font=('calibri', 15, 'bold'), bd=10, fg="Black", bg="#87CEEB")
        F3.place(x=340, y=180, width=810, height=485)

        list_box = Frame(F3)
        list_box.place(x=10, width=690, height=440)

        self.product_list = Listbox(list_box, width=480, height=330, font=('calibri', 15, 'bold'))
        self.product_list.pack(pady=10, padx=10)

        btn_plus = Frame(F3)
        btn_plus.place(x=720, y=5, width=50, height=45)
        tambah_btn = Button(btn_plus, text="+", command=self.tambah_produk, width=3, height=1, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        tambah_btn.grid(row=0, column=0)

        btn_min = Frame(F3)
        btn_min.place(x=720, y=70, width=50, height=45)
        kurang_btn = Button(btn_min, text="-", command=self.kurangi_produk, width=3, height=1, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        kurang_btn.grid(row=0, column=1)

        btn_del = Frame(F3)
        btn_del.place(x=720, y=335, width=50, height=100)
        hapus_btn = Button(btn_del, text="Del", command=self.hapus_produk, width=3, height=4, bd=7, font=('arial', 12, 'bold'), relief=GROOVE)
        hapus_btn.grid(row=0, column=2)
    # =================BillArea======================
        F4 = Frame(self.root, bd=10, relief=GROOVE)
        F4.place(x=1160, y=180, width=350, height=485)

        bill_title = Label(F4, text="Bill Area", font='arial 15 bold', bd=7, relief=GROOVE)
        bill_title.pack(fill=X)
        scroll_y = Scrollbar(F4, orient=VERTICAL)
        self.txtarea = Text(F4, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)
    # =======================ButtonFrame=============
        F5 = LabelFrame(self.root, text="Area Pembayaran", font=('calibri', 14, 'bold'), bd=10, fg="Black", bg="#87CEEB")
        F5.place(x=0, y=670, relwidth=1, height=140)

        m1_lbl = Label(F5, text="Total Belanja", font=('calibri', 20, 'bold'), bg="#87CEEB", fg="black")
        m1_lbl.grid(row=0, column=0, padx=20, pady=10, sticky='W')
        m1_txt = Entry(F5, width=16, textvariable=self.product_price, font='arial 20 bold', bd=7, relief=GROOVE)
        m1_txt.grid(row=0, column=1, padx=18, pady=10)

        m4_lbl = Label(F5, text="Tunai", font=('calibri', 20, 'bold'), bg="#87CEEB", fg="black")
        m4_lbl.grid(row=0, column=2, padx=20, pady=10, sticky='W')
        m4_txt = Entry(F5, width=16, textvariable=self.tunai, font='arial 20 bold', bd=7, relief=GROOVE)
        m4_txt.grid(row=0, column=3, padx=18, pady=10)
    # =======Buttons-======================================        
        btn_f = Frame(F5, bd=7, relief=GROOVE)
        btn_f.place(x=915, width=578, height=90)

        preview_btn = Button(btn_f, command=self.preview_bill, text="Lihat Bill", bd=2, bg="#535C68", fg="white", pady=15, width=12, font='arial 13 bold')
        preview_btn.grid(row=0, column=0, padx=5, pady=5)

        generateBill_btn = Button(btn_f, command=self.bill_area, text="Cetak Struck", bd=2, bg="#535C68", fg="white", pady=15, width=12, font='arial 13 bold')
        generateBill_btn.grid(row=0, column=1, padx=5, pady=5)

        clear_btn = Button(btn_f, command=self.clear_selected_products, text="Hapus", bg="#535C68", bd=2, fg="white", pady=15, width=12, font='arial 13 bold')
        clear_btn.grid(row=0, column=2, padx=5, pady=5)

        exit_btn = Button(btn_f, command=self.exit_app, text="Keluar", bd=2, bg="#535C68", fg="white", pady=15, width=12, font='arial 13 bold')
        exit_btn.grid(row=0, column=3, padx=5, pady=5)

        self.welcome_bill()
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                barcode TEXT PRIMARY KEY,
                                product_name TEXT,
                                price REAL
                            )''')
        self.conn.commit()

    def start_scan(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.update_scan()

    def stop_scan(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

    def update_scan(self):
        ret, frame = self.cap.read() 
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            detected_frame = self.detect_barcode(frame)
            img = Image.fromarray(detected_frame)
            img = img.resize((640, 480))  
            photo = ImageTk.PhotoImage(image=img)
            self.label.config(image=photo)
            self.label.image = photo  
        if self.cap is not None and self.cap.isOpened():
            self.label.after(10, self.update_scan)

    def detect_barcode(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            if barcode_data not in self.detected_barcodes:
                self.detected_barcodes.add(barcode_data) 
                if barcode_data not in self.products: 
                    self.add_product(barcode_data)  
                    self.play_sound()
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    barcode_type = barcode.type
                    text = f"{barcode_data} ({barcode_type})"
            time.sleep(1)  
        return image
    
    def search_product(self):
        search_query = self.man_in.get().lower()  
        matched_products = []
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, price FROM products WHERE product_name LIKE ?", ('%' + search_query + '%',))
        rows = cursor.fetchall()
        for row in rows:
            product_name, price = row
            matched_products.append({'name': product_name, 'price': price}) 
        conn.close()
        self.search_list.delete(0, END) 
        for product in matched_products:
            display_info = f"{product['name']} - Rp.{product['price']}"
            self.search_list.insert(END, display_info)

    def add_product(self, barcode_data):
        self.cursor.execute("SELECT product_name, price FROM products WHERE barcode=?", (barcode_data,))
        result = self.cursor.fetchone()
        if result:
            product_name, price = result
            if barcode_data not in self.selected_products:
                self.selected_products[barcode_data] = {
                    'name': product_name,
                    'price': float(price),
                    'quantity': 1  
            }
                self.product_list.insert(END, f"{product_name} - Rp.{price} - Quantity: 1")
                self.update_total()
            else:
                self.selected_products[barcode_data]['quantity'] += 1  
                self.update_quantity_in_list(barcode_data, self.selected_products[barcode_data]['quantity'])
                self.update_total()
        else:
            messagebox.showerror("Error", f"Product with barcode {barcode_data} not found!")

    def add_product_from_search(self, event):
        selected_index = self.search_list.curselection()  
        if selected_index:
            selected_product = self.search_list.get(selected_index) 
            product_info = selected_product.split(" - ")
            product_name = product_info[0]
            conn = sqlite3.connect("products.db")
            cursor = conn.cursor()
            cursor.execute("SELECT barcode, price FROM products WHERE product_name=?", (product_name,))
            result = cursor.fetchone()
            conn.close()
            if result:
                barcode, price = result
                if barcode not in self.selected_products:  
                    self.selected_products[barcode] = {
                        'name': product_name,
                        'price': float(price),
                        'quantity': 1
                    }
                    self.product_list.insert(END, f"{product_name} - Rp.{price} - Quantity: 1")
                    self.update_total()
                    self.play_sound()  
                    self.man_in.delete(0, END)
                    self.search_list.delete(0, END) 
                else:
                    messagebox.showinfo("Info", "Produk sudah ada dalam pembelian!")

    def play_sound(self):
        pygame.mixer.music.load(r'C:\Users\LENOVO\Desktop\Billing System\Billing System\sound\bip.mp3')  # Ganti dengan path file sesuai tempat (wajin)
        pygame.mixer.music.play()

    def update_quantity_in_list(self, barcode, quantity):
        product_info = f"{self.selected_products[barcode]['name']} - Rp.{self.selected_products[barcode]['price']}"
        items = self.product_list.get(0, END)
        for index, item in enumerate(items):
            if product_info in item:
                self.product_list.delete(index)
                self.product_list.insert(index, f"{product_info} - Quantity: {quantity}")
                break

    def update_total(self):
        total_price = sum(item['price'] * item['quantity'] for item in self.selected_products.values())
        self.product_price.set(f"Rp. {total_price}")

    def tambah_produk(self):
        selected_index = self.product_list.curselection()  
        if selected_index:  #
            selected_product = self.product_list.get(selected_index)  
            product_info = selected_product.split(" - ")
            product_name = product_info[0]
            barcode = ''  
            for barcode_data, item in self.selected_products.items():
                if item['name'] == product_name:
                    barcode = barcode_data
                    break
            if barcode:
                self.add_product(barcode) 
            else:
                messagebox.showerror("Error", "Product not found!")
        else:
            messagebox.showerror("Error", "No product selected. Please select a product from the list.")
    
    def kurangi_produk(self):
        selected_index = self.product_list.curselection()
        if selected_index:
            selected_product = self.product_list.get(selected_index)
            product_info = selected_product.split(" - ")
            product_name = product_info[0]
            barcode = ''
            for barcode_data, item in self.selected_products.items():
                if item['name'] == product_name:
                    barcode = barcode_data
                    break
            if barcode and self.selected_products[barcode]['quantity'] > 1:
                self.selected_products[barcode]['quantity'] -= 1
                self.update_quantity_in_list(barcode, self.selected_products[barcode]['quantity'])
                self.update_total()
            else:
                messagebox.showerror("Error", "Minimum quantity reached!")

    def hapus_produk(self):
        selected_index = self.product_list.curselection()  
        if selected_index: 
            selected_product = self.product_list.get(selected_index)  
            product_info = selected_product.split(" - ")
            product_name = product_info[0]
            price = float(product_info[1].split("Rp.")[1])
            self.product_list.delete(selected_index)
            for barcode, item in list(self.selected_products.items()):
                if item['name'] == product_name and item['price'] == price:
                    del self.selected_products[barcode]
                    self.detected_barcodes.discard(barcode)
                    break  
            self.update_total()

    def welcome_bill(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.txtarea.delete('1.0', END)
        self.txtarea.insert(END, "\tJaya Makmur\n", 'title')
        self.txtarea.insert(END, "======================================\n")
        self.txtarea.insert(END, f"Waktu:\t{current_time}\n")
        self.txtarea.insert(END, f"Kasir:\t{self.c_name.get()}\n")
        self.txtarea.insert(END, f"Member:\t{self.member.get()}\n")
        self.txtarea.insert(END, "======================================\n")
        self.txtarea.tag_configure('title', font=('Cambria', 20, 'bold'))  

    def preview_bill(self):
        if self.c_name.get() == " " or self.member.get() == " ":
            messagebox.showerror("Error", "Customer Details Are Must")
        elif not self.selected_products:
            messagebox.showerror("Error", "No Product Purchased")
        else:
            self.welcome_bill()

            for barcode, item in self.selected_products.items():
                product_name = item['name']
                price = item['price']
                quantity = item['quantity']
                total_price = price * quantity
                self.txtarea.insert(END, f"\n{product_name} x {quantity} \t\t\tRp.{total_price}")
            self.txtarea.insert(END, f"\n\n--------------------------------------")
            total_price = sum(item['price'] * item['quantity'] for item in self.selected_products.values())
            self.txtarea.insert(END, f"\n Total:\t\t\t Rp.{total_price}")

    def bill_area(self):
        if self.c_name.get() == " " or self.member.get() == " ":
            messagebox.showerror("Error", "Customer Details Are Must")
        elif not self.selected_products:
            messagebox.showerror("Error", "No Product Purchased")
        else:
            self.welcome_bill()
            self.product_list.delete(0, END)

            for barcode, item in self.selected_products.items():
                product_name = item['name']
                price = item['price']
                quantity = item['quantity']
                total_price = price * quantity
                self.txtarea.insert(END, f"\n{product_name} x {quantity} \t\t\tRp.{total_price}")

            self.txtarea.insert(END, f"\n--------------------------------------")
            total_price = sum(item['price'] * item['quantity'] for item in self.selected_products.values())
            if self.tunai.get() != '0.0':
                self.txtarea.insert(END, f"\n Tunai:\t\t\tRp.{self.tunai.get()}")
            self.txtarea.insert(END, f"\n Total:\t\t\t Rp.{total_price}")
            kembalian = float(self.tunai.get()) - total_price
            self.txtarea.insert(END, f"\n Kembalian:\t\t\t Rp.{kembalian}")
            self.txtarea.insert(END, f"\n--------------------------------------")
            self.save_bill()
            self.clear_selected_products()

    def clear_selected_products(self):
        self.selected_products = {} 
        self.clear_data() 

    def save_bill(self):
        op = messagebox.askyesno("Save Bill", "Do you want to save the bill?")
        if op > 0:
            if not os.path.exists("bills"):
                os.makedirs("bills")

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d_%H-%M-%S")  

            self.bill_data = self.txtarea.get('1.0', END)
            bill_file_path = "bills/" + str(current_time) + ".txt"  

            f1 = open(bill_file_path, "w")
            f1.write(self.bill_data)
            f1.close()
            messagebox.showinfo("Saved", f"Bill Saved Successfully as {current_time}")
        else:
            return

    def clear_data(self):
        op = messagebox.askyesno("Clear", "Do you really want to Clear?")
        if op > 0:
        # ====================================================
            self.product_price.set("") 
            self.tunai.set("")
            self.welcome_bill() 
            self.detected_barcodes.clear()
            self.product_price.set("")
            self.member.set("")
            self.bill_no.set("")
            self.search_bill.set("")
            self.product_list.delete(0, END)  

    def exit_app(self):
        op = messagebox.askyesno("Exit", "Do you really want to exit?")
        if op > 0:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
        
root = Tk()
obj = Bill_App(root)
root.mainloop()