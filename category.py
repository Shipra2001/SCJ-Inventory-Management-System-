from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("SCJ Scanform Solution Private Limited Inventory Management System | Developed by Shipra Moharana")
        self.root.config(bg="#F8F3F0")
        self.root.focus_force()
        
        # Variables
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()

        # Title
        lbl_title = Label(self.root, text="Manage Product Category", font=("gaudy old style", 30), bg="#184a45", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        lbl_category_name = Label(self.root, text="Enter Category Name", font=("gaudy old style", 30), bg="white")
        lbl_category_name.place(x=50, y=100)
        
        text_category_name = Entry(self.root, textvariable=self.var_cat_name, font=("gaudy old style", 18), bg="lightyellow")
        text_category_name.place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="ADD",command=self.add, font=("gaudy old style", 18), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)
        
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("gaudy old style", 18), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)

        # Category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=500, height=170)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.category_table = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="CID")
        self.category_table.heading("name", text="Name")
        self.category_table["show"] = "headings"
        self.category_table.column("cid", width=100)
        self.category_table.column("name", width=100)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        #Images----------------
        self.im1=Image.open("images/sw1.png")
        self.im1=self.im1.resize((550,300),Image.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=300)

        self.im2=Image.open("images/sc2.jpg")
        self.im2=self.im2.resize((550,300),Image.LANCZOS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RIDGE)
        self.lbl_im2.place(x=670,y=300)
        self.show()
#Functions--------------------------------------------------------------------------------------

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_name.get()=="":
                messagebox.showerror("Error","Category name is required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_cat_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present, try a different",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(?)",(
                                self.var_cat_name.get(),
                                
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfuly")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from  category")
            rows=cur.fetchall() 
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.category_table.focus()
        content=(self.category_table.item(f))
        row=content['values']
        # print(row)
        self.var_cat_id.set(row[0])
        self.var_cat_name.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select category from list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Try Again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==TRUE:
                     cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                     con.commit()
                     messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                    self.show()
                    self.var_cat_id.set("")
                    self.var_cat_name.set("")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    

if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
