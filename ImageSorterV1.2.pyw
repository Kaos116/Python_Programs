import exifread
import os
import threading
import tkinter as tk
from tkinter import filedialog
from shutil import copyfile
import tkinter.font as tkFont
from tkinter import messagebox
import time
import winsound

def overwrite():
    var14.set(False)
    var15.set(False)
def skip():
    var14.set(False)
    var13.set(False)
def rename():
    var13.set(False)
    var15.set(False)
def go_toppath():
    t3.delete('1.0', tk.END)
    t3.insert(1.0, '\n\nCalculating the number of files to sort.')
    return
def set_toppath():
    global top_dir
    global total_images
    global file_path
    top_dir = ''
    old_time = time.time()

    file_path = filedialog.askdirectory()
    top_dir = file_path.replace('/', "\\"+"\\")
    t1.delete('1.0', tk.END)
    t1.insert(1.0, file_path)
    t3.delete('1.0', tk.END)
    t3.insert(1.0, '\n\nCalculating the number of files to sort.')
    root.update_idletasks()
    total_images = 0
    for drp, dirs, files in os.walk(top_dir):
        total_images += len(files)
        if time.time() >= old_time +.5:
            waiting_wheel()
            root.update_idletasks()
            old_time = time.time()
    t3.insert(tk.END, '\n\n' + str(total_images)+' files to sort \n')
def waiting_wheel():
    global tick
    t3.delete('1.0', tk.END)
    if tick == 1:
        t3.insert(1.0, '\n\nCalculating the number of files to sort -')
    if tick == 2:
        t3.insert(1.0, '\n\nCalculating the number of files to sort \\')
    if tick == 3:
        t3.insert(1.0, '\n\nCalculating the number of files to sort |')
    if tick == 4:
        t3.insert(1.0, '\n\nCalculating the number of files to sort /')
        tick = 0
    tick +=1
    root.update_idletasks()
def set_sortpath():
    global sort_dir
    sort_dir = ''
    file_path = filedialog.askdirectory()
    sort_dir = file_path.replace('/', "\\"+"\\")
    t2.delete('1.0', tk.END)
    t2.insert(1.0, file_path)
def begin_sort():
    global top_dir
    global sort_dir
    global dirpath
    global fname
    global total_images
    global file_list
    tag = 'EXIF DateTimeOriginal'

    for dirpath, dirnames, filenames in os.walk(top_dir):

        for fname in filenames:
            for file_ext in file_list:
                if file_ext in fname:
                    f = open(dirpath+'\\'+fname, 'rb')
                    tags = exifread.process_file(f, details=False)
                    f.close()
                    try:
                        pic_date = str(tags[tag])
                        if len(pic_date) >= 4:
                            pic_date = pic_date.split(':')
                            pic_year = (pic_date[0])
                            if int(pic_year) <= 1966 : pic_year = 'Unknown'
                            pic_month = (pic_date[1])
                            if int(pic_month) < 1 : pic_month = 'Unknown'
                            pic_day = (pic_date[2])
                            pic_day = pic_day[:2]
                            if int(pic_day) < 1 : pic_day = 'Unknown'
                            dest_dir = sort_dir+'\\'+pic_year+'\\'+pic_month+'\\'+pic_day
                        else:
                            dest_dir = sort_dir+'\\Unknown'

                    except:
                        dest_dir = sort_dir + '\\Unknown'
                    try:

                        if (os.path.isdir(dest_dir)):
                            if var15.get() == 1:
                                if os.path.isfile(dest_dir+'\\'+fname) == False:
                                    copyfile(dirpath+'\\'+fname, dest_dir+'\\'+fname)
                            if var13.get() == 1:
                                copyfile(dirpath+'\\'+fname, dest_dir+'\\'+fname)
                            if var14.get() == 1:
                                if os.path.isfile(dest_dir+'\\'+fname) == False:
                                    copyfile(dirpath+'\\'+fname, dest_dir+'\\'+fname)
                                else:
                                    fn, fn2 = fname.split('.')
                                    fname2 = fn+"-DUP."+fn2
                                    copyfile(dirpath+'\\'+fname, dest_dir+'\\'+fname2)
                        else:
                            os.makedirs(dest_dir, exist_ok=True )
                            copyfile(dirpath + '\\' + fname, dest_dir + '\\' + fname)
                        if var16.get() == 1:
                            os.remove(dirpath + '\\' + fname)

                    except:
                        pass
                    t3.insert(1.0, str(total_images)+' - ' + fname + ' >>> ' + dest_dir + '\n')
                    total_images -= 1

                root.update_idletasks()

            if stop_event.is_set():
                break
    if total_images>=1:
        t3.insert(1.0, str(total_images) + ' files not images or file type not selected.\n\n')
    t3.insert(1.0, '\n--- SORT COMPLETE ---\n\n')
    winsound.Beep(1000,200)
def start_sort():
    global sort_dir
    global top_dir
    fileTypeList()
    if sort_dir == '' or top_dir == "":
        messagebox.showerror('Blank Field','Directory fields cannot be blank')

    sort_thread.start()
def all_select():
    if var6.get() == 1:
        var1.set(True)
        var2.set(True)
        var3.set(True)
        var4.set(True)
        var5.set(True)
        var7.set(True)
        var8.set(True)
        var9.set(True)
        var10.set(True)
        var11.set(True)
        var12.set(True)

    if var6.get() == 0:
        var1.set(False)
        var2.set(False)
        var3.set(False)
        var4.set(False)
        var5.set(False)
        var7.set(False)
        var8.set(False)
        var9.set(False)
        var10.set(False)
        var11.set(False)
        var12.set(False)
def fileTypeList():
    global file_list
    file_list = []
    if var1.get()==1:
        file_list.append('.JPG')
        file_list.append('.jpg')
    if var2.get()==1:
        file_list.append('.gif')
        file_list.append('.GIF')
    if var3.get()==1:
        file_list.append('.bmp')
        file_list.append('.BMP')
    if var4.get()==1:
        file_list.append('.png')
        file_list.append('.PNG')
    if var5.get()==1:
        file_list.append('.tif')
        file_list.append('.TIF')
    if var7.get()==1:
        file_list.append('.cr2')
        file_list.append('.CR2')
    if var8.get()==1:
        file_list.append('.nef')
        file_list.append('.NEF')
    if var9.get()==1:
        file_list.append('.pef')
        file_list.append('.PEF')
    if var10.get()==1:
        file_list.append('.rw2')
        file_list.append('.RW2')
    if var11.get()==1:
        file_list.append('.dng')
        file_list.append('.DNG')
    if var12.get()==1:
        file_list.append('.raf')
        file_list.append('.RAF')
    file_list.append('.ORF')
def del_orig():
    msg_box = messagebox.askyesno('Delete Warning', '     This should only be used if you\n'\
            '     do not have enough disk space\n'\
            '     to handle the sorted directory\n'\
            '     It is best to sort without deletion,\n'\
            '     confirm all your images have been\n'\
            '     sorted, then delete the source image\n\n'\
            'Do you wish to continue with your selection?', default='no')
    if msg_box == False:
        var16.set(False)
inst_text='Image Sorter - will sort by the meta data date and time image was taken.\n\n'\
          '1. Choose the top folder you wish to sort down through.\n' \
          '    It will sort all files in sub folders.\n'\
          '    You will have to wait until it counts the files it will be sorting.\n\n'\
          '2. Choose the destination folder for your sorted images,\n\n'\
          '3. Select which file types to sort or ALL,\n\n'\
          '4. Choose what to do if a duplicate is encounter,\n\n'\
          '5. Choose if you wish for the original file to be deleted,\n\n'\
          "6. Click 'Start Sort', sit back, relax and wait.\n\n"


bgColor = '#c2c6cc'
sort_dir = ''
top_dir = ''
file_list = []
tick = 1
root = tk.Tk()
root.title('Image Sorter')
root.geometry('1260x410')
root.configure(bg=bgColor)
root.resizable(False, False)

sort_thread = threading.Thread(target=begin_sort)
sort_thread.daemon = True
stop_event = threading.Event()
stop = threading.Event()

fontStyle1 = tkFont.Font(family="Courier New bold", size=16)
fontStyle2 = tkFont.Font(family="Courier New", size=12)
fontStyle3 = tkFont.Font(family="Courier New bold", size=11)
fontStyle4 = tkFont.Font(family="Courier New", size=8)

var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
var5 = tk.IntVar()
var6 = tk.IntVar()
var7 = tk.IntVar()
var8 = tk.IntVar()
var9 = tk.IntVar()
var10 = tk.IntVar()
var11 = tk.IntVar()
var12 = tk.IntVar()
var13 = tk.IntVar()
var14 = tk.IntVar()
var15 = tk.IntVar()
var16 = tk.IntVar()


w1 = tk.LabelFrame(root, text="Top Folder to Sort", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w1.place(width=600, height=90, x=20, y=20)
t1 = tk.Text(w1, height=1, width=42, font=fontStyle2)
t1.place(x=10, y=14)
b1 = tk.Button(w1, text='Choose Folder', font=fontStyle3, command=set_toppath)
b1.place(x=450, y=10)

w2 = tk.LabelFrame(root, text="Destination Folder", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w2.place(width=600, height=90, x=20, y=120)
t2 = tk.Text(w2, height=1, width=42, font=fontStyle2)
t2.place(x=10, y=14)
b2 = tk.Button(w2, text='Choose Folder', font=fontStyle3, command=set_sortpath)
b2.place(x=450, y=10)

w3 = tk.LabelFrame(root, text="Status", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w3.place(width=600, height=290, x=640, y=20)
t3 = tk.Text(w3, height=17, width=83, font=fontStyle4, bg=bgColor, borderwidth=0, wrap="none")
t3.place(x=5, y=5)

t3.insert(1.0, inst_text)

w4 = tk.LabelFrame(root, text="File Types", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w4.place(width=600, height=90, x=20, y=220)
R1 = tk.Checkbutton(w4, text=".jpg", font=fontStyle2, bg=bgColor, variable=var1)
R1.place(x=5, y=2)
R2 = tk.Checkbutton(w4, text=".gif", font=fontStyle2, bg=bgColor, variable=var2)
R2.place(x=105, y=2)
R3 = tk.Checkbutton(w4, text=".bmp", font=fontStyle2, bg=bgColor, variable=var3)
R3.place(x=205, y=2)
R4 = tk.Checkbutton(w4, text=".png", font=fontStyle2, bg=bgColor, variable=var4)
R4.place(x=305, y=2)
R5 = tk.Checkbutton(w4, text=".tiff", font=fontStyle2, bg=bgColor, variable=var5)
R5.place(x=405, y=2)
R6 = tk.Checkbutton(w4, text="ALL", font=fontStyle2, bg=bgColor, variable=var6, command=all_select)
R6.place(x=505, y=2)
R7 = tk.Checkbutton(w4, text=".cr2", font=fontStyle2, bg=bgColor, variable=var7)
R7.place(x=5, y=30)
R8 = tk.Checkbutton(w4, text=".nef", font=fontStyle2, bg=bgColor, variable=var8)
R8.place(x=105, y=30)
R9 = tk.Checkbutton(w4, text=".pef", font=fontStyle2, bg=bgColor, variable=var9)
R9.place(x=205, y=30)
R10 = tk.Checkbutton(w4, text=".rw2", font=fontStyle2, bg=bgColor, variable=var10)
R10.place(x=305, y=30)
R11 = tk.Checkbutton(w4, text=".dng", font=fontStyle2, bg=bgColor, variable=var11)
R11.place(x=405, y=30)
R12 = tk.Checkbutton(w4, text=".raf", font=fontStyle2, bg=bgColor, variable=var12)
R12.place(x=505, y=30)

w5 = tk.LabelFrame(root, text="Duplicate Files", bd=4, relief="groove", font=fontStyle1, bg=bgColor)
w5.place(width=600, height=70, x=20, y=320)
R13 = tk.Checkbutton(w5, text="Overwrite", font=fontStyle2, bg=bgColor, variable=var13, command=overwrite)
R13.place(x=5, y=2)
R14 = tk.Checkbutton(w5, text="Rename", font=fontStyle2, bg=bgColor, variable=var14, command=rename)
R14.place(x=155, y=2)
R15 = tk.Checkbutton(w5, text="Skip", font=fontStyle2, bg=bgColor, variable=var15, command=skip)
R15.place(x=280, y=2)
R16 = tk.Checkbutton(w5, text="Delete Original", font=fontStyle2, bg=bgColor, variable=var16, command=del_orig)
R16.place(x=380, y=2)

b3 = tk.Button(root, text='Start Sort', font=fontStyle1, height=1, width=13, command=start_sort)
b3.place(x=747, y=340)
b5 = tk.Button(root, text='Exit', font=fontStyle1, height=1, width=13, command=root.destroy)
b5.place(x=953, y=340)


root.mainloop()