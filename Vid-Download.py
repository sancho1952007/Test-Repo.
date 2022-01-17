import os
import pyperclip
from tkinter import *
from pytube import YouTube
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *

root=Tk()
root.title("Vid-Download")

def ConvertToMp3():
	if urls.get(1.0, END).replace(' ', '').replace('\n', '')!="":
		sure=askyesno("Sure?", "Are You Sure To Start The Concversion To Mp3?\nThis Might Take Time Depending On The Number Of The Videos...")
		if sure:
			url = urls.get(1.0, END)
			url = url.split('\n')
			for each in url:
				if each.replace(' ', '') != '':
					if each.startswith('https://youtu.be/') or each.startswith('https://www.youtube.com/watch?v='):
						try:
							get = YouTube(each)
							video = get.streams.filter(only_audio=True).first()
							download = video.download(output_path='.')
							base, ext = os.path.splitext(download)
							new_file = base + '.mp3'
							os.rename(download, new_file)
							addLog("[Success] "+get.title+"\nSuccessfully Got Downloaded!")
						except:
							try:
								addLog(f'[Error] Could Not Convert [{each}] Video To Mp3!')
								os.remove(get.title+'.mp4')
							except:
								pass
							pass

					else:
						addLog(f'[Invalid URL] The URL [{each}] You Entered Is Not A Youtube Video URL!')
			showinfo("Done!", 'All Video(s) Have Been Converted\nCheck The Logs For Errors If Any...')
	else:
		showerror("URL(s) Not Supplied", "Cannot Convert To Mp3 Due To No URL(s) Given")

def ConvertToMp4():
	if urls.get(1.0, END).replace(' ', '').replace('\n', '')!="":
		sure=askyesno("Sure?", "Are You Sure To Start The Concversion To Mp3?\nThis Might Take Time Depending On The Number Of The Videos...")
		if sure:
			url = urls.get(1.0, END)
			url = url.split('\n')
			for each in url:
				if each.replace(' ', '') != '':
					if each.startswith('https://youtu.be/') or each.startswith('https://www.youtube.com/watch?v='):
						try:
							get = YouTube(each)
							video = get.streams.filter(only_audio=False).get_highest_resolution()
							download = video.download(output_path='.')
							base, ext = os.path.splitext(download)
							new_file = base + '.mp4'
							os.rename(download, new_file)
							addLog("[Success] "+get.title+"\nSuccessfully Got Downloaded!")
						except Exception as e:
							try:
								addLog(f'[Error] Could Not Convert [{each}] Video To Mp4!')
							except:
								pass
							pass

					else:
						addLog(f'[Invalid URL] The URL [{each}] You Entered Is Not A Youtube Video URL!')
			showinfo("Done!", 'All Video(s) Have Been Converted\nCheck The Logs For Errors If Any...')
	else:
		showerror("URL(s) Not Supplied", "Cannot Convert To Mp3 Due To No URL(s) Given")


def OpenFromFile():
	file=askopenfilename(title='Choose A File That Contains Youtube URL(s) To Convert To...', filetypes=[("All Files", '*')])
	if file:
		try:
			with open(file, 'r') as readFile:
				urls.insert(1.0, readFile.read())
				readFile.close()

		except:
			showerror('File Opening Error', 'Could Not Open The Selected File!')

def HowToUse():
	HowTo=Toplevel()
	how=ScrolledText(HowTo, width='70', height='10')
	how.pack(fill=BOTH, expand=True)
	how.insert(1.0, """[How To Use The URL Box]
> Enter Each Youtube Video URL In A New Line.
> Please Avoid Blank Lines...

[How To Convert The Video URL(s) To Mp3/Mp4]
> Just Go To The Convert Then Choose The Format To Convert To...""")
	how.config(state=DISABLED)


def askCloseLog():
	sure_logs=askyesno("Close Logs?", "Are You Sure To Close The Log(s) Window?")
	if sure_logs:
		log.withdraw()

def showLogs():
	log.deiconify()

def addLog(Log):
	logs.config(state=NORMAL)
	logs.insert(1.0, Log+'\n\n')
	logs.config(state=DISABLED)


def paste():
	pastedValue=pyperclip.paste()
	urls.insert(END, pastedValue)

urls=ScrolledText(root, font=('Cascadia Code', 15), height='13', width='50', undo=True)
urls.pack(fill=BOTH, expand=True)

log=Toplevel()
log.title("Logs")
log.geometry("550x300")
logs=ScrolledText(log, width='70', height='20', state=DISABLED, font=('Cascadia Code', 15))
logs.pack(fill=BOTH, expand=True)
log.protocol('WM_DELETE_WINDOW', askCloseLog)

menu = Menu(root)
File = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=File)
File.add_command(label='Open', command=OpenFromFile)
File.add_command(label='Save')
File.add_separator()
File.add_command(label='Exit', command=root.destroy)

Convert = Menu(menu, tearoff=0)
menu.add_cascade(label='Convert', menu=Convert)
Convert.add_cascade(label='Convert To Mp3', command=ConvertToMp3)
Convert.add_cascade(label='Convert To Mp4', command=ConvertToMp4)

About = Menu(menu, tearoff=0)
menu.add_cascade(label='About', menu=About)
About.add_command(label='How To Use?', command=HowToUse)
About.add_command(label='Show Logs', command=showLogs)


# Right Click Menu

def popup(event):
	try:
		rc.tk_popup(event.x_root, event.y_root)
	finally:
		rc.grab_release()

rc=Menu(root, tearoff=0)
rc.add_command(label="Paste", command=paste)
root.bind('<Button-3>', popup)

# Configurations
root.config(menu=menu)
root.mainloop()