from tkinter import *
from PIL import Image,ImageTk,ImageDraw  # pip install pillow
from datetime import *
import time
from math import *
from tkinter import messagebox
import pymysql                           # pip install pymysql
class Login_window:
    def __init__(self,root):
        self.root=root
        self.root.title("LOGIN Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        #===Background colors=============
        left_lbl=Label(self.root,bg="#08A3D2",bd=0)
        left_lbl.place(x=0,y=0,width=600,relheight=1)

        right_lbl=Label(self.root,bg="#031F3C",bd=0)
        right_lbl.place(x=600,y=0,relwidth=1,relheight=1)        

        #===Frames===========================================

        login_frame=Frame(self.root,bg="white")
        login_frame.place(x=250,y=100,width=800,height=500)

        title=Label(login_frame,text="LOGIN HERE",font=("times new roman",30,"bold"),bg="white",fg="#08A3D2").place(x=250,y=50)

        email=Label(login_frame,text="EMAIL ADDRESS",font=("times new roman",18,"bold"),bg="white",fg="black").place(x=250,y=150)
        self.txt_email=Entry(login_frame,font=("times new roman",15),bg="lightgray")
        self.txt_email.place(x=250,y=180,width=350,height=35)

        password=Label(login_frame,text="PASSWORD",font=("times new roman",18,"bold"),bg="white",fg="black").place(x=250,y=250)
        self.txt_password=Entry(login_frame,font=("times new roman",15),bg="lightgray")
        self.txt_password.place(x=250,y=280,width=350,height=35)


        btn_reg=Button(login_frame,text="Register new Account",command=self.register_window,font=("times new roman",14),bg="white",bd=0,fg="#B00857",cursor="hand2").place(x=250,y=320)

        btn_login=Button(login_frame,text="Login",command=self.login,font=("times new roman",20,"bold"),bg="white",fg="black",cursor="hand2").place(x=250,y=380,width=180,height=40)



        #===Clock================
        self.lbl=Label(self.root,bg="black",bd=0)
        self.lbl.place(x=90,y=120,width=350,height=450)
        #self.clock_image()
        self.working()

    def register_window(self):
        self.root.destroy()
        import register

    def login(self):
        if self.txt_email.get()=="" or self.txt_password.get()=="":
            messagebox.showerror("Error","All Feilds Are Requried",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="members")
                cur=con.cursor()
                cur.execute("select * from members where email=%s and password=%s",(self.txt_email.get(),self.txt_password.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username and Password",parent=self.root)
                else:
                    messagebox.showinfo("Success","Login Successful",parent=self.root)
                    self.root.destroy()
                    import bicepcurls
                con.close()
                    

            except Exception as es:
                messagebox.showerror("Error",f"Error due to {str(es)}",parent=self.root)




    def clock_image(self,hr,min_,sec_):
        clock=Image.new("RGB",(400,400),(0,0,0))
        draw=ImageDraw.Draw(clock)
        #----FOR CLOCK IMAGE
        bg=Image.open("images/c.jpeg")
        bg=bg.resize((300,300),Image.ANTIALIAS)
        clock.paste(bg,(50,50))
        
        #----HOUR LINE IMAGE
        origin=200,200
        draw.line((origin,200+50*sin(radians(hr)),200-50*cos(radians(hr))),fill="orange",width=4)
        #----MINUTE LINE IMAGE
        draw.line((origin,200+80*sin(radians(min_)),200-80*cos(radians(min_))),fill="blue",width=3)
        #----SECOND LINE IMAGE
        draw.line((origin,200+100*sin(radians(sec_)),200-100*cos(radians(sec_))),fill="green",width=2)
        draw.ellipse((195,195,210,210),fill="white")


        clock.save("clock_new.png")

    def working(self):
        h=datetime.now().time().hour
        m=datetime.now().time().minute
        s=datetime.now().time().second
        #print(h,m,s)
        hr=(h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360
        #print(hr,min_,sec_)
        self.clock_image(hr,min_,sec_)
        self.img=ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200,self.working)




root=Tk()
obj=Login_window(root)
root.mainloop()