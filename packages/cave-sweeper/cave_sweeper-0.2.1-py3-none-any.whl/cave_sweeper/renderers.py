import os
from tkinter import Tk, Label, ttk, StringVar, Frame, N, W, E, S
from cave_sweeper.field_slot import Field


def render_selection_window():
    def _render_minefield_window():
        os.environ["MINEFIELD_COLUMNS"] = cols_combo.get()
        os.environ["MINEFIELD_ROWS"] = rows_combo.get()
        os.environ["DIFFICULTY"] = difficulty.get()
        selection_window.destroy()
        render_minefield_window()

    selection_window = Tk()
    selection_window.title("Pick your settings")
    selection_frame = ttk.Frame(selection_window, padding="50 50 50 50")
    selection_frame.grid(column=0, row=0, sticky=(N, E, W, S))
    selection_window.columnconfigure(0, weight=1)
    selection_window.rowconfigure(0, weight=1)

    #ROW1
    rows_combo_label = ttk.Label(master=selection_frame, text="Rows: ")
    rows_combo_label.grid(row=1, column=1, sticky=W)

    rows_combo = ttk.Combobox(selection_frame, width=5)
    rows_combo['values'] = (10, 15, 20, 25)
    rows_combo.state(["readonly"])
    rows_combo.set(10)
    rows_combo.grid(row=1, column=2, sticky=E)

    #ROW 2
    cols_combo_label = ttk.Label(master=selection_frame, text="Cols: ")
    cols_combo_label.grid(row=2, column=1, sticky=W)

    cols_combo = ttk.Combobox(selection_frame, width=5)
    cols_combo['values'] = (10, 15, 20, 25)
    cols_combo.state(["readonly"])
    cols_combo.set(10)
    cols_combo.grid(row=2, column=2, sticky=E)

    #ROW 3
    difficulty = StringVar()
    difficulty.set("easy")

    rb_easy = ttk.Radiobutton(master=selection_frame, text="Easy", variable=difficulty, value="easy")
    rb_easy.grid(row=3, column=1, sticky=W)

    rb_hard = ttk.Radiobutton(master=selection_frame, text="Hard", variable=difficulty, value="hard")
    rb_hard.grid(row=3, column=2, sticky=E)

    #ROW 4
    btn_ok = ttk.Button(master=selection_frame, text="OK", width=4, command=_render_minefield_window)
    btn_ok.grid(row=4, column=1, sticky=W)

    btn_close = ttk.Button(master=selection_frame, text="Close", width=4, command=selection_window.quit)
    btn_close.grid(row=4, column=2, sticky=E)

    # adds extra spacing between widgets and the borders of 'selection_frame'
    for child in selection_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    selection_window.mainloop()


def render_minefield_window():
    MINEFIELD_COLUMNS = int(os.environ.get("MINEFIELD_COLUMNS", 8))
    MINEFIELD_ROWS = int(os.environ.get("MINEFIELD_ROWS", 8))
    countdown_time = MINEFIELD_COLUMNS * MINEFIELD_COLUMNS * 2

    root = Tk()
    # styling of the main app window
    root.title("Minefield")
    root.configure(bg="lightgray")

    # display
    display_frame = ttk.Frame(master=root, width=MINEFIELD_COLUMNS*48, height=100)
    display_frame.place(x=10, y=10)

    # label to display amount of fields remaining
    remaining_label = ttk.Label(master=display_frame, background="black", foreground="brown1")
    remaining_label.config(
        font=("consolas", 50),
        text=MINEFIELD_COLUMNS * MINEFIELD_ROWS
    )
    remaining_label.place(x=10, y=14)


    # label to display amount of mines
    mines_label = Label(master=display_frame, bg="dim gray")
    mines_label.config(
        font=("consolas", 50),
        width=2,
        height=1,
        fg="brown1",
    )
    mines_label.place(x=(MINEFIELD_COLUMNS*48 + 20)/2 - 50, y=14)

    # minefield
    mf_frame = Field(
        remaining_label=remaining_label,
        mines_label=mines_label,
        master=root, bg="gray38",
        width=MINEFIELD_COLUMNS*48,
        height=MINEFIELD_ROWS*38
    )
    mf_frame.place(x=10, y=120)

    for c in range(MINEFIELD_COLUMNS):
        for r in range(MINEFIELD_ROWS):
            new_field_btn_kwargs = {
                "column": c,
                "row": r,
                "bd": 0,
                "pady": 0,
                "padx": 0,
                "width": 2,
                "height": 2,
                "highlightbackground": "gray38"
            }
            mf_frame.add_button(**new_field_btn_kwargs)

    mf_frame.place_mines()

    # label to display countdown timer
    countdown_label = Label(master=display_frame, bg="dim gray")
    countdown_label.config(
        font=("consolas", 50),
        width=4,
        height=1,
        fg="brown1",
    )
    countdown_label.place(x=(MINEFIELD_COLUMNS * 48 + 20) - 160, y=14)

    def update_label():
        nonlocal countdown_time
        if countdown_time >= 0:
            countdown_label.config(text=str(countdown_time))
            countdown_time -= 1
            root.after(1000, update_label)
        else:
            mf_frame.game_over(timeout=True)
            pass

    root.after(1000, update_label)

    # renders the app window
    mine_btn_width, mine_btn_heigth = mf_frame.btn_size
    root.geometry(f"{MINEFIELD_COLUMNS*mine_btn_width + 20}x{MINEFIELD_ROWS*mine_btn_heigth + 130}")
    root.resizable(width=False, height=False)
    root.mainloop()