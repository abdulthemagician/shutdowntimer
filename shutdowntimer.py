import tkinter

root = tkinter.Tk()

#Window configuration
win_width = 400
win_height = 400

#Screen resolution
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Center position of window
x = (screen_width // 2) - (win_width // 2)
y = (screen_height // 2) - (win_height // 2)


root.title("Shutdown Timer")
print(screen_width, " : ", screen_height)

root.geometry(f"{win_width}x{win_height}+{x}+{y}")
root.mainloop()