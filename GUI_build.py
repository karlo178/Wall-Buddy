import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from database import TaskDatabase
from datetime import datetime

class ModernGUI:
    def __init__(self, root, task_database):
        self.root = root
        self.root.title("Modern GUI with Table")
        self.task_database = task_database

        
        self.root.attributes('-fullscreen', True)

        canvas = tk.Canvas(self.root, bg="#333333", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Ot taki se gradient
        for i in range(30):
            color = "#{:02x}{:02x}{:02x}".format(51 + i * 2, 51 + i * 2, 51 + i * 2)
            canvas.create_rectangle(0, i * 60, self.root.winfo_screenwidth(), (i + 1) * 60, fill=color, width=0)

        style = ThemedStyle(self.root)
        style.set_theme("equilux")  

        
        columns = ("#", "Task", "Priority", "Budget", "Deadline", "Days Remaining")
        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            style="Treeview",
            height=20,  #number of visible rows
            selectmode="none",  # Disable row selection
        )

        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300) 


        # Move the treeview widget almost to the top of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        table_width = len(columns) * 300
        y_position = 30  # Set to a smaller value to move the table almost to the top

        x_position = (screen_width - table_width) // 2
        self.tree.place(x=x_position, y=y_position)

    def get_budget_summary(self):
            total_budget = self.task_database.calculate_budget_summary()
            if total_budget is not None:
                label_text = f"Total budget: {total_budget}"
                label = tk.Label(self.root, text=label_text, font=("Arial", 12), bg="#333333", fg="white")
                label.place(relx=0.5, rely=0.95, anchor="center")
                print(f"Total budget: {total_budget}")
            else:
                print("Error calculating budget summary.")


if __name__ == "__main__":
    root = tk.Tk()
    task_database = TaskDatabase()  
    app = ModernGUI(root, task_database)
    app.get_budget_summary()
    root.mainloop()
