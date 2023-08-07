<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### This package takes pictures of source code
Example code: 
```python
from sshot import shot
from PIL import Image
code='''
print('Hello World!')
'''
image=shot(code,lang='python')
Image.fromarray(image).save('code.png')
```
The code above will create something like:
![](https://i.postimg.cc/sxLHWpJ7/code.png)

Use in command line:
```commandline
sshot -i test.py -l python -o code.png
sshot -i test.py -l python -o code.png -b bg.png # Add background image.
sshot -i test.py -l python -o code.png -b 00FF00FF0000 # Red code background color, green line number background color.
sshot -i test.py -l python # Show the image in a tkinter window.
```

It is also supported to set the background image of code, like:
```python
from sshot import shot
from PIL import Image
from sshot.background import Background
import numpy as np
code='''
print('Hello World!')
'''
bg=np.array(Image.open('bg.png'))
image=shot(code,lang='python',background=Background(bg))
Image.fromarray(image).save('code.png')
```
Added SVG support, but other packages are required.