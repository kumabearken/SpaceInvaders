from tkinter import *

class takeInput(object):

    def __init__(self,requestMessage):
        self.root = Tk()
        self.root.geometry('300x100')
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.pack()
        self.acceptInput(requestMessage)

    def acceptInput(self,requestMessage):
        r = self.frame
        k = Label(r,text=requestMessage)
        k.pack(side='left')
        self.e = Entry(r,text='Name')
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='okay',command=self.gettext)
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.mainloop()