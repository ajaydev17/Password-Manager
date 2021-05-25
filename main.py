from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END, messagebox
import random
import json
import pyperclip3

# Constants

BLACK = "#000000"
GRAY = "#A9A9A9"
FONT = ("Arial", 12, "normal")
padding = (0, 10)
file_name = "data.json"


# Password Save Functionality

def save_password():
    website_entered = website_entry.get()
    email_entered = email_entry.get()
    password_entered = password_entry.get()

    new_data = {
        website_entered: {
            "email": email_entered,
            "password": password_entered
        }
    }

    if len(website_entered) == 0 or len(password_entered) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure that you have not left any fields empty!!!")
    else:
        is_ok = messagebox.askokcancel(title=website_entered,
                                       message=f"These are the details entered: \nEmail: {email_entered} "
                                               f"\nPassword: {password_entered}\n Is it ok to "
                                               f"save?")

        if is_ok:
            try:
                with open(file_name, "r") as data_file:
                    # Load json data
                    data = json.load(data_file)
            except FileNotFoundError:
                # Create file
                with open(file_name, "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Dump json data
                data.update(new_data)

                with open(file_name, "w") as data_file:
                    # Dump json data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()


# Generate Password

def generate_random_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    char_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    number_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    symbol_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = char_list + number_list + symbol_list
    random.shuffle(password_list)
    password_string = ''.join(password_list)

    # Copy to Clipboard
    pyperclip3.copy(password_string)

    password_entry.insert(0, password_string)


# Search Password

def search_password():
    website_entered = website_entry.get()

    if len(website_entered) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure that you have not left any fields empty!!!")
    else:
        try:
            with open(file_name, "r") as data_file:
                # Load data
                data = json.load(data_file)
                email_fetched = data[website_entered]['email']
                password_fetched = data[website_entered]['password']

                # Copy to Clipboard
                pyperclip3.copy(password_fetched)

                messagebox.showinfo(title=website_entered, message=f"Email: {email_fetched}\n"
                                                                   f"Password: {password_fetched}")
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message=f"No data file found!!!")
        except KeyError:
            messagebox.showinfo(title="Oops", message=f"Website {website_entered} not found in the password manager!!!")
        finally:
            website_entry.delete(0, END)


# Create Window

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BLACK)

# Canvas

canvas = Canvas(width=200, height=200, bg=BLACK, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Labels

website_name = Label(text="Website :", bg=BLACK, fg=GRAY, font=FONT)
website_name.grid(row=1, column=0, pady=padding)

email_id = Label(text="Email/Username :", bg=BLACK, fg=GRAY, font=FONT)
email_id.grid(row=2, column=0, pady=padding)

password = Label(text="Password :", bg=BLACK, fg=GRAY, font=FONT)
password.grid(row=3, column=0, pady=padding)

# Entries

website_entry = Entry(font=FONT)
website_entry.grid(row=1, column=1, columnspan=1, sticky="EW", ipady=5, pady=padding)
website_entry.focus()

email_entry = Entry(font=FONT)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW", ipady=5, pady=padding)
email_entry.insert(0, "devadigaajay1729@gmail.com")

password_entry = Entry(font=FONT)
password_entry.grid(row=3, column=1, sticky="EW", ipady=5, pady=padding, padx=padding)

# Buttons

generate_password = Button(text="Generate Password", bg="#FFFFFF", font=FONT, command=generate_random_password)
generate_password.grid(row=3, column=2, ipady=1, pady=padding)

add_button = Button(text="Add", width=35, bg="#FFFFFF", font=FONT, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW", ipady=1)

search_button = Button(text="Search", width=15, bg="#FFFFFF", font=FONT, command=search_password)
search_button.grid(row=1, column=2, ipady=1, pady=padding, sticky="E")
window.mainloop()
