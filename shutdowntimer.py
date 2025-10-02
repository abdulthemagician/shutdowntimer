import tkinter

main = tkinter.Tk()

#Window configuration
win_width = 400
win_height = 400

#Screen resolution
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

#Center position of window
x = (screen_width // 2) - (win_width // 2)
y = (screen_height // 2) - (win_height // 2)


main.title("Shutdown Timer")
print(screen_width, " : ", screen_height)

main.geometry(f"{win_width}x{win_height}+{x}+{y}")
main.mainloop()
