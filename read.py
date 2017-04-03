from PIL import ImageGrab
from functools import reduce

image=ImageGrab.grab()

# x0=int(input("UpperLeft.X:"))
# y0=int(input("UpperLeft.Y:"))
# x1=int(input("BottomRight.X:"))
# y1=int(input("BottomRight.Y:"))
x0=200
y0=400

res=128

Content=None
Index=None
hashf=None


def is_border(c):
    return c[0]>240 and c[1]<15 and c[2]>240

while not is_border(image.getpixel((x0,y0))):
    x0-=1
x0+=1
while not is_border(image.getpixel((x0,y0))):
    y0-=1
y0+=1

x1=x0
y1=y0
while not is_border(image.getpixel((x1,y1))):
    x1+=1
x1-=1
while not is_border(image.getpixel((x1,y1))):
    y1+=1
x1+=1

def GetBit(x,y):
    return image.getpixel((x0+(x1-x0)/res*(x+0.5),y0+(y1-y0)/(res+1)*(y+0.5)))

def GetAll():
    data=[]
    for y in range(res+1):
        data.append([])
        for x in range(res):
            c=GetBit(x,y)
            data[y].append(1 if c[0]<128 else 0)
    return data

def Process(data):
    global Content
    global Index
    global hashf
    start=sum([data[res][i]*(1<<i) for i in range(32)])
    total=sum([data[res][i+32]*(1<<i) for i in range(32)])
    hashf=sum([data[res][i+64]*(1<<i) for i in range(32)])
    hashb=sum([data[res][i+96]*(1<<i) for i in range(32)])
    if Content is None:
        Content=bytearray(b'\x00'*total)
        Index=[False]*(total//2048 if total%2048==0 else total//2048+1)
    for i in range(res):
        for j in range(res//8):
            pos=start+i*res//8+j
            if pos<total:
                Content[pos]=sum([data[i][j*8+k]*(1<<k) for k in range(8)])
    return start//2048,hashb

def calc_hash(d):
    return reduce(lambda a,b:((a<<5)%4294967296-a+b)%4294967296,d)

c=0
while True:
    image=ImageGrab.grab()
    pos,hashb=Process(GetAll())
    if hashb==calc_hash(Content[pos*2048:(pos+1)*2048]):
        if not Index[pos]:
            Index[pos]=True
            c+=1
            print(c,"/",len(Index))
        if not False in Index:
            if hashf==calc_hash(Content):
                break
    else:
        print("Hash error at",pos)

with open("file","wb") as f:
    f.write(Content)

print("Finished")