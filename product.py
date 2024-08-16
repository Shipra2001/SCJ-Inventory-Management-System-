from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("SCJ Scanform Solution Private Limited Inventory Management System | Developed by Shipra Moharana")
        self.root.config(bg="#F8F3F0")
        self.root.focus_force()
#---------------------------------
        self.var_emp_searchby = StringVar()
        self.var_emp_searchtxt = StringVar()
        self.var_cat=StringVar() 
        self.var_name=StringVar()
        self.cat_list=[]
        self.fetch_cat()
        
        self.var_pid=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_frame.place(x=20,y=10,width=450,height=490)

        # Title
        title = Label(product_frame, text="Manage Products Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP,fill=X)
        #column1
        lbl_category = Label(product_frame, text="Category", font=("goudy old style", 18), bg="white").place(x=30,y=60)
        lbl_product_name = Label(product_frame, text="Name", font=("goudy old style", 18), bg="white").place(x=30,y=110)
        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 18), bg="white").place(x=30,y=160)
        lbl_quantity = Label(product_frame, text="Quantity", font=("goudy old style", 18), bg="white").place(x=30,y=210)
        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 18), bg="white").place(x=30,y=260)

        #Column 2
        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat,values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        txt_name = Entry(product_frame, textvariable=self.var_name,font=("goudy old style", 15),bg="lightyellow").place(x=150,y=110,width=200)
        txt_price= Entry(product_frame, textvariable=self.var_price,font=("goudy old style", 15),bg="lightyellow").place(x=150,y=160,width=200)
        txt_qty= Entry(product_frame, textvariable=self.var_qty,font=("goudy old style", 15),bg="lightyellow").place(x=150,y=210,width=200)
        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status,values=("Active","Inactive"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150,y=260,width=200)
        cmb_status.current(0)

        #Buttons
        btn_add = Button(product_frame, text="Save",command=self.add,font=("goudy old style", 15), bg="#3792cb", fg="black", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_frame, text="Update",command=self.update, font=("goudy old style", 15), bg="#1fd655", fg="black", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_frame, text="Delete",command=self.delete, font=("goudy old style", 15), bg="#F6465B", fg="black", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_frame, text="Clear",command=self.clear, font=("goudy old style", 15), bg="#BDBDBD", fg="black", cursor="hand2").place(x=340, y=400, width=100, height=40)

        
        search_frame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="#F8F3F0")
        search_frame.place(x=500, y=10, width=620, height=90)

        #Options for combobox-------------------------
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_emp_searchby, values=("Select", "Category", "Name"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(search_frame, textvariable=self.var_emp_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)
        btn_search = Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15), bg="#FF7600", fg="black", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

#Product Details---------------------------------------------------
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=500,y=130,width=780,height=520)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(p_frame,columns=("pid","Category","Name","Price","Quantity","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid",text="pid")
        self.productTable.heading("Category",text="Category")
        self.productTable.heading("Name",text="Name")
        self.productTable.heading("Price",text="Price")
        self.productTable.heading("Quantity",text="Quantity")
        self.productTable.heading("Status",text="Status")
                                          
        self.productTable["show"]="headings"

        self.productTable.column("pid",width=90)
        self.productTable.column("Category",width=100)
        self.productTable.column("Name",width=100)
        self.productTable.column("Price",width=100)
        self.productTable.column("Quantity",width=100)
        self.productTable.column("Status",width=100)
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)


        self.show()
#--------------------------------------------------------------------------
    def fetch_cat(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            self.cat_list.append("Empty")
            if len(cat)>0:
             del self.cat_list[:]
             self.cat_list.append("Select")
             for i in cat:
                self.cat_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)



    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All Fields Are Required",parent=self.root)
            else:
                cur.execute("Select * from product where Name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present",parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Name,Price,Quantity,Status) values(?,?,?,?,?)",(
                                self.var_cat.get(),
                                self.var_name.get(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                            
                    ))
                    con.commit()
                    messagebox.showinfo("Success","product Details Added Successfuly",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from  product")
            rows=cur.fetchall() 
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        # print(row)
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_name.set(row[2]),
        self.var_price.set(row[3]),
        self.var_qty.set(row[4]),
        self.var_status.set(row[5]),
    
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please Select Product From List",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Name=?,Price=?,Quantity=?,Status=? where pid=?",(
                               self.var_cat.get(),
                                self.var_name.get(),
                                self.var_price.get(),
                                self.var_qty.get(),
                                self.var_status.get(),
                                self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfuly")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product From List",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==TRUE:
                     cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                     con.commit()
                     messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                     self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def clear(self):
        self.var_cat.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")
        self.var_emp_searchtxt.set("")
        self.var_emp_searchby.set("Select")
        self.show()

    def search(self):
     con = sqlite3.connect(database=r'ims.db')
     cur = con.cursor()
     try:
        if self.var_emp_searchby.get() == "Select":
            messagebox.showerror("Error", "Select Search By Option", parent=self.root)
        elif self.var_emp_searchtxt.get() == "":
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
        else:
            search_by = self.var_emp_searchby.get().lower()
            search_txt = f"%{self.var_emp_searchtxt.get()}%"
            query = f"SELECT * FROM product WHERE {search_by} LIKE ?"
            cur.execute(query, (search_txt,))
            rows = cur.fetchall()
            if rows:
                self.productTable.delete(*self.productTable.get_children())
                for row in rows:
                    self.productTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No Record Found!", parent=self.root)
     except Exception as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)




if __name__ == "__main__": 
    root = Tk()
    obj = productClass(root)
    root.mainloop()