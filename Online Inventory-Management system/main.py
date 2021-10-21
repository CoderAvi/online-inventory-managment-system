#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all the modules
from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime
import math
conn=sqlite3.connect("storedb.db")
c=conn.cursor()

date=datetime.datetime.now().date()
#temporary list like sessions
products_list=[]
product_price=[]
product_quantity=[]
product_id=[]


class Application:
    def __init__(self,master,*args,**kwargs):
        self.master=master
        self.left=Frame(master,width=700,height=768,bg='white')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=666, height=768, bg='lightblue')
        self.right.pack(side=RIGHT)

        #components
        self.heading=Label(self.left,text="AVI'S INVENTORY SYSTEM",font=('arial 50 bold'),bg='white')
        self.heading.place(x=0,y=0)

        self.date_l=Label(self.right,text="Date: "+str(date),font=('arial 16 bold'),bg='lightblue',fg='black')
        self.date_l.place(x=0,y=0)

        #table invoice
        self.tproduct=Label(self.right,text="Products",font=('arial 18 bold'),bg='lightblue',fg='black')
        self.tproduct.place(x=0,y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('arial 18 bold'), bg='lightblue', fg='black')
        self.tquantity.place(x=300, y=60)

        self.tamount = Label(self.right, text="Amount", font=('arial 18 bold'), bg='lightblue', fg='black')
        self.tamount.place(x=500, y=60)

        #enter stuff
        self.enterid=Label(self.left,text="Enter Product's ID",font=('arial 18 bold'),bg='white')
        self.enterid.place(x=0,y=80)


        self.enteride=Entry(self.left,width=25,font=('arial 18 bold'),bg='lightblue')
        self.enteride.place(x=190,y=80)
        self.enteride.focus()

        #button
        self.search_btn=Button(self.left,text="Search",width=22,height=2,bg='green',command=self.ajax)
        self.search_btn.place(x=350,y=120)
        #fill it later by the fuction ajax

        self.productname=Label(self.left,text="",font=('arial 27 bold'),bg='white',fg='steelblue')
        self.productname.place(x=0,y=250)

        self.pprice = Label(self.left, text="", font=('arial 27 bold'), bg='white', fg='steelblue')
        self.pprice.place(x=0, y=290)

        #total label
        self.total_l=Label(self.right,text="",font=('arial 40 bold'),bg='lightblue',fg='white')
        self.total_l.place(x=0,y=600)
    def ajax(self,*args,**kwargs):
        self.get_id=self.enteride.get()
        #get the product info with that id and fill i the labels above
        query="SELECT * FROM inventory WHERE id=?"
        result=c.execute(query,(self.get_id,))
        for self.r in result:
            self.get_id=self.r[0]
            self.get_name=self.r[1]
            self.get_price=self.r[4]
            self.get_stock=self.r[2]
        self.productname.configure(text="Product's Name: " +str(self.get_name))
        self.pprice.configure(text="Price:RS. "+str(self.get_price))


        #create the quantity and the discount label
        self.quantity_l=Label(self.left,text="Enter Quantity",font=('arial 18 bold'),bg='white')
        self.quantity_l.place(x=0,y=370)

        self.quantity_e=Entry(self.left,width=25,font=('arial 18 bold'),bg='lightblue')
        self.quantity_e.place(x=190,y=370)
        self.quantity_e.focus()

        #discount
        self.discount_l = Label(self.left, text="Enter Discount", font=('arial 18 bold'), bg='white')
        self.discount_l.place(x=0, y=410)


        self.discount_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightblue')
        self.discount_e.place(x=190, y=410)
        self.discount_e.insert(END,0)


        #add to cart button
        self.add_to_cart_btn = Button(self.left, text="Add to Cart", width=22, height=2, bg='orange', fg='green', command=self.add_to_cart)
        self.add_to_cart_btn.place(x=350, y=450)

        #genrate bill and change
        self.change_l=Label(self.left,text="Given Amount",font=('arial 18 bold'),bg='white')
        self.change_l.place(x=0,y=550)

        self.change_e=Entry(self.left,width=25,font=('arial 18 bold'),bg='lightblue')
        self.change_e.place(x=190,y=550)

        self.change_btn= Button(self.left, text="Calculate Change", width=22, height=2, bg='orange',command=self.change_func)
        self.change_btn.place(x=350, y=590)

        #geneerate bill button
        self.bill_btn = Button(self.left, text="Generate Bill", width=100, height=2, bg='red',fg='green',command=self.generate_bill)
        self.bill_btn.place(x=0, y=640)

    def add_to_cart(self,*args,**kwargs):
        self.quantity_value=int(self.quantity_e.get())
        if  self .quantity_value >int(self.get_stock):
            tkinter.messagebox.showinfo("","opps! product is out of stock.")
        else:
            #calculate the price first
            self.final_price=(float(self.quantity_value) * float(self.get_price))-(float(self.discount_e.get()))
            products_list.append(self.get_name)
            product_price.append(self.final_price)
            product_quantity.append(self.quantity_value)
            product_id.append(self.get_id)

            self.x_index=0
            self.y_index=100
            self.counter=0
            for self.p in products_list:
                self.tempname=Label(self.right,text=str(products_list[self.counter]),font=('arial 18 bold'),bg='lightblue',fg='green')
                self.tempname.place(x=0,y=self.y_index)
                self.tempqt = Label(self.right, text=str(product_quantity[self.counter]), font=('arial 18 bold'), bg='lightblue', fg='green')
                self.tempqt.place(x=300, y=self.y_index)
                self.tempprice = Label(self.right, text=str(product_price[self.counter]), font=('arial 18 bold'), bg='lightblue', fg='green')
                self.tempprice.place(x=500, y=self.y_index)

                self.y_index+=40
                self.counter+=1


                #total configure
                self.total_l.configure(text="Total : Rs. "+str(sum(product_price)))
                #delete
                self.quantity_l.place_forget()
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.add_to_cart_btn.destroy()
                #autofocus to the enter id
                self.enteride.focus()
                self.enteride.delete(0,END)

    def change_func(self,*args,**kwargs):
        self.amount_given=float(self.change_e.get())
        self.our_total=float(sum(product_price))

        self.to_give=self.amount_given-self.our_total

        #label change
        self.c_amount=Label(self.left,text="Change: Rs. "+str(self.to_give),font=('arial 18 bold'),fg='green',bg='white')
        self.c_amount.place(x=0 ,y=600)

    def generate_bill(self,*args,**kwargs):
        self.x=0
        initial="SELECT * FROM inventory WHERE id=?"
        result=c.execute(initial,(product_id[self.x],))
        for r in result:
            self.old_stock=r[2]
        for i in products_list:
            for r in result:
                self.old_stock = r[2]
            self.new_stock=int(self.old_stock) - int(product_quantity[self.x])
            #updating the stock
            sql = "UPDATE inventory SET stock=? WHERE id=?"
            c.execute(sql,(self.new_stock,product_id[self.x]))
            conn.commit()

            #insert into transcation
            sql2="INSERT INTO transactions (product_name,quantity,amount,date) VALUES(?,?,?,?)"
            c.execute(sql2,(products_list[self.x],product_quantity[self.x],product_price[self.x],date))
            conn.commit()
            print("Decreased")
            self.x+=1
        tkinter.messagebox.showinfo("","Bill generated successfully")

root=Tk()
b=Application(root)
root.geometry("1366x768+0+0")
root.mainloop()
