import tkinter as tk

def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)

def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_listbox.delete(selected_task)

def check_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_listbox.itemconfig(selected_task, bg="green")

root = tk.Tk()
root.title("Task list")
root.configure(background="DarkSlateBlue")

label1 = tk.Label(root, text="Input a task")
label1.pack(pady=10)

task_entry = tk.Entry(root, width=35, bg="DarkGrey")
task_entry.pack(pady=10)

add_task_button = tk.Button(root, text="Add a task", bg="LightSlateBlue", command=add_task)
add_task_button.pack(pady=10)

delete_task_button = tk.Button(root, text="Delete a task", bg="LightSlateBlue", command=delete_task)
delete_task_button.pack(pady=10)

check_task_button = tk.Button(root, text="Check a task", bg="LightSlateBlue", command=check_task)
check_task_button.pack(pady=10)

label2 = tk.Label(root, text="Uncompleted tasks:")
label2.pack(pady=10)

task_listbox = tk.Listbox(root, width=50, height=20, bg="GhostWhite")
task_listbox.pack(pady=10)



root.mainloop()



