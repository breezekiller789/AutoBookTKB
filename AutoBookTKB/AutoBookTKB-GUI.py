# !/usr/bin/python
# -*-coding:utf-8 -*-
import tkinter as tk
from tkinter import ttk
import json
import sys
import threading

class AutoBookTKB_GUI:

    def __init__(self, master): 
        self.load_json('AutoBookTKB-settings.json')

        self.master = master
        self.master.title("AutoBookTKB")

        self.id_box = ttk.Entry(self.master) # Id: Entry
        self.id_box.insert(tk.END, self.settings['id']) # Set default

        self.pwd_box = ttk.Entry(self.master,show='*') # Password: Entry
        self.pwd_box.insert(tk.END, self.settings['password']) # Set default

        # Course: Combobox.
        self.course_chosen = tk.StringVar()
        self.course = ttk.Combobox(self.master, width=18, 
                                   textvariable=self.course_chosen)
        self.course['values'] = (u"請選擇課程:", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        # Set default
        if self.settings['classIndex'].isdigit():
            self.course.current(self.settings['classIndex'])
        else:
            self.course.current(0)

        # Date: Label
        self.date = ttk.Label(master, text=self.get_date_text())

        # Location: Combobox
        self.location_chosen = tk.StringVar()
        self.location = ttk.Combobox(self.master, width=18, 
                                     textvariable=self.location_chosen)
        with open('locationList.json', 'r', encoding="utf-8") as fp:
            self.location_list = json.load(fp)
        fp.close()
        self.mylist = []
        self.mylist.append(u'請選擇預約地點')
        for key in self.location_list:
            self.mylist.append(key)
        self.location['values'] = tuple(self.mylist)
        # Set default
        if self.settings['location']:
            self.location.current(self.mylist.index(self.settings['location']))
        else:
            self.location.current(0)

        # Sessions: Checkbuttons
        self.session_checked = [0, 0, 0, 0, 0, 0]
        self.session_checkbuttons = []
        for s in range(len(self.session_checked)):
            self.session_checked[s] = tk.IntVar()
            chkbut = tk.Checkbutton(self.master, text=str(s), 
                                    variable=self.session_checked[s], 
                                    onvalue=1, offvalue=0)
            self.session_checkbuttons.append(chkbut)
            # Set default
            if s in self.settings['sessions']:
                chkbut.select()

        # Send: Button
        self.send_button = ttk.Button(self.master, text=u"送出", command=self.send)

        self.console = ttk.Entry(self.master) 

        self.master.geometry('450x600')
        self.show_gui()

    def send(self):
        self.print_log()
        self.update_settings()
        self.update_json('AutoBookTKB-settings.json')
        t = threading.Thread(target=self.auto_book)
        t.start()

    def print_log(self):
        # sys.stdout = __redirection__(self.console)
        print("*************************")
        print("id: " + self.id_box.get())
        print("pwd: " + self.pwd_box.get())
        print("course: " + self.course_chosen.get())
        print("location: " + self.location_chosen.get())

        self.sessions = []
        for idx, val in enumerate(self.session_checked):
            if val.get():
                self.sessions.append(idx)
        print("sessions: " + str(self.sessions))

        print("*************************")


    def update_settings(self):
        self.settings['id'] = self.id_box.get()
        self.settings['password'] = self.pwd_box.get()
        self.settings['classIndex'] = self.course_chosen.get()
        self.settings['location'] = self.location_chosen.get()
        self.settings['sessions'] = self.sessions

    def update_json(self, f):
        with open(f, 'w+', encoding="utf-8") as fp:
            json.dump(self.settings, fp, indent=4, ensure_ascii=False)
        fp.close()

    def load_json(self, f):
        with open(f, 'r', encoding="utf-8") as fp:
             self.settings = json.load(fp)
        fp.close()

    def get_date_text(self):
        import datetime
        date = datetime.date.today() + datetime.timedelta(days=6)
        return(str(date))

    def show_gui(self):
        ttk.Label(self.master, text=u"自動預約TKB上課座位")
        ttk.Label(self.master, text="==================")

        ttk.Label(self.master, text=u'身分證字號: ').place(x=50, y=80)
        ttk.Label(self.master, text=u'密碼: ').place(x=50, y=120)

        self.id_box.place(x=160, y=80)
        self.pwd_box.place(x=160, y=120)

        ttk.Label(self.master, text=u'課程: ').place(x=50, y=160)
        self.course.place(x=160, y=160)

        ttk.Label(self.master, text=u'日期: ').place(x=50, y=200)
        self.date.place(x=160, y=200)

        ttk.Label(self.master, text=u'地點: ').place(x=50, y=240)
        self.location.place(x=160, y=240)

        ttk.Label(self.master, text=u'場次: ').place(x=50, y=280)
        y = 280
        for s in range(len(self.session_checked)):
            self.session_checkbuttons[s].place(x=160, y=y)
            y = y + 20

        ttk.Label(self.master, 
            text=u"按下送出後，將會於中午12:00或午夜12:00自動進行預約。").place(x=50, y=420)

        self.send_button.place(x=160, y=440)

    def auto_book(self):
        from AutoBookTKB import AutoBookTKB
        atb = AutoBookTKB('AutoBookTKB-settings.json')
        atb.main()


class __redirection__():
    def __init__(self, s):
        self.buf=''
        self.__console__=sys.stdout
        self.console = s

    def write(self, s):
        s = s + '\n'
        self.console.insert(tk.END, s)

    def to_console(self):
        sys.stdout = self.__console__
        print(self.buf)

    def flush(self):
        self.buff=''


if __name__ == '__main__':
    root = tk.Tk()
    atb_gui = AutoBookTKB_GUI(root)
    root.mainloop()

