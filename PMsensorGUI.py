from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import time

class PMsensor:
    def __init__(self):

        root = Tk()
        root.title("空气质量检测仪")
        root.resizable(False,False)
#PM2.5传感器命令字        
        self.openpm=bytes.fromhex('33 3E 00 0C A1 00 00 01 00 00 00 00 00 00 01 1F')
        self.closepm=bytes.fromhex('33 3E 00 0C A1 00 00 00 00 00 00 00 00 00 01 1E')
        self.openop=bytes.fromhex('33 3E 00 0C A2 00 00 01 00 00 00 00 00 00 01 20')
        self.closeop=bytes.fromhex('33 3E 00 0C A2 00 00 01 00 00 00 00 00 00 01 1F')
        self.reqpm=bytes.fromhex('33 3E 00 0C A4 00 00 00 00 00 00 00 00 00 01 21')

        self.comstatus="Close"
        self.comvalue=StringVar()
        self.comboxlist=ttk.Combobox(root,textvariable=self.comvalue,state='readonly') 
        self.port_list = list(serial.tools.list_ports.comports())
        if len(self.port_list)<=0:
            self.comstatus="No COM Found"
            self.com1=()
        else:
            self.com1=tuple(self.port_list)
            
        self.comboxlist["values"]=self.com1
        self.comboxlist.bind("<<ComboboxSelected>>",self.comread)
        self.comboxlist.grid(row=1,column=2)

        self.com=""
        ttk.Label(root,text="端口选择：").grid(row=1,column=1,sticky = E)
        ttk.Label(root,text="传感器开关：").grid(row=2,column=1,sticky=E)
        ttk.Label(root,text="定时输出开关：").grid(row=3,column=1,sticky=E)
        ttk.Label(root,text="PM1.0:").grid(row=4,column=1,sticky=E)
        ttk.Label(root,text="PM2.5:").grid(row=5,column=1,sticky=E)
        ttk.Label(root,text="PM10:").grid(row=6,column=1,sticky=E)

        ttk.Label(root,text="ug/m3").grid(row=4,column=3,sticky=W)
        ttk.Label(root,text="ug/m3").grid(row=5,column=3,sticky=W)
        ttk.Label(root,text="ug/m3").grid(row=6,column=3,sticky=W)
        ttk.Label(root,text="By Sirius").grid(row=8,column=3,sticky=E)

        self.pm10=StringVar()
        ttk.Label(root,textvariable=self.pm10).grid(row=4,column=2)

        self.pm25=StringVar()
        ttk.Label(root,textvariable=self.pm25).grid(row=5,column=2)

        self.pm100=StringVar()
        ttk.Label(root,textvariable=self.pm100).grid(row=6,column=2)

        self.stlable=Label(root,text=self.comstatus,fg="red")
        self.stlable.grid(row=8,column=1,sticky=W)

        self.v1=IntVar()
        ssop=Radiobutton(text="开",variable=self.v1,value = 1,command=self.sensorswich).grid(row=2,column=2)
        sscl=Radiobutton(text="关",variable=self.v1,value = 2,command=self.sensorswich).grid(row=2,column=3)

        self.v2=IntVar()
        pop=Radiobutton(text="开",variable=self.v2,value = 1,command=self.sensoroutput).grid(row=3,column=2)
        pcl=Radiobutton(text="关",variable=self.v2,value = 2,command=self.sensoroutput).grid(row=3,column=3)

        gdatabt=Button(text="传感器读取",command=self.sensorread).grid(row=7,column=2)
        exbt=Button(text="退出",command=root.quit).grid(row=7,column=3)

        root.iconbitmap('ico.ico')

        root.mainloop()

    #传感器开关
    def sensorswich(self):
        if self.com=="":
            self.stlable["fg"]="red"
            self.stlable["text"]="请先选择端口" 
            messagebox.showerror("Error","请先选择端口")
        else:          
            com = serial.Serial(self.com)
            if self.v1.get()==1:
                com.write(self.openpm)
                com.close()
            else:
                com.write(self.closepm)
                com.close()

    #传感器定时输出控制
    def sensoroutput(self):
        if self.com=="":
            self.stlable["fg"]="red"
            self.stlable["text"]="请先选择端口"
            messagebox.showerror("Error","请先选择端口")
        else:
            com = serial.Serial(self.com)
            if self.v2.get()==1:
                com.write(self.openop)
                com.close()
            else:
                com.write(self.closeop)
                com.close()

    #串口读取
    def comread(self,*args):
#        if self.comboxlist.get()
        self.com = list(self.port_list[self.comboxlist.current()])[0]
        self.comstatus = self.com
        self.stlable["fg"]="black"
        self.stlable["text"]=self.com+" Select"

    #传感器读取
    def sensorread(self):
        if self.com=="":
            self.stlable["fg"]="red"
            self.stlable["text"]="请先选择端口"
            messagebox.showerror("Error","请先选择端口")
        else:
            com = serial.Serial(self.com)
            com.write(self.reqpm)
            pmdata = com.read(32)
            com.close()
            self.pm10.set(self.pmread(pmdata,3))
            self.pm25.set(self.pmread(pmdata,5))
            self.pm100.set(self.pmread(pmdata,7))

    # d为原始数据，j为pm1,pm2.5,pm10数据所在起始位置，分别对应3，5，7
    def pmread(self,d,j):
        ph = 0
        pl = 0
        count = 0
        for n in d:
            count += 1
            if (n == 50) and (d[count]== 61) :
                ph=d[count+j]
                pl=d[count+j+1]
                count = 0
                break
        return ph*256+pl

PMsensor()