from tkinter import*
from PIL import Image, ImageTk
from employee import employeeClass
from category import categoryClass
from product import productClass
from sales import SalesClass
import sqlite3
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("SCJ Scanform Solution Private Limited Inventory Management System | Developed by Shipra Moharana")
        self.root.config(bg="#F8F3F0")
        #title
        self.icon_title=PhotoImage(file="images/scjlogo.png")
        title= Label(self.root,text="SCJ Inventory Management System",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#C0C0C0",fg="#800000",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=90)

        #BUTTON
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="#F1A177",cursor="hand2").place(x=1110,y=10,height=50,width=150)
        
        #clock
        self.lbl_clock=Label(self.root,text="Welcome To Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15,"bold"),bg="#636363",fg="white")
        self.lbl_clock.place(x=0,y=80,relwidth=1,height=30)

        #LeftMenu Button
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu= Frame(self.root,bd=2,relief=RIDGE,bg="#C1B9B9")
        LeftMenu.place(x=0,y=110,width=200,height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Button(LeftMenu,text="MENU",font=("times new roman",20),bg="#F1A177").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_products=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",18,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
     
        #content
        self.lbl_employee=Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="#dda882",fg="black",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=400,y=150,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Categories\n[0]",bd=5,relief=RIDGE,bg="#4fa8a4",fg="black",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=800,y=150,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Products\n[0]",bd=5,relief=RIDGE,bg="#99c4b0",fg="black",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=400,y=350,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",bd=5,relief=RIDGE,bg="#dacbad",fg="black",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=800,y=350,height=150,width=300)

        #footer
        lbl_footer=Label(self.root,text="IMS Inventory Management System | Developed By Shipra Moharana\n For Any Technical Issue Contact 7846962480",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
#----------------------------------------------------------------------------------------------
    def employee(self):
       self.new_win=Toplevel(self.root)
       self.new_obj=employeeClass(self.new_win)

    def category(self):
       self.new_win=Toplevel(self.root)
       self.new_obj=categoryClass(self.new_win)

    def product(self):
       self.new_win=Toplevel(self.root)
       self.new_obj=productClass(self.new_win)
   
    def sales(self):
       self.new_win=Toplevel(self.root)
       self.new_obj=SalesClass(self.new_win)

    def update_content(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try:
          cur.execute("select * from product")
          product=cur.fetchall()
          self.lbl_product.config(text=f'Total Products\n[{ str(len(product))}]')

       
         #  cur.execute("select * from sales")
         #  sales=cur.fetchall()
         #  self.lbl_sales.config(text=f'Total Sales\n[{ str(len(sales))}]')

          cur.execute("select * from category")
          category=cur.fetchall()
          self.lbl_category.config(text=f'Total Categories\n[{ str(len(category))}]')
       
          cur.execute("select * from employee")
          employee=cur.fetchall()
          self.lbl_employee.config(text=f'Total Employees\n[{ str(len(employee))}]')

          self.lbl_sales.config(text=f'Total Sales\n[{str(len(os.listdir("bill")))}]')

          time_=time.strftime("%I:%M:%S")
          date_=time.strftime("%d-%m-%Y")
          self.lbl_clock.config(text=f"Welcome To Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
          self.lbl_clock.after(200,self.update_content)

       except Exception as ex:
         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def logout(self):
      self.root.destroy()
      os.system("python login.py")

   


if __name__ == "__main__": 
 root= Tk()
 obj= IMS(root)
 root.mainloop()        
