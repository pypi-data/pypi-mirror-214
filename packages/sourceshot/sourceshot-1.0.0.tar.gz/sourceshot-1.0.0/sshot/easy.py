"""
Easy functions for images
"""
from PIL import Image,ImageTk
import numpy as np
def require_tk():
    return __import__('tkinter')
def image_open(path):
    return np.array(Image.open(path))
def image_save(path,img):
    Image.fromarray(img).save(path)
def image_show(img,title=''):
    tk=require_tk()
    image_pil=Image.fromarray(img)
    wn=tk.Tk()
    wn.title(title)
    image_tk = ImageTk.PhotoImage(image_pil)
    wn.geometry('{}x{}'.format(img.shape[1],img.shape[0]))
    l=tk.Label(wn,text='',image=image_tk)
    l.place(x=0,y=0,width=img.shape[1],height=img.shape[0])
    wn.mainloop()
