from PIL import Image,ImageFont
import numpy as np
import cv2
from .imageproc import *
from pygments.lexers import *
from pygments import *
from .config import *
from .easy import *
class Background():
    """
    Class for background of code screenshot.
    """
    def __init__(self,obj):
        if isinstance(obj,tuple): # Background is a color.
            if isinstance(obj[0],tuple):
                self.type=0
                self.lineno_bg=obj[0]
                self.code_bg=obj[1]
            else:
                self.lineno_bg=obj
                self.code_bg=obj
                self.type=0
        else: # Background is an image.
            self.type=1
            self.bg=obj
    def color(self,code,lineno):
        if self.type:
            whole=image_merge_row(lineno,code)
            bg=cv2.resize(self.bg,(whole.shape[1],whole.shape[0]),interpolation=cv2.INTER_LINEAR)
            for i in range(whole.shape[0]):
                for j in range(whole.shape[1]):
                    if whole[i][j][3]==0:
                        whole[i][j][3]=255
                        whole[i][j][:3]=bg[i][j][:3]
            return np.array(Image.fromarray(whole).convert('RGB'))
        else:
            for i in range(code.shape[0]):
                for j in range(code.shape[1]):
                    if code[i][j][3]==0:
                        code[i][j][3]=255
                        code[i][j][:3]=np.array(self.code_bg,dtype=np.uint8)
            for i in range(lineno.shape[0]):
                for j in range(lineno.shape[1]):
                    if lineno[i][j][3]==0:
                        lineno[i][j][3]=255
                        lineno[i][j][:3]=np.array(self.lineno_bg,dtype=np.uint8)
            return np.array(Image.fromarray(image_merge_row(lineno,code)).convert('RGB'))
def fromstr(string):
    def hex2rgb(x):
        return (int(x[:2],16),int(x[2:4],16),int(x[4:6],16))
    if '.' in string:
        return Background(image_open(string))
    elif len(string)==6:
        return Background(hex2rgb(string))
    else:
        return Background((hex2rgb(string[:6]),hex2rgb(string[6:])))
