from tkinter import *
from Drowsiness_Detection import Drowsiness_Detection

window = Tk()
window.title("졸음 방지 경보기 프로그램")
window.geometry('300x500+500+200')
frame = Frame(window, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=2)
frame.config(background='#6FA0BF')
label = Label(frame,
              text="졸음 경보 프로그램",
              bg='#6FA0BF',
              foreground='white',
              font=('Arial 20 bold')
              )
label.place(x=70, y=30)

img = PhotoImage(file='Image/eye_icon.png')
img_label = Label(
    bg='#6FA0BF',
    image=img
)
img_label.place(x=70, y=80)

drow_detect = Drowsiness_Detection

# 버튼 생성
button = Button(frame, padx=5, pady=5, width=15, bg='white', fg='black', relief=GROOVE, command=drow_detect, text='Start',font=('helvetica 15 bold'))
button.place(x=75, y=290)

window.mainloop()


