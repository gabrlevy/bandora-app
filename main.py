import math
from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    global timer
    if timer:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")
        timer_label.config(text="Bandora Timer")
        checks.config(text="")
        completed_sessions.config(text="")
        pause_button.config(text="Pause")
        global reps
        reps = 0
        timer = None

# ---------------------------- UPDATE SESSIONS MECHANISM ------------------------------- #
def update_sessions(reps):
    mark = ""
    sessions = "completed sessions:"
    long_break = math.floor(reps / 8)
    for _ in range(long_break):
        sessions += " | "
    completed_sessions.config(text=sessions)
    work_sessions = math.floor(reps / 2)
    for _ in range(work_sessions):
        mark += "✔"
        checks.config(text=mark)

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    update_sessions(reps)

    if reps % 2 != 0:
        timer_label.config(text="Work!", fg=GREEN)
        count_down(work_sec)
    elif reps % 8 == 0:
        timer_label.config(text="Take a long break", fg=RED)
        count_down(long_break_sec)
    else:
        timer_label.config(text="Small break", fg=PINK)
        count_down(short_break_sec)

# ------------------------------- PAUSE MECHANISM --------------------------------- #

def pause_timer():
    global timer
    if timer is None:
        return
    if pause_button.cget('text') == "Pause":
        window.after_cancel(timer)
        pause_button.config(text="Resume")
    else:
        current_time = canvas.itemcget(timer_text, "text")
        current_min = int(current_time[:2])
        current_sec = int(current_time[3:])
        remaining_time = current_min * 60 + current_sec
        timer = window.after(0, count_down, remaining_time)
        pause_button.config(text="Pause")



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    """
    counts down the time
    Parameters:
    count (int): remaining time in seconds
    """
    global timer
    count_min = math.floor(count / 60)
    count_min = "{:02d}".format(count_min)
    count_sec = count % 60
    count_sec = "{:02d}".format(count_sec)

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count >= 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Bandora Timer")
window.config(padx=50, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


timer_label = Label(text="Bandora Timer", font=(FONT_NAME, 30, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=1, row=0)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

pause_button = Button(text="Pause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=1, row=5)

checks = Label(bg=YELLOW, fg=GREEN)
checks.grid(column=1, row=3)

completed_sessions = Label(bg=YELLOW, fg=GREEN)
completed_sessions.grid(column=1, row=4)

window.mainloop()
