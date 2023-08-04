# import customtkinter as ctk
# import requests
# ctk.set_appearance_mode("System")

# # Supported themes : green, dark-blue, blue
# ctk.set_default_color_theme("green")

# def send_post_request():
#     url = 'http://127.0.0.1:5000/send_data'
#     data = {'input': entry.get()}
#     response = requests.post(url, data=data)
#     print(response.text)

# def send_get_request():
#     url = 'http://127.0.0.1:5000/send_sent_data'
#     response = requests.get(url)
#     label.configure(text=response.text)

# root = ctk.CTk()

# root.geometry('500x500')

# entry = ctk.CTkEntry(root,placeholder_text='ASK ME TO ANSWER')
# entry.pack(pady=10)

# post_button = ctk.CTkButton(root, text='Send To AI', command=send_post_request)
# post_button.pack(pady=10)

# get_button = ctk.CTkButton(root, text='Get The Answer', command=send_get_request)
# get_button.pack(pady=10)

# label = ctk.CTkLabel(root)
# label.pack(pady=10)
# root.mainloop()
# ############################################################################ any user
"""
import customtkinter as ctk
import requests

USER_ID = 'user1'

def send_post_request():
    url = 'http://127.0.0.1:1234/send_data'
    data = {'input': entry.get(), 'user_id': USER_ID}
    response = requests.post(url, data=data)
    print(response.text)

def send_get_request():
    url = 'http://127.0.0.1:1234/get_sent_data'
    params = {'user_id': USER_ID}
    response = requests.get(url, params=params)
    label.configure(text=response.text)

root = ctk.CTk()

entry = ctk.CTkEntry(root)
entry.pack(pady=10)

post_button = ctk.CTkButton(root, text='Send POST Request', command=send_post_request)
post_button.pack(pady=10)

get_button = ctk.CTkButton(root, text='Send GET Request', command=send_get_request)
get_button.pack(pady=10)

label = ctk.CTkLabel(root)
label.pack(pady=10)

root.mainloop()
"""################################################################ with password
import customtkinter as ctk
import requests
ctk.set_appearance_mode("System")

ctk.set_default_color_theme("green")
api_key = ''
def login():
    url = api_key +'/login'
    data = {'username': username_entry.get(), 'password': password_entry.get()}
    response = requests.post(url, data=data)
    if response.text == 'Login successful':
        login_frame.pack_forget()
        main_frame.pack()
    else:
        print(response.text)

def send_post_request():
    url = api_key+'/send_data'
    data = {'input': entry.get(), 'user_id': username_entry.get()}
    response = requests.post(url, data=data)
    print(response.text)

def send_get_request():
    url = api_key+'/get_sent_data'
    params = {'user_id': username_entry.get()}
    response = requests.get(url, params=params)
    label.configure(text=response.text)

root = ctk.CTk()

login_frame = ctk.CTkFrame(root)

username_label = ctk.CTkLabel(login_frame, text='Username:')
# username_label.pack(pady=10)

username_entry = ctk.CTkEntry(login_frame)
# username_entry.pack(pady=10)

password_label = ctk.CTkLabel(login_frame, text='Password:')
# password_label.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, show='*')
# password_entry.pack(pady=10)

login_button = ctk.CTkButton(login_frame, text='Login', command=login)
# login_button.pack(pady=10)

# login_frame.pack()

main_frame = ctk.CTkFrame(root)

entry = ctk.CTkEntry(main_frame)
# entry.pack(pady=10)

post_button = ctk.CTkButton(main_frame, text='Send POST Request', command=send_post_request)
# post_button.pack(pady=10)

get_button = ctk.CTkButton(main_frame, text='Send GET Request', command=send_get_request)
# get_button.pack(pady=10)

label = ctk.CTkLabel(main_frame)
# label.pack(pady=10)

# root.mainloop()
def AI():
    root.geometry('500x500')
    username_label.pack(pady=10)
    username_entry.pack(pady=10)
    password_label.pack(pady=10)
    password_entry.pack(pady=10)
    login_button.pack(pady=10)
    login_frame.pack()
    entry.pack(pady=10)
    post_button.pack(pady=10)
    get_button.pack(pady=10)
    label.pack(pady=10)
    root.mainloop()








