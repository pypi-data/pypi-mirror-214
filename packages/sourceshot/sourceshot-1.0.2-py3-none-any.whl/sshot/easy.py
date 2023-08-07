"""
Easy functions for images
"""
from PIL import Image,ImageTk
import numpy as np
from platform import system
import os
from uuid import uuid4
def require_tk():
    return __import__('tkinter')
def save_svg(path,img):
    import matplotlib.pyplot as plt
    plt.imsave(path,img)
def read_svg(path):
    import cairosvg as cs
    def _tmp():
        if system()=='Windows':
            return os.environ['TMP']
        else:
            return '/tmp'
    file=os.path.join(_tmp(),str(uuid4())+'.png')
    cs.svg2png(file_obj=open(path,'rb'),write_to=file)
    return image_open(file)
def image_open(path):
    if path.endswith('.svg'):
        return read_svg(path)
    return np.array(Image.open(path))
def image_save(path,img):
    if path.endswith('.svg'):
        save_svg(path,img)
    else:
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
