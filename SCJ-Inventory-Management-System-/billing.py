from tkinter import *
from PIL import Image, ImageTk
from tkinter import Tk,ttk, messagebox
import sqlite3
import time
import os
import tempfile

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("SCJ Scanform Solution Private Limited Inventory Management System | Developed by Shipra Moharana")
        self.root.config(bg="#F8F3F0")
        self.cart_list=[]
        self.chk_print=0
        
        # Title
        self.icon_title = PhotoImage(file="images/scjlogo.png")
        title = Label(self.root, text="SCJ Inventory Management System", image=self.icon_title, compound=LEFT, 
                      font=("times new roman", 40, "bold"), bg="#C0C0C0", fg="#800000", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=90)

        # BUTTON
        btn_logout = Button(self.root, text="Logout",command=self.logout,font=("times new roman", 15, "bold"), bg="#F1A177", cursor="hand2")
        btn_logout.place(x=1110, y=10, height=50, width=150)
        
        # Clock
        self.lbl_clock = Label(self.root, text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15, "bold"), bg="#636363", fg="white")
        self.lbl_clock.place(x=0, y=80, relwidth=1, height=30)

        # Product Frame
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE)
        ProductFrame1.place(x=6, y=120, width=410, height=490)
        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg='#262626', fg="white")
        pTitle.pack(side=TOP, fill=X)

        # Product Search Frame-----------------------------------------------------------
        self.var_search = StringVar()      
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product | By Name ", font=("times new roman", 15, "bold"), bg="white", fg="green")
        lbl_search.place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_search.place(x=5, y=45)

        text_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15), bg="lightyellow")
        text_search.place(x=135, y=47, width=150, height=22)

        btn_search = Button(ProductFrame2, text="Search", command=self.search,font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=290, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All",command=self.show, font=("goudy old style", 15), bg="#083531", fg="white", cursor="hand2")
        btn_show_all.place(x=290, y=10, width=100, height=25)

        # Product Details Frame-----------------------------------------------------------   
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=1, y=140, width=398, height=320)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid","Category", "Name", "Price", "Quantity", "Status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid", text="pid")
        self.product_Table.heading("Category", text="Category")
        self.product_Table.heading("Name", text="Name")
        self.product_Table.heading("Price", text="Price")
        self.product_Table.heading("Quantity", text="Quantity")
        self.product_Table.heading("Status", text="Status")

        self.product_Table["show"] = "headings"

        self.product_Table.column("pid", width=50)
        self.product_Table.column("Category", width=100)
        self.product_Table.column("Name", width=100)
        self.product_Table.column("Price", width=80)
        self.product_Table.column("Quantity", width=60)
        self.product_Table.column("Status", width=90)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="Note: Enter 0 Quantity to remove product from the Cart", 
                         font=("goudy old style", 12), anchor='w', bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)

        #Customer Frame-------------------------------------------------------------------------
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE)
        CustomerFrame.place(x=420, y=120, width=530, height=70)
        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg='#262626', fg='white').pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13), bg="lightyellow").place(x=380, y=35, width=140)

        # Cal Cart Frame--------------------------------------------
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE)
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=310)

        # Calculator Frame--------------------------------------------
        self.var_cal_input = StringVar()
        Cal_Frame = Frame(Cal_Cart_Frame, bd=9, relief=RIDGE, bg="white")
        Cal_Frame.place(x=5, y=10, width=268, height=340)

        txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=('arial', 15, "bold"), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(Cal_Frame, text='7', font=('arial', 15, 'bold'), command=lambda: self.get_input(7), bd=5, width=4, pady=7, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(Cal_Frame, text='8', font=('arial', 15, 'bold'), command=lambda: self.get_input(8), bd=5, width=4, pady=7, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(Cal_Frame, text='9', font=('arial', 15, 'bold'), command=lambda: self.get_input(9), bd=5, width=4, pady=7, cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(Cal_Frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5, width=4, pady=7, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(Cal_Frame, text='4', font=('arial', 15, 'bold'), command=lambda: self.get_input(4), bd=5, width=4, pady=7, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(Cal_Frame, text='5', font=('arial', 15, 'bold'), command=lambda: self.get_input(5), bd=5, width=4, pady=7, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(Cal_Frame, text='6', font=('arial', 15, 'bold'), command=lambda: self.get_input(6), bd=5, width=4, pady=7, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(Cal_Frame, text='-', font=('arial', 15, 'bold'), command=lambda: self.get_input('-'), bd=5, width=4, pady=7, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(Cal_Frame, text='1', font=('arial', 15, 'bold'), command=lambda: self.get_input(1), bd=5, width=4, pady=7, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(Cal_Frame, text='2', font=('arial', 15, 'bold'), command=lambda: self.get_input(2), bd=5, width=4, pady=7, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(Cal_Frame, text='3', font=('arial', 15, 'bold'), command=lambda: self.get_input(3), bd=5, width=4, pady=7, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(Cal_Frame, text='*', font=('arial', 15, 'bold'), command=lambda: self.get_input('*'), bd=5, width=4, pady=7, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(Cal_Frame, text='0', font=('arial', 15, 'bold'), command=lambda: self.get_input(0), bd=5, width=4, pady=7, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(Cal_Frame, text='C', font=('arial', 15, 'bold'), command=self.clear_cal, bd=5, width=4, pady=7, cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(Cal_Frame, text='=', font=('arial', 15, 'bold'), command=self.perform_cal, bd=5, width=4, pady=7, cursor="hand2").grid(row=4, column=2)
        btn_div = Button(Cal_Frame, text='/', font=('arial', 15, 'bold'), command=lambda: self.get_input('/'), bd=5, width=4, pady=7, cursor="hand2").grid(row=4, column=3)

        # Cart Frame--------------------------------------------
        Cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        Cart_Frame.place(x=280, y=8, width=245, height=300)
        self.cartTitle = Label(Cart_Frame, text="Cart \t Total Product: [0]", font=("goudy old style", 15), bg='lightgray')
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(Cart_Frame, columns=("pid","Category","Name","Price","Quantity"),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid", text="pid")
        self.CartTable.heading("Category",text="Category")
        self.CartTable.heading("Name", text="Name")
        self.CartTable.heading("Price", text="Price")
        self.CartTable.heading("Quantity", text="Quantity")


        self.CartTable["show"] = "headings"
        self.CartTable.column("pid", width=40)
        self.CartTable.column("Category", width=100)
        self.CartTable.column("Name", width=90)
        self.CartTable.column("Price", width=90)
        self.CartTable.column("Quantity", width=60)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ADD CART WIDGET FRAME--------------------------------------------
        self.var_pid = StringVar()
        self.var_category=StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=500, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per Qty", font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15), bg="lightyellow", state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15), bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart, font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=180, y=70, width=150, height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update Cart", command=self.add_update_cart,font=("times new roman", 15, "bold"), bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        # Billing Area--------------------------------------------
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=953, y=120, width=315, height=380)
        BTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # Billing Buttons--------------------------------------------
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=480, width=315, height=380)
        self.lbl_amnt = Label(billMenuFrame, text='Bill Amount\n[0]', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=107, height=70)

        self.lbl_discount = Label(billMenuFrame, text='Discount\n[5%]', font=('goudy old style', 15, 'bold'), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=113, y=5, width=105, height=70)
        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n[0]', font=('goudy old style', 15, 'bold'), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=221, y=5, width=90, height=70)

        btn_print = Button(billMenuFrame, text='Print', command=self.print_bill, font=("goudy old style", 15, "bold"), bg="lightgreen", cursor="hand2")
        btn_print.place(x=2, y=80, width=107, height=50)
        btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, font=("goudy old style", 15, "bold"), bg="gray", cursor="hand2")
        btn_clear_all.place(x=113, y=80, width=105, height=50)
        btn_generate = Button(billMenuFrame, text='Generate \n Bill',command=self.generate_bill,font=("goudy old style", 14, "bold"), bg="#009688", fg="white", cursor="hand2")
        btn_generate.place(x=221, y=80, width=90, height=50)


        # Footer--------------------------------------------
        footer = Label(self.root, text="SCJ Inventory Management System | Developed By Shipra Moharana \nFor any Technical Issues contact: 784xxxxxxx",
                       font=("times new roman", 12), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        self.show()
        # self.bill_top
        self.update_date_time()

#ALL FUNCTIONS------------------------------------------------------------------------------------
    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT pid, Category, Name, Price, Quantity, Status FROM product where Status='Active'")
            rows = cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
            con.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def search(self):
     con = sqlite3.connect(database=r'ims.db')
     cur = con.cursor()
     try:
        if self.var_search.get() == "":
            messagebox.showerror("Error", "Search input is required", parent=self.root)
        else:
            # Corrected the SQL query by removing the extra single quote
            cur.execute("SELECT pid, Category, Name, Price, Quantity, Status FROM product WHERE Name LIKE '%" + self.var_search.get() + "%' and Status='Active'")
            rows = cur.fetchall()
            if rows:
                self.product_Table.delete(*self.product_Table.get_children())
                for row in rows:
                    self.product_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No Record Found!", parent=self.root)
     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
     finally:
        con.close()

    def get_data(self, ev):
     f = self.product_Table.focus()
     content = (self.product_Table.item(f))
     row = content['values']
     self.var_pid.set(row[0])  # Corrected to set the correct index for pid
     self.var_pname.set(row[2])
     self.var_price.set(row[3])
     self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
     self.var_stock.set(row[4])
     self.var_category.set(row[1])  # Added to capture the category
     self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_category.set(row[1])  # Added to capture the category
        self.var_pname.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.lbl_inStock.config(text=f"In Stock [{str(row[5])}]")
        self.var_stock.set(row[5])
        self.var_qty.set(row[4])


    def add_update_cart(self):
     if self.var_pid.get() == '':
        messagebox.showerror('Error', "Please select a product from the list", parent=self.root)
     elif self.var_qty.get() == '':
        messagebox.showerror('Error', "Quantity is required", parent=self.root)

     elif int(self.var_qty.get()) > int(self.var_stock.get()):
        messagebox.showerror('Error', "Invalid Quantity\nPlease enter a valid quantity", parent=self.root)
     else:
        price_cal=self.var_price.get()
        cart_data =[self.var_pid.get(),self.var_category.get(),self.var_pname.get(), price_cal, self.var_qty.get(),self.var_stock.get()]

        #Update Cart-----------
        present='no'
        index_=0
        for row in self.cart_list:
           if self.var_pid.get()== row[0]:
              present='yes'
              break
           index_+=1
        if present=='yes':
           op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update / Remove from the Cart List?",parent=self.root)
           if op==True:
              if self.var_qty.get()=="0":
                 self.cart_list.pop(index_) 
              else:
                 self.cart_list[index_][4]=self.var_qty.get() #qty

        else:
           self.cart_list.append(cart_data)
        
        self.show_cart()
        self.bill_updates()


    def show_cart(self):
     try:
        self.CartTable.delete(*self.CartTable.get_children())
        for row in self.cart_list:
            self.CartTable.insert('', END, values=row)
     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def bill_updates(self):
       self.bill_amnt=0
       self.net_pay=0
       self.discount=0
       for row in self.cart_list:
        self.bill_amnt=self.bill_amnt+(float(row[3])*int(row[4]))

       self.discount=(self.bill_amnt*5)/100

       self.net_pay=self.bill_amnt-self.discount
       self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
       self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
       self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
       
    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please Add Product to the Cart", parent=self.root)
        else:
            #BILL TOP
            self.bill_top()   
            #BILL MIDDLE
            self.bill_middle()
            #BILL BOTTOM
            self.bill_bottom()
                        
            # Save the bill to a file
            fp=open(f'bill/{str(self.invoice)}.txt', 'w') 
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            
            messagebox.showinfo('Saved', "Bill has been generated/Saved in Backend", parent=self.root)
            self.chk_print = 1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t   SCJ Inventory
 Phone No. 91784xxxxx, Okhla-110020
{str("="*36)}
 Customer Name: {self.var_cname.get()}
 Ph No. {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*36)}
 Product Name\t\tQTY\tPrice
{str("-"*36)}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)
        print("Bill Top Content Inserted")

    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
         for row in self.cart_list:
            pid=row[0]
            name=row[2]
            qty=int(row[5])-int(row[4])
            if int(row[4])==int(row[5]):
               status='Inactive'
            if int(row[4])!=int(row[5]):
               status='Active'

            price=float(row[3])*int(row[4])
            price=str(price)
            self.txt_bill_area.insert(END,"\n "+name+"\t\t"+row[4]+"\tRs."+price)
            #Update Qty in product table
            cur.execute('Update product set Quantity=?, status=? where pid=?',(
               qty,
               status,
               pid
               ))
            con.commit()
         con.close()
         self.show()
        except Exception as ex:
         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

            # self.show() 
       
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*36)}
 Bill Amount\t\t\tRs.{self.bill_amnt}
 Discount\t\t\tRs.{self.discount}
 Net Pay\t\t\tRs.{self.net_pay}
{str("="*36)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)
        self.clear_cart()

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart ()
        self.chk_print=0

    def print_bill(self):
       if self.chk_print==1:
          messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
          new_file=tempfile.mktemp('.txt')
          open(new_file,'w').write(self.txt_bill_area.get(1.0,END))
          os.startfile(new_file,'print')
       else:
          messagebox.showerror('Print',"Please generate bill to print the receipt",parent=self.root)
          

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")

        self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def logout(self):
       self.root.destroy()
       os.system("python login.py")   
        
if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
