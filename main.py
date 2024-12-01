#coding=utf-8
import subprocess
import tkinter
import tkinter.messagebox
import PIL.Image
import PIL.ImageTk
import easygui
import tkinter.ttk
import json
import os,sys
import PIL
win=tkinter.Tk()
win.title("服务器管理")
win.geometry('1050x590')
#读取配置文件
try:
    config=json.load(open("config.json",'r'))
#使用默认配置文件
except:
    config={
        "jre":[],
        "server":[],
        "useshell":True
    }
def envset():
    def addjre():
        jre=easygui.fileopenbox("选择Java路径","打开","java.exe")
        if(jre==None):
            tkinter.messagebox.showerror("错误","请选择一个有效的java.exe")
            return
        config["jre"].append(jre)
        btn=tkinter.ttk.Button(envset_win,text="删除"+jre,command=lambda:deljre(jre,btn))
        btn.pack()
    def deljre(jre,btn):
        config["jre"].remove(jre)
        btn.forget()
    envset_win=tkinter.Toplevel(win)
    tkinter.ttk.Button(envset_win,text="添加Java路径",command=addjre).pack()
    for i in config["jre"]:
        btn=tkinter.ttk.Button(envset_win,text="删除"+i,command=lambda:deljre(i,btn))
        btn.pack()
def editserver(editing=False):
    #服务端默认配置
    if(editing==False):
        serverconfig={
            "javapath":"",
            "serverpath":"",
            "workdir":"",
            "name":"",
            "nogui":True
        }
    #使用已选的配置
    else:
        if(targetserver==None):
            tkinter.messagebox.showerror("错误","请选择一个服务端配置文件")
            return
        targetindex=config["server"].index(targetserver)
        serverconfig=targetserver
    editserver_win=tkinter.Toplevel()
    #java路径
    tkinter.ttk.Label(editserver_win,text="Java路径").pack()
    javavar=tkinter.StringVar()
    def selectjava(event):
        serverconfig["javapath"]=javavar.get()
    javacombo=tkinter.ttk.Combobox(editserver_win,textvariable=javavar,values=config['jre'])
    try:
        javacombo.current(config["jre"].index(serverconfig["javapath"]))
    except:
        pass
    javacombo.bind('<<ComboboxSelected>>',selectjava)
    javacombo.pack()
    #server路径
    def selectserver():
        serverconfig["serverpath"]=easygui.fileopenbox("选择一个服务端文件","打开","*.jar")
        if(serverconfig["serverpath"]==None):
            tkinter.messagebox.showerror("错误","请选择一个服务端文件")
            return
        serverconfig["name"]=os.path.basename(serverconfig["serverpath"])
        serverconfig["workdir"]=os.path.dirname(serverconfig["serverpath"])
        serverbtn.config(text="服务器路径:"+serverconfig["serverpath"])
    serverbtn=tkinter.ttk.Button(editserver_win,text="服务器路径:"+serverconfig["serverpath"],command=selectserver)
    serverbtn.pack()
    #--nogui是否启用
    noguivar=tkinter.BooleanVar(value=bool(serverconfig["nogui"]))
    def togglegui():
        serverconfig["nogui"]=noguivar.get()
    noguibtn=tkinter.ttk.Checkbutton(editserver_win,text="禁用服务器UI",variable=noguivar,command=togglegui)
    noguibtn.pack()
    #保存并退出
    def saveandexit():
        editserver_win.destroy()
        if(serverconfig["javapath"]=="" or serverconfig["serverpath"]=="" or serverconfig["workdir"]=="" or serverconfig["name"]==""):
            tkinter.messagebox.showerror("错误","无效配置")
            return
        global index
        #将新配置添加到列表中
        if(editing==False):
            if(serverconfig in config["server"]):
                tkinter.messagebox.showerror("错误","不要重复添加服务端配置")
                return
            config["server"].append(serverconfig)
            serverbtnlist.append(tkinter.ttk.Radiobutton(serverbtnmgmt,text=serverconfig["name"],variable=servervar,value=serverconfig,command=select))
            serverbtnmgmt.add(serverbtnlist[index])
            index+=1
        #改变当前配置
        else:
            config["server"][targetindex]=serverconfig
    tkinter.ttk.Button(editserver_win,text="保存并退出",command=saveandexit).pack()
menu=tkinter.Menu(win)
win.config(menu=menu)
menu.add_command(label="jre环境管理",command=envset)
menu.add_command(label="添加新服务端",command=editserver)
#加载背景图片
bg=PIL.ImageTk.PhotoImage(PIL.Image.open("bg.png"))
tkinter.ttk.Label(win,image=bg).place(x=0,y=0)
#服务端管理
serverbtnmgmt=tkinter.PanedWindow(win,orient=tkinter.VERTICAL)
serverbtnmgmt.pack(side=tkinter.LEFT)
serverbtnlist=[]
targetserver=None
def launch():
    if(targetserver==None):
        tkinter.messagebox.showerror("错误","请选择一个服务端配置文件")
        return
    cmd='"'+targetserver["javapath"]+'" -jar "'+targetserver["serverpath"]+'"'
    # print(cmd)
    if(bool(targetserver["nogui"])==True):
        cmd+=' --nogui'
    if(sys.platform=='win32'):
        cmd='start "'+targetserver["name"]+'" '+cmd
        print(cmd)
        subprocess.Popen(cmd,shell=True,cwd=os.path.dirname(targetserver["serverpath"]),start_new_session=True)
    else:
        subprocess.Popen('python '+os.path.join(os.getcwd(),'terminal.py')+' '+cmd+' "'+targetserver["workdir"]+'"')
def delserver():
    global targetserver
    if(targetserver==None):
        tkinter.messagebox.showerror("错误","请选择一个服务端配置文件")
        return
    serverbtnmgmt.forget(serverbtnlist[config["server"].index(targetserver)])
    config["server"].remove(targetserver)
    targetserver=None
def select():
    global targetserver
    server=servervar.get()
    targetserver=eval(server)
launchbtn=tkinter.ttk.Button(win,text="启动",command=launch)
launchbtn.pack()
delbtn=tkinter.ttk.Button(win,text="删除配置",command=delserver)
delbtn.pack()
editbtn=tkinter.ttk.Button(win,text="编辑配置",command=lambda:editserver(True))
editbtn.pack()
index=0
servervar=tkinter.StringVar()
for i in config["server"]:
    serverbtnlist.append(tkinter.ttk.Radiobutton(serverbtnmgmt,text=i["name"],variable=servervar,value=i,command=select))
    serverbtnmgmt.add(serverbtnlist[index])
    index+=1
win.resizable(0,0)
win.mainloop()
json.dump(config,open("config.json","w"))
