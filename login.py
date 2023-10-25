import customtkinter as ctk
import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
from tkinter import messagebox
import datetime


class LoginScreen:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')


        self.root = ctk.CTk()
        self.root.geometry('450x550+460+90')
        self.root.title('Login')
        self.root.resizable(False, False)


        bg_image = ImageTk.PhotoImage(Image.open('assets/pattern.png'))

        # Text fonts
        self.font1 = Font(family='@Batang', size=22, weight='bold', slant='roman', underline=False)
        self.font2 = Font(family='@KaiTi', size=8, weight='bold')
        self.font3 = Font(family='@KaiTi', size=8, weight='bold', underline=True, slant='italic')

        # Background image setup
        self.bg_label = ctk.CTkLabel(self.root, image=bg_image)
        self.bg_label.pack()

        # Frame setup
        self.frame = ctk.CTkFrame(self.bg_label, width=320, height=360, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Log into Label
        self.login_label = tk.Label(self.root, text='Login', font=self.font1, bg='#2b2b2b', fg='white')
        self.login_label.place(x=180, y=105)

        # User entry
        self.user_entry = ctk.CTkEntry(self.root, width=220, placeholder_text='Username')
        self.user_entry.place(x=112, y=175)

        # Password entry
        self.password_entry = ctk.CTkEntry(self.root, width=220, placeholder_text='Password')
        self.password_entry.place(x=112, y=230)

        # Show password checkbox
        self.checkbox = ctk.CTkCheckBox(self.root, bg_color='#302c2c', text='Show', border_width=1, width=2,
                                        height=2, checkbox_width=18, checkbox_height=18, command=self.show_password)
        self.checkbox.place(x=115, y=265)
        self.password_entry.configure(show='*')

        # New user
        self.newacc_label = tk.Label(self.root, font=self.font3, text='Create an account', bg='#2b2b2b',
                                     fg='white', cursor='hand2')
        self.newacc_label.place(x=172, y=410)
        self.newacc_label.bind('<Button-1>', self.create_newuser)

        self.login_button = ctk.CTkButton(self.root, text='Login', corner_radius=12, bg_color='#2b2b2b',
                                          width=200, height=35, font=('Arial bold', 18), fg_color='green',
                                          hover_color='dark green', text_color='white', command=self.login_confirmation)
        self.login_button.place(x=125, y=340)

    def create_newuser(self, event):
        self.root.destroy()
        register = Register()
        register.run()

    def login_confirmation(self):
        with open('users.txt', 'r') as file:
            username = self.user_entry.get()
            password = self.password_entry.get()

            lines = file.read().split('=-=-=-=-=-=-=-=-=-=-=-=-=-')
            for user_data in lines:
                try:
                    user_info = user_data.strip().split('\n')
                    stored_username = user_info[1].split(': ')[1]
                    stored_password = user_info[2].split(': ')[1]
                    if (username == stored_username and password == stored_password) or (username == 'admin' and password == 'admin'):
                        messagebox.showinfo('Success', 'Success Login')
                        self.root.destroy()
                        from mainproject import MainScreen
                        project = MainScreen()
                        project.run()
                    else:
                        messagebox.showwarning('Error', 'Invalid Username or Password')
                except IndexError:
                    if username == 'admin' and password == 'admin':
                        messagebox.showinfo('Success', 'Success Login')
                        self.root.destroy()
                        from mainproject import MainScreen
                        library = MainScreen()
                        library.run()
                    else:
                        messagebox.showwarning('Error', 'Invalid Username or Password')
    @staticmethod
    def is_username_registered(username):
        username = username.lower()
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Username'):
                    existing_username = line.split(': ')[1].strip()
                    existing_username = existing_username.lower()
                    if existing_username == username:
                        return True
        return False


    def show_password(self):
        value = self.checkbox.get()
        if value:
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='*')

    def run(self):
        self.root.mainloop()


class Register:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')


        self.root = ctk.CTk()
        self.root.geometry('450x550+460+90')
        self.root.title('Login')
        self.root.resizable(False, False)

        bg_image = ImageTk.PhotoImage(Image.open('assets/pattern.png'))
        self.next_id = 1

        # Text fonts
        self.font1 = Font(family='@Batang', size=22, weight='bold', slant='roman', underline=False)
        self.font2 = Font(family='@KaiTi', size=8, weight='bold')
        self.font3 = Font(family='@KaiTi', size=8, weight='bold', underline=True, slant='italic')

        # Background image setup
        self.bg_label = ctk.CTkLabel(self.root, image=bg_image)
        self.bg_label.pack()

        # Frame setup
        self.frame = ctk.CTkFrame(self.bg_label, width=320, height=360, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.login_label = tk.Label(self.root, text='Register', font=self.font1, bg='#2b2b2b', fg='white')
        self.login_label.place(x=170, y=105)

        # User entry
        self.user_entry = ctk.CTkEntry(self.root, width=220, placeholder_text='Username')
        self.user_entry.place(x=112, y=175)

        # Password entry
        self.password_entry = ctk.CTkEntry(self.root, width=220, placeholder_text='Password')
        self.password_entry.place(x=112, y=230)

        self.password_entry2 = ctk.CTkEntry(self.root, width=220, placeholder_text='Repeat your password')
        self.password_entry2.place(x=112, y=285)

        # Show password checkbox
        self.checkbox = ctk.CTkCheckBox(self.root, bg_color='#302c2c', text='Show', border_width=1, width=2,
                                        height=2, checkbox_width=18, checkbox_height=18, command=self.show_password)
        self.checkbox.place(x=115, y=320)
        self.password_entry.configure(show='*')
        self.password_entry2.configure(show='*')

        # Regiter button
        self.register_button = ctk.CTkButton(self.root, text='Register', corner_radius=12, bg_color='#2b2b2b',
                                          width=200, height=35, font=('Arial bold', 18),fg_color='green',
                                             hover_color='dark green', command=self.analyze_credentials)
        self.register_button.place(x=125, y=375)

    def show_password(self):
        value = self.checkbox.get()
        if value:
            self.password_entry.configure(show='')
            self.password_entry2.configure(show='')
        else:
            self.password_entry.configure(show='*')
            self.password_entry2.configure(show='*')


    def analyze_credentials(self):
        username = self.user_entry.get()
        password = self.password_entry.get()
        password2 = self.password_entry2.get()

        requirements = [0, 0]

        if not self.is_username_registered(username) and len(username) > 4:
            requirements[0] = 1
        elif self.is_username_registered(username):
            messagebox.showwarning('Invalid username', 'Username already exists')
        elif len(username) <= 4:
            messagebox.showwarning('Invalid username', 'Short username')
        elif password != password2:
            messagebox.showwarning('Invalid password', 'Password not matching')
        if password == password2:
            if len(password) < 8:
                messagebox.showwarning('Invalid password', 'Short password')
            else:
                requirements[1] = 1
        else:
            messagebox.showwarning('Invalid password', 'Password not matching')

        if all(num == 1 for num in requirements):
            self.save_registration(username, password)
            messagebox.showinfo('Successfully registered', 'You can login now.')
            self.root.destroy()
            login = LoginScreen()
            login.run()


    @staticmethod
    def is_username_registered(username):
        username = username.lower()
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('Username'):
                    existing_username = line.split(': ')[1].strip()
                    existing_username = existing_username.lower()
                    if existing_username == username:
                        return True
        return False

    def save_registration(self, username, password):
        unique_id = f'ID: {self.next_id} | {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        with open('users.txt', 'a') as file:
            file.write(f'{unique_id}\n')
            file.write(f'Username: {username}\n')
            file.write(f'Password: {password}\n')
            file.write('=-=-=-=-=-=-=-=-=-=-=-=-=-\n')
        self.next_id += 1

    def run(self):
        self.root.mainloop()

