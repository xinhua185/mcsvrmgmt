import subprocess
import tkinter
import tkinter.messagebox
import PIL.Image
import PIL.ImageTk
import easygui
import tkinter.ttk
import json
import os
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
        "lastselect":{
            "javapath":"",
            "serverpath":"",
            "workdir":"",
            "name":"",
            "nogui":True
        }
    }
def envset():
    def addjre():
        jre=easygui.fileopenbox("选择Java路径","打开","java.exe")
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
def editserver(serverconfig=None):
    editserver_win=tkinter.Toplevel()
    #服务端默认配置
    if(serverconfig==None):
        serverconfig={
            "javapath":"",
            "serverpath":"",
            "workdir":"",
            "name":"",
            "nogui":1
        }
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
        if(serverconfig in config["server"]):
            tkinter.messagebox.showerror("错误","不要重复添加服务端配置")
            return
        global index
        config["server"].append(serverconfig)
        editserver_win.destroy()
        serverbtnlist.append(tkinter.ttk.Radiobutton(serverbtnmgmt,text=i["name"],variable=servervar,value=i,command=select))
        serverbtnmgmt.add(serverbtnlist[index])
        index+=1
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
    if(bool(targetserver["nogui"])==True):
        subprocess.Popen('"'+targetserver["javapath"]+'" -jar "'+targetserver["serverpath"]+'" --nogui',shell=True,cwd=targetserver["workdir"])
    else:
        subprocess.Popen('"'+targetserver["javapath"]+'" -jar "'+targetserver["serverpath"]+'"',shell=True,cwd=targetserver["workdir"])
def delserver():
    global targetserver
    serverbtnmgmt.forget(serverbtnlist[config["server"].index(targetserver)])
    config["server"].remove(targetserver)
    targetserver=None
def select():
    global targetserver
    server=servervar.get()
    targetserver=eval(server)
launchbtn=tkinter.ttk.Button(win,text="启动",command=launch)
launchbtn.pack()
delbtn=tkinter.ttk.Button(win,text="删除此配置",command=delserver)
delbtn.pack()
index=0
servervar=tkinter.StringVar()
for i in config["server"]:
    serverbtnlist.append(tkinter.ttk.Radiobutton(serverbtnmgmt,text=i["name"],variable=servervar,value=i,command=select))
    serverbtnmgmt.add(serverbtnlist[index])
    index+=1
win.resizable(0,0)
win.mainloop()
json.dump(config,open("config.json","w"))