import sqlite3
import tkinter as tk
from tkinter import messagebox
import re
from random import randint
from tkinter import ttk
import hashlib
import csv
from datetime import datetime

conn = sqlite3.connect('KSUWorkshop.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS stu (
        StuID TEXT PRIMARY KEY,
        FName TEXT,
        LName TEXT,
        Password TEXT,
        Email TEXT,
        mobileNo TEXT
    );
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS workshop (
        workshopID TEXT PRIMARY KEY,
        workshopName TEXT,
        workshopLoc TEXT,
        workshopCap INTEGER,
        reservDate TEXT,
        reservTime TEXT
    );
''')



c.execute('''
    CREATE TABLE IF NOT EXISTS reservation (
        reservID TEXT PRIMARY KEY,
        StuID TEXT,
        workshopID TEXT,
        FOREIGN KEY(StuID) REFERENCES stu(StuID),
        FOREIGN KEY(workshopID) REFERENCES workshop(workshopID)
    );
''')

conn.commit()
conn.close()
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('400x350')
        self.root.title("KSU Workshop Reservation System")
        self.root.config(bg='lightblue')
        self.signup()
        self.root.mainloop()

    def signup(self):
        tk.Label(self.root, text="JOIN US! let's share and shine", width=25, font=("garamond", 15)).place(x=45, y=35)
        tk.Label(self.root, text="StudentID:", width=17, font=("bold", 10)).place(x=50, y=80)

        self.entry_3 = tk.Entry(self.root)
        self.entry_3.place(x=200, y=80)

        tk.Label(self.root, text="First Name:", width=17, font=("bold", 10)).place(x=50, y=110)
        self.fNameEntry = tk.Entry(self.root)
        self.fNameEntry.place(x=200, y=110)

        tk.Label(self.root, text="Last Name:", width=17, font=("bold", 10)).place(x=50, y=140)
        self.lNameEntry = tk.Entry(self.root)
        self.lNameEntry.place(x=200, y=140)

        tk.Label(self.root, text="Password:", width=17, font=("bold", 10)).place(x=50, y=170)
        self.passEntry = tk.Entry(self.root, show='*')
        self.passEntry.place(x=200, y=170)

        tk.Label(self.root, text="Email address:", width=17, font=("bold", 10)).place(x=50, y=200)
        self.emailEntry = tk.Entry(self.root)
        self.emailEntry.place(x=200, y=200)

        tk.Label(self.root, text="Phone number:", width=17, font=("bold", 10)).place(x=50, y=230)
        self.mobileEntry = tk.Entry(self.root)
        self.mobileEntry.place(x=200, y=230)

        tk.Button(self.root, text='Save', width=20, command=self.save_student_info).place(x=120, y=280)
        tk.Button(self.root, text='Login', width=20, command=self.login_window).place(x=120, y=310)

        self.create_admin_account()


    def create_admin_account(self):
        conn = sqlite3.connect('KSUWorkshop.db')
        c = conn.cursor()
        admin_password = self.hash_password("admin123")
        c.execute(
            "INSERT OR IGNORE INTO stu VALUES ('000000000', 'Admin', 'User', ?, 'admin@ksu.edu.sa', '0500000000')",
            (admin_password,))
        conn.commit()
        conn.close()

    def hash_password(self, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return  hashed


    def verify_password(self, password, stored_password):
        passW = password.encode()
        return hashlib.sha256(passW).hexdigest() == stored_password


    def save_student_info(self):

            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            StuID = self.entry_3.get()
            firstname = self.fNameEntry.get()
            lastname = self.lNameEntry.get()
            password = self.passEntry.get()
            email = self.emailEntry.get()
            mobile = self.mobileEntry.get()
            if not re.match(r"^\d{9}$", StuID):

                messagebox.showinfo("Invalid input", "Student ID must be 9 digits")
                return

            if not firstname or not lastname:
                messagebox.showinfo("Invalid input", "First name and last name cannot be empty")
                return

            if not re.match(r"^[A-Za-z0-9]{6,}$", password):
                messagebox.showinfo("Invalid input", "Password must be at least 6 characters")
                return

            if not re.match(r"^[a-zA-Z0-9._%+-]+@student\.ksu\.edu\.sa$", email):
                messagebox.showinfo("Invalid input", "Invalid email format")
                return

            if not re.match(r"^(05)\d{8}$", mobile):
                messagebox.showinfo("Invalid input", "Invalid mobile number format")
                return

            hashed_password = self.hash_password(password)
            c.execute("SELECT StuID FROM stu WHERE StuID = ?", (StuID,))
            if c.fetchone():
                messagebox.showinfo("Error", "Student ID already exists")
                return

            c.execute("INSERT INTO stu VALUES (?, ?, ?, ?, ?, ?)",
                      (StuID, firstname, lastname, hashed_password, email, mobile))

            conn.commit()

            messagebox.showinfo("Success", "Student registered successfully")


    def login_window(self):

        self.root.withdraw()

        self.login_frame = tk.Toplevel(self.root)
        self.login_frame.geometry('400x200')
        self.login_frame.title("Login")
        self.login_frame.config(bg='lightblue')

        tk.Label(self.login_frame, text="᯽WELCOME᯽", width=15, font=("garamond", 15)).place(x=10, y=20)

        self.userVar = tk.StringVar()
        self.passwordVar = tk.StringVar()

        tk.Label(self.login_frame, text="ID:", width=20, font=("bold", 10)).place(x=0, y=60)

        self.idEntry = tk.Entry(self.login_frame, textvariable=self.userVar)
        self.idEntry.place(x=170, y=60)

        tk.Label(self.login_frame, text="Password:", width=20, font=("bold", 10)).place(x=0, y=90)

        self.userEntry = tk.Entry(self.login_frame, textvariable=self.passwordVar, show='*')
        self.userEntry.place(x=170, y=90)

        tk.Button(self.login_frame, text="Sign in", width=10, command=self.signin).place(x=150, y=130)


    def log_transaction(self, user_id, workshop_name, location, date_time, success=True):

        timeNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 'Success' if success else 'Fail'
        with open('Transactions.log.txt', 'a') as log_file:

            log_file.write(
                f"{timeNow} / {status} / ID: {user_id} / Workshop:{workshop_name} / Location: {location} / Date&Time: {date_time} \n")

    def signin(self):


            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            uid = self.userVar.get()
            pwd = self.passwordVar.get()

            if not re.match(r"^\d{9}$", uid):
                messagebox.showinfo("Invalid ID", "ID must be 9 digits")
                return

            c.execute("SELECT Password FROM stu WHERE StuID = ?", (uid,))
            user_data = c.fetchone()
            conn.close()

            if user_data:
                hashed_password = user_data[0]
                if self.verify_password(pwd, hashed_password):
                    messagebox.showinfo("Success", "Login Successful")

                    if uid == "000000000":
                        self.login_frame.withdraw()
                        self.create_admin_window()

                    else:
                        self.login_frame.withdraw()
                        self.booking_tickets_window(uid)

                else:
                    messagebox.showinfo("Error", "Incorrect password")

            else:
                messagebox.showinfo("Error", "User not found")



    def create_admin_window(self):


                    self.admin_window = tk.Toplevel(self.root)
                    self.admin_window.geometry('500x400')
                    self.admin_window.title("Admin Page")
                    self.admin_window.config(bg='lightblue')


                    tk.Label(self.admin_window, text="Workshop Name:").pack()
                    self.workshopName = tk.Entry(self.admin_window)
                    self.workshopName.pack()

                    tk.Label(self.admin_window, text="Workshop Location:").pack()
                    self.workshopLocation = tk.Entry(self.admin_window)
                    self.workshopLocation.pack()

                    tk.Label(self.admin_window, text="Workshop Capacity:").pack()
                    self.workshopCapacity = tk.Entry(self.admin_window)
                    self.workshopCapacity.pack()

                    tk.Label(self.admin_window, text="Date & Time (YYYY-MM-DD HH:MM):").pack()
                    self.workshopDateTime = tk.Entry(self.admin_window)
                    self.workshopDateTime.pack()

                    tk.Button(self.admin_window, text="Create Workshop", command=self.create_workshop).pack()
                    tk.Button(self.admin_window, text="Backup Data", command=self.backup_data).pack()
                    tk.Button(self.admin_window, text="Logout", command=self.logout).pack()

    def create_workshop(self):

            workshop_id = str(randint(10000, 99999))
            name = self.workshopName.get()
            location = self.workshopLocation.get()
            capacity = int(self.workshopCapacity.get())
            date, time = self.workshopDateTime.get().split()
            conn = sqlite3.connect('KSUWorkshop.db')

            c = conn.cursor()
            c.execute("INSERT INTO workshop VALUES (?, ?, ?, ?, ?, ?)",

                      (workshop_id, name, location, capacity, date, time))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Workshop created successfully")

    def backup_data(self):

            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            c.execute("SELECT * FROM workshop")
            data = c.fetchall()
            conn.close()

            with open('backup.csv', 'w', newline='') as file:

                writer = csv.writer(file)
                writer.writerow(["Workshop ID", "Name", "Location", "Capacity", "Date", "Time"])
                writer.writerows(data)

            messagebox.showinfo("Success", "Data backed up successfully")


    def booking_tickets_window(self, uid):

        self.booking_window = tk.Toplevel(self.root)
        self.booking_window.geometry('700x400')
        self.booking_window.title("Booking Workshops")
        self.booking_window.config(bg='lightblue')

        self.notebook = ttk.Notebook(self.booking_window)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = ttk.Frame(self.notebook, width=500, height=200)
        self.frame2 = ttk.Frame(self.notebook, width=500)

        self.notebook.add(self.frame1, text="Book a Workshop")
        self.notebook.add(self.frame2, text="View My Workshops")

        self.display_workshops(self.frame1)

        self.bookedListbox1 = tk.Listbox(self.frame2, width=50, height=10)
        self.bookedListbox1.pack(pady=10)

        self.view_button = tk.Button(self.frame2, text="Show All", width=20,

                                     command=lambda: self.display_all_booked_workshops(self.frame2, uid))

        self.view_button.pack(pady=10)

        self.bookedListbox2 = tk.Listbox(self.frame2, width=50, height=10)

        self.bookedListbox2.pack(pady=10)

        self.display_upcoming_booked_workshops(self.frame2, uid)

        tk.Button(self.booking_window, text='Logout', width=10, bg='AntiqueWhite3', fg='black',
                  command=self.logout).place(x=300, y=350)

    def display_workshops(self, frame):

            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            now=datetime.now().strftime("%Y-%m-%d %H:%M")
            workshops = c.execute("SELECT * FROM workshop")
            workshop_data = workshops.fetchall()
            conn.close()

            self.workshopListbox = tk.Listbox(frame, width=50, height=10)
            self.workshopListbox.pack(pady=10)

            for workshop in workshop_data:
                workshop_info = f"ID: {workshop[0]}, Name: {workshop[1]}, Location: {workshop[2]}, Capacity: {workshop[3]}, Date: {workshop[4]}, Time: {workshop[5]}"
                if workshop[4]>now :
                 self.workshopListbox.insert(tk.END, workshop_info)

            tk.Button(frame, text='Book', width=10, bg='AntiqueWhite3', fg='black',
                      command=lambda: self.book_workshop(self.workshopListbox.get(tk.ANCHOR))).pack()


    def display_upcoming_booked_workshops(self, frame, uid):

            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            now = datetime.now().strftime('%Y-%m-%d HH:MM')
            booked_workshops = c.execute("""

                SELECT w.workshopName, w.workshopLoc, w.reservDate, w.reservTime
                FROM reservation r
                JOIN workshop w ON r.workshopID = w.workshopID
                WHERE r.StuID = ? AND DATE(w.reservDate) >= ?
            """, (uid, now))

            booked_data = booked_workshops.fetchall()

            conn.close()

            self.bookedListbox1.delete(0, tk.END            )  
            if booked_data:
                for workshop in booked_data:
                    workshop_info = f"Name: {workshop[0]}, Location: {workshop[1]}, Date: {workshop[2]}, Time: {workshop[3]}"
                    self.bookedListbox1.insert(tk.END, workshop_info)


    def display_all_booked_workshops(self, frame, uid):

            conn = sqlite3.connect('KSUWorkshop.db')

            c = conn.cursor()

            booked_workshops = c.execute("""

                SELECT w.workshopName, w.workshopLoc, w.reservDate, w.reservTime
                FROM reservation r
                JOIN workshop w ON r.workshopID = w.workshopID
                WHERE r.StuID = ?

            """, (uid,))

            booked_data = booked_workshops.fetchall()
            conn.close()
            self.bookedListbox2.delete(0, tk.END)  

            if booked_data:
                for workshop in booked_data:
                    workshop_info = f"Name: {workshop[0]}, Location: {workshop[1]}, Date: {workshop[2]}, Time: {workshop[3]}"

                    self.bookedListbox2.insert(tk.END, workshop_info)

            else:
                self.bookedListbox2.insert(tk.END, "No workshops booked yet.")


    def book_workshop(self, workshop_info):

            conn = sqlite3.connect('KSUWorkshop.db')
            c = conn.cursor()
            workshop_id = workshop_info.split(",")[0].split(":")[1].strip()

            existing_reservation = c.execute("SELECT * FROM reservation WHERE StuID = ? AND workshopID = ?",

                                             (self.userVar.get(), workshop_id))

            if existing_reservation.fetchone():
                messagebox.showinfo("Error", "You have already booked this workshop.")
                workshop_details = c.execute(
                    "SELECT workshopName, workshopLoc, reservDate, reservTime FROM workshop WHERE workshopID = ?",

                    (workshop_id,))

                workshop_data = workshop_details.fetchone()

                workshop_name, workshop_location, reserv_date, reserv_time = workshop_data

                self.log_transaction(self.userVar.get(), workshop_name, workshop_location,
                                     f"{reserv_date} {reserv_time}", success=False)

                conn.close()
                return

            workshop_details = c.execute(

                "SELECT workshopName, workshopLoc, reservDate, reservTime FROM workshop WHERE workshopID = ?",

                (workshop_id,))

            workshop_data = workshop_details.fetchone()
            workshop_name, workshop_location, reserv_date, reserv_time = workshop_data
            capacity = c.execute("SELECT workshopCap FROM workshop WHERE workshopID = ?", (workshop_id,))
            current_capacity = capacity.fetchone()[0]

            if current_capacity == 0:

                messagebox.showinfo("Error", "This workshop is fully booked.")
                self.log_transaction(self.userVar.get(), workshop_name, workshop_location,

                                     f"{reserv_date} {reserv_time}", success=False)

                conn.close()
                return

            reservID = str(randint(10000, 99999))
            c.execute("INSERT INTO reservation VALUES(?, ?, ?)", (reservID, self.userVar.get(), workshop_id))
            c.execute("UPDATE workshop SET workshopCap = workshopCap - 1 WHERE workshopID = ?", (workshop_id,))
            conn.commit()

            messagebox.showinfo("Success", "Workshop booked successfully.")
            self.log_transaction(self.userVar.get(), workshop_name, workshop_location,

                                 f"{reserv_date} {reserv_time}", success=True)

            conn.close()
            self.workshopListbox.delete(0, tk.END)
            self.display_workshops(self.frame1)
            self.bookedListbox1.delete(0, tk.END)
            self.display_upcoming_booked_workshops(self.frame2, self.userVar.get())

    def logout(self):

        if hasattr(self, 'admin_window') and self.admin_window.winfo_exists():
            self.admin_window.destroy()

        if hasattr(self, 'booking_window') and self.booking_window.winfo_exists():
            self.booking_window.destroy()

        self.root.deiconify()

        self.signup()

if __name__ == "__main__":
    gui = GUI()
