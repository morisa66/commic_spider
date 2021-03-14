from tkinter import *
import utils
from utils import run
import threading
R = Tk()

R.minsize(600, 400)
R.maxsize(600, 400)

L = Label(R,
          text="COMMIC PICTURE SPIDER",
          justify=LEFT,
          compound=CENTER,
          font=("Baskerville", 20),
          fg="DeepPink")
L.pack()

L1 = Label(R,
           text="Tag:",
           font=("Baskerville", 20),
           fg="DeepPink")
L1.place(x=80, y=60)

E1 = Entry(R,
           bd=3,
           font=("Baskerville", 20),
           bg='Cyan',
           fg="DeepPink")
E1.place(x=150, y=60)


def eventhandler(event):
    E1.focus()


# Ctrl+f : choose
E1.bind_all('<Control-f>', eventhandler)

L2 = Label(R,
           text="Itor",
           font=("Baskerville", 20),
           fg="DeepPink")
L2.place(x=80, y=120)

E2 = Entry(R,
           bd=3,
           font=("Baskerville", 20),
           bg='Cyan',
           fg="DeepPink")
E2.place(x=150, y=120)


def eventhandler(event):
    E2.focus()


# Ctrl+g : choose
E2.bind_all('<Control-g>', eventhandler)

# furude_rika
def tmp_f():
    try:
        run(tag=str(E1.get()), itor=int(E2.get()))
    except:
        run(tag="", itor=1)
    utils.END_FALG = False

def start_thread():
    T = threading.Thread(target=tmp_f)
    T.start()

def end_thread():
    utils.END_FALG = True



B = Button(R, text="start", command=start_thread)
B.place(x=220, y=220)
B = Button(R, text="end", command=end_thread)
B.place(x=330, y=220)

R.mainloop()


