#python
import math
import numpy as np
#import time as tm
from tkinter import *
# from tkinter import messagebox as msgbox
from numpy import *
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import colors
from matplotlib import axes
#%matplotlib inline
import urllib
from pyheatmap.heatmap import HeatMap
np.set_printoptions(threshold=nan)

#定义几何参数和物性参数
d_size={'metal':5,'mold':9}
d_thermo={
'c':{'metalc':0.16,'moldc':0.27},
'k':{'metalk':0.1,'moldk':0.0025},
'r':{'metalmold':1500},
'd':{'metald':7.5,'moldd':1.6}
}
d_temp={'liq':1510,'sol':1450}
gridstep=0.2       #网格步长
D=gridstep/2
L=65             #潜热
T0=1570          #金属初始温度
T1=20            #铸型初始温度
time=[0.0]
w4=0             #铸型与绝热层处的W
#等价比热
cequal=d_thermo['c']['metalc']-L*(-1/(d_temp['liq']-d_temp['sol']))

w1 = d_thermo['k']['moldk']  # 模具内部
w2 = d_thermo['k']['metalk']  # 金属内部
w3 = pow(gridstep, 1) / (
            d_thermo['r']['metalmold'] + D / d_thermo['k']['metalk'] + D / d_thermo['k']['moldk'])  # 铸型与金属交界

print(w1)
print(w2)
print(w3)

# 计算时间步长（只需计算金属内部和铸型内部的时间步长，并取最小值，以确定稳定性条件）
timestep1 = d_thermo['d']['moldd'] * d_thermo['c']['moldc'] * pow(gridstep, 2) / (4 * w1)
timestep2 = d_thermo['d']['metald'] * d_thermo['c']['metalc'] * pow(gridstep, 2) / (4 * w2)
if timestep1 > timestep2:
    timestep = timestep2
else:
    timestep = timestep1

print(timestep)

#网格数目
d_len={'metalsize':int(d_size['metal']/gridstep),'moldsize':int(d_size['mold']/gridstep),'thick':int((d_size['mold']-d_size['metal'])/(2*gridstep))}


# 应该建立两个数组记录温度，在计算时，1个数组的数据不发生变化，另一个数组里记录计算出的值
arr = np.zeros((int(d_len['moldsize'] + 2), int(d_len['moldsize'] + 2)), dtype=np.float)
for i in range(d_len['moldsize'] + 2):
    for j in range(d_len['moldsize'] + 2):
        if i > (d_len['thick']) and i < (d_len['thick'] + d_len['metalsize'] + 1) and j > (d_len['thick']) and j < (
                d_len['thick'] + d_len['metalsize'] + 1):
            arr[i][j] = T0
        else:
            arr[i][j] = T1
# 复制arr，表示前一时刻温度
arr1 = arr.copy()

#初始金属与铸型温度分布
plt.figure(figsize=(4,3))
plt.imshow(arr,cmap = cm.get_cmap('hot'))
plt.colorbar()
plt.savefig('hm.png')

#初始温度分布图以及参数显示
root=Tk()
root.title("parameters")
#root.geometry('600x400+20+20')

frmL=Frame(width=400,height=200)
frmC=Frame(width=150,height=120)
frmR=Frame(width=300,height=120)
frmB=Frame(width=450,height=30)

#setting their positions
frmL.grid(row=0,column=0,rowspan=6,padx=1,pady=1)
frmC.grid(row=0,column=1,rowspan=5,columnspan=2,padx=1,pady=10)
frmR.grid(row=0,column=3,rowspan=5,columnspan=4,padx=1,pady=10)
frmB.grid(row=5,column=1,columnspan=6,padx=1,pady=1)

frmL.grid_propagate(0)
frmC.grid_propagate(0)
frmR.grid_propagate(0)
frmB.grid_propagate(0)

#left show img
image=Image.open("hm.png")
photo=ImageTk.PhotoImage(image)
showImage=Label(frmL,image=photo)
showImage.image=photo
showImage.pack()

#center show parameters of the size
Label(frmC,text="metalsize:").grid(row=0,column=1)
e1=StringVar()
metal_en=Entry(frmC,width=10,textvariable=e1)
e1.set(d_size['metal'])
metal_en.grid(row=0,column=2)

Label(frmC,text="moldsize:").grid(row=1,column=1)
e2=StringVar()
mold_en=Entry(frmC,width=10,textvariable=e2)
e2.set(d_size['mold'])
mold_en.grid(row=1,column=2)

Label(frmC,text="gridstep:").grid(row=2,column=1)
e3=StringVar()
grid_en=Entry(frmC,width=10,textvariable=e3)
e3.set(gridstep)
grid_en.grid(row=2,column=2)

Label(frmC,text="T_init_metal:").grid(row=3,column=1)
e4=StringVar()
temp0_en=Entry(frmC,width=10,textvariable=e4)
e4.set(T0)
temp0_en.grid(row=3,column=2)

Label(frmC,text="T_init_mold:").grid(row=4,column=1)
e5=StringVar()
temp1_en=Entry(frmC,width=10,textvariable=e5)
e5.set(T1)
temp1_en.grid(row=4,column=2)

#right show the thermo parameters
Label(frmR,text="metalc:").grid(row=0,column=3)
e11=StringVar()
metalc_en=Entry(frmR,width=10,textvariable=e11)
e11.set(d_thermo['c']['metalc'])
metalc_en.grid(row=0,column=4)

Label(frmR,text="metalk:").grid(row=1,column=3)
e22=StringVar()
metalk_en=Entry(frmR,width=10,textvariable=e22)
e22.set(d_thermo['k']['metalk'])
metalk_en.grid(row=1,column=4)

Label(frmR,text="metald:").grid(row=2,column=3)
e33=StringVar()
metald_en=Entry(frmR,width=10,textvariable=e33)
e33.set(d_thermo['d']['metald'])
metald_en.grid(row=2,column=4)

Label(frmR,text="moldc:").grid(row=0,column=5)
e12=StringVar()
moldc_en=Entry(frmR,width=10,textvariable=e12)
e12.set(d_thermo['c']['moldc'])
moldc_en.grid(row=0,column=6)

Label(frmR,text="moldk:").grid(row=1,column=5)
e23=StringVar()
moldk_en=Entry(frmR,width=10,textvariable=e23)
e23.set(d_thermo['k']['moldk'])
moldk_en.grid(row=1,column=6)

Label(frmR,text="moldd:").grid(row=2,column=5)
e34=StringVar()
moldd_en=Entry(frmR,width=10,textvariable=e34)
e34.set(d_thermo['d']['moldd'])
moldd_en.grid(row=2,column=6)

Label(frmR,text="r:").grid(row=3,column=3)
e45=StringVar()
r_en=Entry(frmR,width=10,textvariable=e45)
e45.set(d_thermo['r']['metalmold'])
r_en.grid(row=3,column=4)

Label(frmR,text="L:").grid(row=4,column=3)
e56=StringVar()
L_en=Entry(frmR,width=10,textvariable=e56)
e56.set(L)
L_en.grid(row=4,column=4)

Label(frmB,text="Please close the window to continue!!!",font=("Arial",14,"bold")).grid(row=6,column=3,columnspan=3)

root.mainloop()               #注意此处关闭窗口后才能够继续后续计算

#改变参数后再次赋值（同样也可以设置能够读取其他参数的变化，在这里只设置了能够改变铸型边长）
d_size['mold']=int(e2.get())
#可在此处加入其它的更改的重新读入
#再次计算网格数目
d_len={'metalsize':int(d_size['metal']/gridstep),'moldsize':int(d_size['mold']/gridstep),'thick':int((d_size['mold']-d_size['metal'])/(2*gridstep))}

#输出网格数
print(d_len['metalsize'])
print(d_len['moldsize'])
print(d_len['thick'])
#重新定义温度数组
arr = np.zeros((int(d_len['moldsize'] + 2), int(d_len['moldsize'] + 2)), dtype=np.float)
for i in range(d_len['moldsize'] + 2):
    for j in range(d_len['moldsize'] + 2):
        if i > (d_len['thick']) and i < (d_len['thick'] + d_len['metalsize'] + 1) and j > (d_len['thick']) and j < (
                d_len['thick'] + d_len['metalsize'] + 1):
            arr[i][j] = T0
        else:
            arr[i][j] = T1
# 复制arr，表示前一时刻温度
arr1 = arr.copy()

# temp不同区域的计算公式
def temp(i, j):
    pmetal = timestep / (d_thermo['d']['metald'] * d_thermo['c']['metalc'] * pow(gridstep, 2))
    pmold = timestep / (d_thermo['d']['moldd'] * d_thermo['c']['moldc'] * pow(gridstep, 2))
    if i != 0 and j != 0 and i != (d_len['moldsize'] + 1) and j != (d_len['moldsize'] + 1):
        left = arr1[i - 1][j]
        right = arr1[i + 1][j]
        up = arr1[i][j + 1]
        down = arr1[i][j - 1]
    # 边界2四角
    if i == 0 or j == 0 or i == (d_len['moldsize'] + 1) or j == (d_len['moldsize'] + 1):
        arr[i][j] = T1
    elif i == 1 and j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == 1 and j == d_len['moldsize']:
        p2 = w4 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize'] and j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize'] and j == d_len['moldsize']:
        p2 = w4 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 边界1
    elif i == 1:
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize']:
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == d_len['moldsize']:
        p2 = w4 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 模具内部1
    elif i < d_len['thick'] or j < d_len['thick'] or i > (d_len['thick'] + d_len['metalsize'] + 1) or j > (
            d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 模具内部2
    elif (i == (d_len['thick']) and j == (d_len['thick'])) \
            or (i == (d_len['thick']) and j == (d_len['thick'] + d_len['metalsize'] + 1)) \
            or (i == (d_len['thick'] + d_len['metalsize'] + 1) and j == (d_len['thick'] + d_len['metalsize'] + 1)) \
            or (i == (d_len['thick'] + d_len['metalsize'] + 1) and j == (d_len['thick'])):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 金属内部
    elif i > (d_len['thick'] + 1) and i < (d_len['thick'] + d_len['metalsize']) and j > (d_len['thick'] + 1) and j < (
            d_len['thick'] + d_len['metalsize']):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    # 金属四角
    elif i == (d_len['thick'] + 1) and j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif i == (d_len['thick'] + 1) and j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']) and j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']) and j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    # mold与metal交界
    elif i == (d_len['thick']):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == (d_len['thick']):
        p2 = w3 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == (d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # the boundary of metal and mold,in metal
    elif i == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]
    elif j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pmetal * p2 + arr1[i][j]


# 采用等价比热法进行潜热处理
def metal(i, j):
    pe = timestep / (d_thermo['d']['metald'] * cequal * pow(gridstep, 2))
    pmold = timestep / (d_thermo['d']['moldd'] * d_thermo['c']['moldc'] * pow(gridstep, 2))
    if i != 0 and j != 0 and i != (d_len['moldsize'] + 1) and j != (d_len['moldsize'] + 1):
        left = arr1[i - 1][j]
        right = arr1[i + 1][j]
        up = arr1[i][j + 1]
        down = arr1[i][j - 1]
    if i == 0 or j == 0 or i == (d_len['moldsize'] + 1) or j == (d_len['moldsize'] + 1):
        arr[i][j] = T1
    # 边界2四角
    elif i == 1 and j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == 1 and j == d_len['moldsize']:
        p2 = w4 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize'] and j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize'] and j == d_len['moldsize']:
        p2 = w4 * (T1 - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (T1 - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 边界1
    elif i == 1:
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w4 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == d_len['moldsize']:
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w4 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == 1:
        p2 = w1 * (up - arr1[i][j]) + w4 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == d_len['moldsize']:
        p2 = w4 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 模具内部1
    elif i < d_len['thick'] or j < d_len['thick'] or i > (d_len['thick'] + d_len['metalsize'] + 1) or j > (
            d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 模具内部2
    elif (i == (d_len['thick']) and j == (d_len['thick'])) \
            or (i == (d_len['thick']) and j == (d_len['thick'] + d_len['metalsize'] + 1)) \
            or (i == (d_len['thick'] + d_len['metalsize'] + 1) and j == (d_len['thick'] + d_len['metalsize'] + 1)) \
            or (i == (d_len['thick'] + d_len['metalsize'] + 1) and j == (d_len['thick'])):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # 金属内部
    elif i > (d_len['thick'] + 1) and i < (d_len['thick'] + d_len['metalsize']) and j > (d_len['thick'] + 1) and j < (
            d_len['thick'] + d_len['metalsize']):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    # 金属四角
    elif i == (d_len['thick'] + 1) and j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif i == (d_len['thick'] + 1) and j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']) and j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']) and j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    # mold与metal交界
    elif i == (d_len['thick']):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == (d_len['thick']):
        p2 = w3 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w1 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    elif j == (d_len['thick'] + d_len['metalsize'] + 1):
        p2 = w1 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w1 * (left - arr1[i][j]) + w1 * (right - arr1[i][j])
        arr[i][j] = pmold * p2 + arr1[i][j]
    # the boundary of metal and mold,in metal
    elif i == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w3 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif j == (d_len['thick'] + 1):
        p2 = w2 * (up - arr1[i][j]) + w3 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif i == (d_len['thick'] + d_len['metalsize']):
        p2 = w2 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w3 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]
    elif j == (d_len['thick'] + d_len['metalsize']):
        p2 = w3 * (up - arr1[i][j]) + w2 * (down - arr1[i][j]) + w2 * (left - arr1[i][j]) + w2 * (right - arr1[i][j])
        arr[i][j] = pe * p2 + arr1[i][j]



#main calculate（中心温度达到固相线前进行循环）
count=0       #用于记录时间
tcenter=[]      #用于记录中心温度
while arr1[int((d_len['moldsize']+1)/2)][int((d_len['moldsize']+1)/2)]>d_temp['sol']:
    for i in range(1,(d_len['moldsize']+1)):
        for j in range(1,(d_len['moldsize']+1)):
            if arr1[i][j]>d_temp['liq'] or arr1[i][j]<d_temp['sol']:    #在液相线之上或者固相线之下，正常的比热
                temp(i,j);
            else:
                metal(i,j);           #在液相线与固相线之间，采用等价比热计算
    count=count+1           #记录运行的步数
    tcenter.append(arr1[int((d_len['moldsize'] + 1) / 2)][int((d_len['moldsize'] + 1) / 2)])
    arr1=arr.copy()        #每运行完一步，将arr的值赋给arr1用作下次计算的初始温度
time[0]=count*timestep
print(time[0])
print(tcenter)           #输出中心温度变化的数组，可以用来绘制冷却曲线
#print(arr)             #此处可以选择输出温度数组

#计算结果的显示
new = Tk()
new.title('output')
#显示温度场
plt.figure(figsize=(4,3))
plt.imshow(arr,cmap = cm.get_cmap('hot'))
plt.colorbar()
plt.savefig('hm1.png')
#将金属部分单独记录到一个数组
arr3 = arr[(d_len['thick'] + 1):(d_len['thick'] + d_len['metalsize'] + 1),
       (d_len['thick'] + 1):(d_len['thick'] + d_len['metalsize'] + 1)]
#显示金属部分的温度分布（主要由于金属与铸型的温差较大单独显示会更好看）
plt.figure(figsize=(4,3))
plt.imshow(arr3,cmap = cm.get_cmap('hot'))
plt.colorbar()
plt.savefig('hm2.png')

frmNL = Frame(width=250, height=100)
frmNC = Frame(width=250, height=100)
frmNR = Frame(width=100, height=50)
frmNL.grid(row=0, column=0, rowspan=2, padx=1, pady=5)
frmNC.grid(row=0, column=1, rowspan=2, padx=1, pady=5)
frmNR.grid(row=0, column=2, rowspan=2, columnspan=2, padx=10, pady=10)

image1 = Image.open("hm1.png")
photo1 = ImageTk.PhotoImage(image1)
showImage1 = Label(frmNL, image=photo1)
showImage1.image = photo1
showImage1.pack()
image2 = Image.open("hm2.png")
photo2 = ImageTk.PhotoImage(image2)
showImage2 = Label(frmNC, image=photo2)
showImage2.image = photo2
showImage2.pack()

Label(frmNR, text="timeused:",font=("Arial",12,"bold")).grid(row=0, column=2)
en1 = StringVar()
t_en1 = Entry(frmNR, width=13, textvariable=en1,state=DISABLED)
en1.set(time[0])
t_en1.grid(row=1, column=2)

new.mainloop()





