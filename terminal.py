import subprocess,threading
import tkinter.scrolledtext
import tkinter
import easygui,sys
cmdlist=sys.argv
cmdlist.pop(0)
process = subprocess.Popen(cmdlist,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
win=tkinter.Tk()
text=tkinter.scrolledtext.ScrolledText(win)
text.config(state='disabled')
text.pack()
# err=out=None
text.tag_add('stderr','end')
text.tag_add('stdout','end')
def readerr():
    global err
    while True:
        if process.poll==None:
            return
        text.tag_config('stderr',foreground='red')
        # txt=process.stderr.readline().decode("utf-8",'ignore')
        txt=process.stderr.readline().decode("utf-8")
        if(txt==None):
            return
        text.config(state='normal')
        text.insert('end',txt,'stderr')
        text.config(state='disabled')
def readout():
    while True:
        if process.poll==None:
            return
        text.tag_config('stdout',foreground='black')
        # txt=process.stdout.readline().decode("utf-8",'ignore')
        txt=process.stdout.readline().decode("utf-8")
        if(txt==None):
            return
        text.config(state='normal')
        text.insert('end',txt,'stdout')
        text.config(state='disabled')
def writein():
    while True:
        if process.poll==None:
            return
        cmd=easygui.enterbox('输入命令以发送至服务端')
        if(cmd==None):
            continue
        cmd+='\n'
        process.stdin.write(cmd.encode())
        process.stdin.flush()
errthread=threading.Thread(target=readerr)
outthread=threading.Thread(target=readout)
inthread=threading.Thread(target=writein)
errthread.daemon=outthread.daemon=inthread.daemon=True
errthread.start()
outthread.start()
inthread.start()
# process.wait()
win.mainloop()
#关闭服务端
process.stdin.write("stop\n".encode())
process.stdin.flush()