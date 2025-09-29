import tkinter as tk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--vfs_path', default='/default/vfs', help='Путь к VFS')
parser.add_argument('--prompt', default='vfs:~# ', help='Пользовательское приглашение')
parser.add_argument('--startup_script', default=None, help='Путь к стартовому скрипту')
args = parser.parse_args()

print(f"VFS path: {args.vfs_path}")
print(f"Prompt: {args.prompt}")
print(f"Startup script: {args.startup_script}")

def execute(command_line):
    parts = command_line.split()
    if not parts:
        return ""
    cmd = parts[0]
    args_str = " ".join(parts[1:])
    if cmd == 'ls':
        return f"ls {args_str}"
    elif cmd == 'cd':
        return f"cd {args_str}"
    elif cmd == 'exit':
        root.quit()
        return ""
    else:
        return f"{cmd}: command not found"

root = tk.Tk()
root.title("VFS")
root.geometry('1111x777')
root.configure(bg='black')

welcome_text = """
Welcome to VFS Emulator

"""

label = tk.Label(
    root,
    text=welcome_text,
    font=("Courier", 14),
    fg="white",
    bg="black",
    justify="left",
    anchor="nw",
    padx=10,
    pady=10
)
label.pack(fill='both', expand=True)

text = tk.Text(
    root,
    font=("Courier", 14),
    fg="white",
    bg="black",
    insertbackground="green",
    borderwidth=0,
    highlightthickness=0,
    height=1,
    wrap="none"
)
text.pack(fill="x", padx=10, pady=5)

prompt = args.prompt
text.insert("end", prompt)
text.focus()

def protect_prompt(event):
    if text.index("insert") <= f"1.{len(prompt)}":
        return "break"

def handle_input(event):
    command_line = text.get(f"1.{len(prompt)}", "end-1c").strip()
    if command_line:
        output = execute(command_line)
        label.config(text=label.cget("text") + f"{prompt}{command_line}\n{output}\n")
        text.delete("1.0", "end")
        text.insert("end", prompt)

text.bind("<BackSpace>", protect_prompt)
text.bind("<Left>", protect_prompt)
text.bind("<Return>", handle_input)

if args.startup_script:
    try:
        with open(args.startup_script, 'r') as f:
            for line in f:
                command_line = line.strip()
                if command_line:
                    output = execute(command_line)
                    label.config(text=label.cget("text") + f"{prompt}{command_line}\n{output}\n")
    except:
        pass  

root.mainloop()