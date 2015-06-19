#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from queue import Queue
from itertools import count
from threading import Thread, current_thread, RLock, Event
from tkinter import Tk, Text, Button, Frame, Scrollbar, Label, Entry

service_time = 1  # Request service time
queue = Queue()  # FIFO queue
task_count = count(start=1)  # Request counter
event = Event()  # Continuation flag
lock = RLock()  # For synchronization


class Visual(object):
    """Class where UI is created"""

    def __init__(self):
        self.__root = Tk()  # Create window
        self.__root.wm_title("An Service System Example")  # title
        self.__root.geometry('650x380')  # Window size
        self.__add_frames()
        self.__add_text_fields()
        self.__add_buttons()
        self.__add_labels()
        self.__frame1.pack(side='left', padx=10)
        self.__frame2.pack(side='left', padx=10)
        self.__frame3.pack(side='right', padx=10)

    def run(self):  # UI running method
        self.__root.mainloop()

    def log_message(self, message):  # Method for printing log messages (threads do)
        self.__log['state'] = 'normal'
        self.__log.insert('end', message)
        self.__log['state'] = 'disabled'

    @property
    def text(self):
        line = self.__task_list.get('1.0', '1.0 lineend')
        self.__task_list.delete('1.0', '1.0 lineend+1c')
        return line

    @text.setter
    def text(self, par):
        self.__task_list['state'] = 'normal'
        self.__task_list.insert('end', par)
        self.__task_list['state'] = 'disabled'

    def delete_spec_line(self, line):  # Method for deleting messages from task_list
        if self.__task_list.search(line, '1.0'):
            self.__task_list['state'] = 'normal'
            self.__task_list.delete('{}'.format(self.__task_list.search(line, '1.0')),
                                    '{} lineend+1c'.format(self.__task_list.search(line, '1.0')))
            self.__task_list['state'] = 'disabled'
            return True
        else:
            return False

    def clear(self):  # Method for clearing queue and visual components
        global queue
        self.__task_list['state'] = 'normal'
        self.__task_list.delete('1.0', 'end')
        self.__task_list['state'] = 'disabled'
        self.__log['state'] = 'normal'
        self.__log.delete('1.0', 'end')
        self.__log['state'] = 'disabled'
        with queue.mutex:
            queue.queue.clear()

    def get_value(self):  # Method returns requested processes number
        return int(self._entry.get())

    def __add_buttons(self):  # Add buttons, etc
        Label(self.__frame3, text='Processes').pack(side='top')
        self._entry = Entry(self.__frame3, justify='center')
        self._entry.insert(0, 5)
        self._entry.pack(side='top', pady=10)
        self._start_btn = Button(self.__frame3, text='Start', width=10, command=lambda: start_workers(self, self.get_value()))
        self._start_btn.pack(side='top')
        Button(self.__frame3, text='Add', width=10, command=lambda: add_task(self)).pack(side='top')
        Button(self.__frame3, text='Pause/Run', width=10, command=pause_resume).pack(side='top')
        Button(self.__frame3, text='Clear', width=10, command=self.clear).pack(side='top')

    def __add_labels(self):  # Add inscriptions
        Label(self.__frame1, text='Process Log').pack(side='top')
        Label(self.__frame2, text='Task List').pack(side='top')

    def __add_text_fields(self):  # Add list-boxes
        self.__log = Text(self.__frame1, height=20, width=30, state='disabled')
        self.__task_list = Text(self.__frame2, height=20, width=30, state='disabled')
        self.__log_scroll_y = Scrollbar(self.__frame1, command=self.__log.yview)
        self.__info_scroll_y = Scrollbar(self.__frame2, command=self.__task_list.yview)
        self.__log.configure(yscrollcommand=self.__log_scroll_y.set)
        self.__task_list.configure(yscrollcommand=self.__info_scroll_y.set)
        self.__log_scroll_y.pack(side='right', fill='y')
        self.__info_scroll_y.pack(side='right', fill='y')
        self.__log.pack(side='bottom')
        self.__task_list.pack(side='bottom')

    def __add_frames(self):  # Add frames
        self.__frame1 = Frame(self.__root)
        self.__frame2 = Frame(self.__root)
        self.__frame3 = Frame(self.__root)


def worker(visual):  # Function which is executed by threads
    global queue, lock, event
    while True:
        event.wait()
        task = queue.get()
        sleep(service_time)
        queue.task_done()
        with lock:
            visual.log_message("{} done {}".format(str(current_thread())[-6:-2], task))
            visual.delete_spec_line(task)
        if queue.empty():
            event.clear()
            # visual.log_message("{} : Queue is empty\n".format(str(current_thread())[-6:-2]))


def add_task(visual):  # Function which adds request to queue and visual component (task_list)
    global task_count, queue
    task = "Task {}\n".format(next(task_count))
    queue.put(task)
    visual.text = task


def pause_resume():  # Function is executed when app should be paused or resumed
    global event
    if event.is_set():
        event.clear()
    else:
        event.set()


def start_workers(visual, process_number):  # Function which starts threads
    visual._start_btn.config(state='disabled')
    visual._entry.config(state='disabled')
    pause_resume()
    for i in range(process_number):
        Thread(target=lambda: worker(visual), daemon=True).start()


def main():  # The entry point to the application
    visual = Visual()
    visual.run()


if __name__ == '__main__': main()
