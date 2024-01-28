import tkinter as tk
from bowling_ui import BowlingUI


def main():
    root = tk.Tk()
    root.title("Bowling Score Calculator")
    app = BowlingUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
