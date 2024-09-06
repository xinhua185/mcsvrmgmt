import subprocess,threading
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter
import tkinter.ttk
import easygui,sys
cmdlist=sys.argv
cmdlist.pop(0)
cwd=cmdlist[len(cmdlist)-1]
cmdlist.pop(len(cmdlist)-1)
process = subprocess.Popen(cmdlist,cwd=cwd,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
win=tkinter.Tk()
text=tkinter.scrolledtext.ScrolledText(win)
text.config(state='disabled')
text.pack()
# err=out=None
text.tag_add('stderr','end')
text.tag_add('stdout','end')
def readerr():
    global err
    while process.poll()==None:
        text.tag_config('stderr',foreground='red')
        # txt=process.stderr.readline().decode("utf-8",'ignore')
        txt=process.stderr.readline().decode("utf-8",'ignore')
        if(txt==None):
            return
        text.config(state='normal')
        text.insert('end',txt,'stderr')
        text.config(state='disabled')
def readout():
    while process.poll()==None:
        text.tag_config('stdout',foreground='black')
        # txt=process.stdout.readline().decode("utf-8",'ignore')
        txt=process.stdout.readline().decode("utf-8",'ignore')
        if(txt==None):
            return
        text.config(state='normal')
        text.insert('end',txt,'stdout')
        text.config(state='disabled')
def writein():
    # while True:
        if process.poll()!=None:
            return
        # cmd=easygui.enterbox('输入命令以发送至服务端')
        cmd=cmdvalue.get()
        if(cmd==None):
            # continue
            return
        cmd+='\n'
        process.stdin.write(cmd.encode())
        process.stdin.flush()
def isquit():
    while process.poll()==None:
        pass
    tkinter.messagebox.showinfo("提示","服务器已退出,返回代码为:"+str(process.poll()))
cmdvalue=tkinter.StringVar()
cmdbox=tkinter.ttk.Entry(win,textvariable=cmdvalue)
cmdbox.pack()
sendbtn=tkinter.ttk.Button(win,text="发送",command=writein)
sendbtn.pack()
errthread=threading.Thread(target=readerr)
outthread=threading.Thread(target=readout)
protectthread=threading.Thread(target=isquit)
# inthread=threading.Thread(target=writein)
errthread.daemon=outthread.daemon=protectthread.daemon=True
# inthread.daemon=True
errthread.start()
outthread.start()
protectthread.start()
# inthread.start()
# process.wait()
win.mainloop()
#关闭服务端
if(process.poll()==None):
    process.stdin.write("stop\n".encode())
    process.stdin.flush()