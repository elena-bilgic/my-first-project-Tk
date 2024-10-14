import tkinter as tk

def display_greeting():
    name = entry.get()
    label.config(text="Hello, " + name + "!")

root = tk.Tk()
root.title("The greeting")

label = tk.Label(root,text="Input your name")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Push for greeting", command=display_greeting)
button.pack(pady=10)

root.mainloop()

