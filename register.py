from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("2160x1750")
        self.root.config(bg="white")

        '''# BG Image
        self.bg_image = Image.open("images/bg1.jpg")
        self.bg = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # LEFT Image
        self.left_image = Image.open("images/left image.png")
        self.left = ImageTk.PhotoImage(self.left_image)
        self.left_label = Label(self.root, image=self.left)
        self.left_label.place(x=80, y=30, width=520, height=750)'''
        

        # Register frame
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=600, y=30, width=700, height=750)

        #------------------------------ ROW 1 --------------------------------------------------------------------------------------------------------------------------

        title=Label(frame1,text="REGISTER HERE",font=("times new roman",20,"bold"),bg="white",fg="green").place(x=50,y=30)

        f_name=Label(frame1,text="First Name",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=100)
        self.txt_fname=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_fname.place(x=50,y=130,width=250)

        l_name=Label(frame1,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=100)
        self.txt_lname=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_lname.place(x=370,y=130,width=250)

    #--------------------------------- ROW 2 -----------------------------------------------------------------------------------------------------------------------

        contact=Label(frame1,text="Contact Number",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=170)
        self.txt_contact=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame1,text="E-Mail",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=170)
        self.txt_email=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_email.place(x=370,y=200,width=250)
        
     #---------------------------------- ROW 3 ----------------------------------------------------------------------------------------------------------------------

        password=Label(frame1,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=240)
        self.txt_password=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_password.place(x=50,y=270,width=250)

        cpassword=Label(frame1,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=240)
        self.txt_cpassword=Entry(frame1,font=("times new roman",15),bg="lightgray")
        self.txt_cpassword.place(x=370,y=270,width=250)

    #----------------------------- Terms
        self.var_chk=IntVar()
        chk=Checkbutton(frame1,text="I Agree The Terms And Conditions",bg="white",font=("time new roman",12),variable=self.var_chk,onvalue=1,offvalue=0).place(x=50,y=315)

        btn_register=Button(frame1,text="REGISTER NOW",font=("times new roman",20,"bold"),fg="black",command=self.register_data).place(x=180,y=380)
        btn_login=Button(self.root,text="SIGN IN",command=self.login_window,font=("times new roman",20,"bold"),fg="black").place(x=180,y=380,width=180)
    
    def clear(self):
        self.txt_fname.delete(0,END)
        self.txt_lname.delete(0,END)
        self.txt_contact.delete(0,END)
        self.txt_email.delete(0,END)
        self.txt_password.delete(0,END)
        self.txt_cpassword.delete(0,END)

    def login_window(self):
        self.root.destroy()
        import login

    def register_data(self):
        if self.txt_fname.get()=="" or self.txt_contact.get()=="" or self.txt_email.get()=="" or self.txt_password.get()=="" or self.txt_cpassword.get()=="":
            messagebox.showerror("Error","All Fields Are Requried.",parent=self.root)
        elif self.txt_password.get()!=self.txt_cpassword.get():
            messagebox.showerror("Error", "Passwords Mismatch.",parent=self.root)
        elif self.var_chk.get()==0:
            messagebox.showerror("Error","Please Agree the Terms & Conditions.",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="members")
                cur=con.cursor()
                cur.execute("select * from members where email=%s",self.txt_email.get())
                row=cur.fetchone()
                #print(row)
                if row!=None:
                    messagebox.showerror("Error","User Already Exists, Please Try with Another E-mail.",parent=self.root)
                else:
                    cur.execute("insert into members(f_name,l_name,contact,email,password) values(%s,%s,%s,%s,%s)",
                                    (self.txt_fname.get(),
                                    self.txt_lname.get(),
                                    self.txt_contact.get(),
                                    self.txt_email.get(),
                                    self.txt_password.get()
                                    ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Successfully Registered.",parent=self.root)
                    self.clear()


            except Exception as es:
                messagebox.showerror("Error",f"Error due to: {str(es)}",parent=self.root)



                    

        #print(self.txt_fname.get(),
        #    self.txt_lname.get(),
        #    self.txt_contact.get(),
        #    self.txt_email.get(),
        #    self.txt_password.get(),
        #    self.txt_cpassword.get())

root = Tk()
obj = Register(root)
root.mainloop()
