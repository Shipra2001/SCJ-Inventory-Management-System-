from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("SCJ Scanform Solution Private Limited Inventory Management System | Developed by Shipra Moharana")
        self.root.config(bg="#F8F3F0")
        self.root.focus_force()
        
        self.bill_list=[]
        self.var_invoice = StringVar()
        
        # Title
        lbl_title = Label(self.root, text="View Customer Bills", font=("gaudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        lbl_invoice = Label(self.root, text="Invoice No. ", font=("times new roman", 15), bg="white")
        lbl_invoice.place(x=50, y=100)
        txt_invoice = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="lightyellow")
        txt_invoice.place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search",command=self.search,font=("times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("times new roman", 15, "bold"), bg="lightgrey", cursor="hand2")
        btn_clear.place(x=490, y=100, width=120, height=28)
        
        # Bill list
        sales_frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_frame, orient=VERTICAL)
        self.sales_List = Listbox(sales_frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.config(command=self.sales_List.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.sales_List.pack(fill=BOTH, expand=1)
        self.sales_List.bind("<<ListboxSelect>>", self.get_data)

        # Bill Area
        bill_frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=330, height=330)

        lbl_title2 = Label(bill_frame, text=" Customer Bill Area", font=("gaudy old style", 20), bg="orange")
        lbl_title2.pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)
        self.bill_area = Text(bill_frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.config(command=self.bill_area.yview)
        scrolly2.pack(side=RIGHT, fill=Y)
        self.bill_area.pack(fill=BOTH, expand=1)

        # Image
        self.bill_photo = Image.open("images/cat2.jpg")
        self.bill_photo = self.bill_photo.resize((500, 500), Image.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=730, y=100)

        self.show()

    def show(self):
        del self.bill_list[:]
        self.sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        self.bill_area.delete('1.0', END)
        index_ = self.sales_List.curselection()
        if index_:
            file_name = self.sales_List.get(index_)
            fp=open(f'bill/{file_name}', 'r')
            for i in fp:
                    self.bill_area.insert(END,i)
            fp.close()
    
    def search(self):
     if self.var_invoice.get() == "":
        messagebox.showerror("Error", "Invoice no. is required", parent=self.root)
     else:
        if self.var_invoice.get() in self.bill_list:
            with open(f'bill/{self.var_invoice.get()}.txt', 'r') as fp:
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END, i)
        else:
            messagebox.showerror("Error", "Invalid Invoice no.", parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)

    

if __name__ == "__main__": 
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()
