import os
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import ImageTk, Image
#from PIL.ExifTags import TAGS
import piexif

def set_toppath():
    global top_dir
    global total_images
    global file_path
    global files
    global fname
    global image_count

    top_dir = filedialog.askdirectory()
    file_path = top_dir.replace('/', "\\")
    t1.delete('1.0', END)
    t1.insert(1.0, file_path)

    total_images = 0
    for dirt, blank, files in os.walk(file_path):
        total_images += len(files)

    fname = top_dir + "\\" + files[image_count]
    main_loop()

def get_exif(image_count):
    global top_dir
    global files
    global exif_dict
    fname = top_dir + "\\" + files[image_count]
    text = ""
    try:
        image1 = Image.open(fname)
        exif_dict = piexif.load(image1.info['exif'])
        old_meta = exif_dict["0th"][40094]
        for char in old_meta:
            text = text+chr(char)
        text = text.replace('\0', "")
        t2.delete("1.0", END)
        t2.insert(END, text)

    except:
        pass
        #print("no metadata (XPComment) found")

    return [text]

def create_thumb(image_count):
    global top_dir
    global files
    global image1
    fname = top_dir + "\\" + files[image_count]
    image1 = Image.open(fname)
    image1.thumbnail((550, 565))
    image1.save(top_dir+"\\"+"tn.jpg")
    tn_width = image1.width
    tn_height = image1.height
    if tn_width == 550:
        tn_height = (565-tn_height)/2
        tn_width = 10
    if tn_height == 565:
        tn_width = (550-tn_width)/2
        tn_height = 10

    canvas = Canvas(w2, width=565, height=580, bg=bgColor, bd=0, relief=FLAT)
    canvas.place(x=10, y=10)
    img = top_dir+"\\"+"tn.jpg"
    test = ImageTk.PhotoImage(Image.open(img))
    canvas.create_image(tn_width, tn_height, anchor=NW, image=test)
    #print("Image" + fname)
    get_exif(image_count)
    root.mainloop()
    return

def next_image():
    global image_count
    image_count += 1
    meta_text = get_exif(image_count)
    #print(var1.get(), meta_text)
    if var1.get() == 1:
        if meta_text[0] == "":
            t2.delete("1.0", END)
            create_thumb(image_count)
        else:
            next_image()
    if var1.get() == 0:
        create_thumb(image_count)
    return

def back_image():
    global image_count
    image_count -= 1
    if image_count < 0:
        image_count = 0
    t2.delete("1.0", END)
    create_thumb(image_count)
    return

def save_next():
    global md
    global exif_dict
    global image1
    global top_dir
    global files
    global image_count
    fname = top_dir + "\\" + files[image_count]
    md = []
    new_data = t2.get("1.0", "end-1c")
    for char in new_data:
        md.append(ord(char))
        md.append(0)
    md.append(0)
    md.append(0)
    omd = tuple(md)
    exif_dict["0th"][40094] = (omd)
    exif_bytes = piexif.dump(exif_dict)

    image1.save('%s' % fname, "jpeg", exif=exif_bytes)

    image1 = Image.open(fname)
    exif_dict = piexif.load(image1.info['exif'])
    next_image()
    return

def main_loop():
    global image_count
    global total_images

    if image_count < total_images-1:
        create_thumb(image_count)
        get_exif(image_count)
    return
def sn():
    save_next()
def ni():
    next_image()


bgColor = '#c2c6cc'
image_count = 0
text = ""
files = ""
top_dir = ""
file_list = []
md = []
exif_dict = []
root = Tk()
root.title('Metadata updater')
root.geometry('1260x680')
root.configure(bg=bgColor)
root.resizable(False, False)
var1 = IntVar()
fontStyle1 = tkFont.Font(family="Courier New bold", size=16)
fontStyle2 = tkFont.Font(family="Courier New", size=12)
fontStyle3 = tkFont.Font(family="Courier New bold", size=11)


w1 = LabelFrame(root, text="Working Folder", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w1.place(width=600, height=90, x=640, y=20)

w2 = LabelFrame(root, text="Image", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w2.place(width=600, height=640, x=20, y=20)

w3 = LabelFrame(root, text="Metadata", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w3.place(width=600, height=440, x=640, y=130)

t1 = Text(w1, height=1, width=42, font=fontStyle2)
t1.place(x=10, y=14)

t2 = Text(w3, height=14, width=43, font=fontStyle1)
t2.place(x=14, y=14)

b1 = Button(w1, text='Choose Folder', font=fontStyle3, command=set_toppath)
b1.place(x=450, y=10)

b2 = Button(root, text='Save-Next', font=fontStyle1, height=1, width=10, command=save_next)
b2.place(x=642, y=600)

b3 = Button(root, text='Next', font=fontStyle1, height=1, width=10, command=next_image)
b3.place(x=947, y=600)

b4 = Button(root, text='Exit', font=fontStyle1, height=1, width=10, command=root.destroy)
b4.place(x=1099, y=600)

b5 = Button(root, text='Back', font=fontStyle1, height=1, width=10, command=back_image)
b5.place(x=795, y=600)

c1 = Checkbutton(w3,
                 text='Only show photos without metadata.',
                 font=fontStyle1,
                 bg=bgColor,
                 variable=var1,
                 onvalue=1,
                 offvalue=0)
c1.place(x=58, y=365)
root.mainloop()



