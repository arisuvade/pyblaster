#!/usr/bin/env python3

import customtkinter as ctk
import pyautogui as pg
import time

from message_input import MessageInput
from count_input import CountInput
from send_button import SendButton

from title import TitleUpdater
from theme import ThemeSwitch
from message_counter import MessageCounter


class MessageSpammer:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.geometry("300x220")
        self.master.resizable(False, False)
        self.master.wm_title("Spammer")

        # Title
        self.title = TitleUpdater(master=self.master)

        # Call update_title method every 3 seconds
        self.master.after(3000, self.title.update_title)

        # Message
        self.msg = MessageInput(self.master)
        self.msg.place(relx=0.5, rely=0.2, anchor="center")

        # Count
        self.count = CountInput(self.master)
        self.count.place(relx=0.5, rely=0.4, anchor="center")

        # Send
        self.send = SendButton(self.master, command=self.send_msg)
        self.send.place(relx=0.5, rely=0.6, anchor="center")

        # Theme switch
        self.theme_switch = ThemeSwitch(self.master)
        self.theme_switch.place(relx=0.5, rely=0.8, anchor="center")

        # Message counter
        self.counter = MessageCounter()

        # Current progress label
        self.current_progress_label = ctk.CTkLabel(
            self.master,
            text="0",
            font=("Jetbrains Mono", 12),
        )
        self.current_progress_label.place(relx=0.15, rely=0.8, anchor="center")

        # Total progress label
        self.total_progress_label = ctk.CTkLabel(
            self.master,
            text="0",
            font=("Jetbrains Mono", 12),
        )
        self.total_progress_label.place(relx=0.85, rely=0.8, anchor="center")

        # Error
        self.error_label = ctk.CTkLabel(
            self.master,
            text="",
            font=("Jetbrains Mono", 12, "bold"),
            text_color="red",
        )
        self.error_label.place(relx=0.5, rely=0.93, anchor="center")

    def send_msg(self):
        try:
            # Clear error message
            self.error_label.configure(text="")

            # Get count from user input
            count = int(self.count.get())

            # Total count
            total_count = self.counter.get_count() + 1

            # To move the mouse and run
            height, width = pg.size()
            pg.click(height / 2, width / 4)
            pg.click()

            # To send the message
            pos = pg.position()
            for i in range(count):

                # Check if the mouse position has changed to end the loop
                if pos != pg.position():
                    break

                # Send the message
                pg.typewrite(self.msg.get())
                pg.press("enter")
                time.sleep(0.3)

                # Update current progress label
                current_count = i + 1
                self.counter.increment()
                current_progress_text = f"{current_count}"
                self.current_progress_label.configure(text=current_progress_text)
                self.current_progress_label.update()

                # Update total progress label
                total_count += 1
                total_progress_text = f"{total_count}"
                self.total_progress_label.configure(text=total_progress_text)
                self.total_progress_label.update()

        except ValueError:
            # Show the error in app
            self.error_label.configure(text="Error: Invalid number in count.")


if __name__ == "__main__":
    app = ctk.CTk()
    gui = MessageSpammer(master=app)
    app.mainloop()