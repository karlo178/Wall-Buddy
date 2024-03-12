import tkinter as tk #library for gui
import re #regular expressions are powerful tools for pattern matching and text manipulation
import threading # Threads can be used to perform multiple tasks simultaneously, allowing for more efficient execution of programs
from datetime import datetime 
from Azure_STT_TTS_API import text_to_speech, speech_to_text # import from other file 
from queue import Queue #data structure that follows FIFO principle 
from GUI_build import ModernGUI #imports from other files
from database import TaskDatabase
 

class TaskManager:

    def __init__(self, root, modern_gui): #initialize all needed stuff
        self.listen_active = True
        self.root = root
        self.modern_gui = modern_gui
        self.year, self.month, self.day = 0, 0, 0
        self.queue = Queue()  # queue for communication between threads
        self.listen_thread = threading.Thread(target=self.listen_for_trigger)
        self.listen_thread.start()
        self.task_database = TaskDatabase()
        self.display_database_data()
        
    def check_queue(self): 
        try:
            while True:
                action = self.queue.get_nowait()
                self.handle_user_input(action)
                self.display_database_data()
        except Exception as e:
            print(f"Error ocured: {e}")
        self.root.after(10, self.check_queue)  # Schedule the next check

    def convert_text_to_numbers(self, year_entry, month_entry, day_entry): #process of converting raw data into a format that is more suitable for analysis
        try:
            str_year = year_entry.rstrip('.')
            str_month = month_entry.rstrip('.')
            str_day = day_entry.rstrip('.')

            year = int(str_year)
            month = int(str_month)
            day = int(str_day)

            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("Invalid month or day")

            return year, month, day

        except ValueError as e:
            print(f"Conversion error: {e}")
            return None

    def display_database_data(self):
        try:

            self.modern_gui.tree.delete(*self.modern_gui.tree.get_children())
            data = self.task_database.fetch_all_tasks_sorted_by_priority()
            print("Retrieved data from database:", data)
            for row in data:
                self.modern_gui.tree.insert('', 'end', values = row)
            
            self.modern_gui.tree.update()
        except Exception as e:
            print(f"Error in display_database_data: {e}")
    
    def data_add_row(self):
        try:
            #ZDJAC KOMENTARZ DO URUCHOMIENIA MOWY
            task = self.take_user_input("Please say your task")
            text_to_speech(f"You said {task}.")

            priority = self.take_user_input("Please provide the priority from 1 to 10")
            text_to_speech(f"You said {priority}.")

            budget = self.take_user_input("Please provide the budget")
            text_to_speech(f"You said {budget}.")

            year_entry = self.take_user_input("Please provide deadline year")
            text_to_speech(f"You said {year_entry}.")
            print(year_entry)

            month_entry = self.take_user_input("month")
            text_to_speech(f"You said {month_entry}.")
            print(month_entry)

            day_entry = self.take_user_input("day")
            text_to_speech(f"You said {day_entry}.")
            print(day_entry)
            print(year_entry, month_entry, day_entry)
            text_to_speech(f"You said {year_entry}, {month_entry}, {day_entry}.")

            self.add_row(task, priority, budget, year_entry, month_entry, day_entry)
            deadline = (year_entry, month_entry, day_entry)
            print("Inserting into database:", task, priority, budget, deadline)
            self.task_database.insert_task(task, priority, budget, deadline)
            print("Displaying data in the GUI...")
            self.display_database_data()

            
            # task = input("Please enter your task: ")
            # priority = input("Please provide the priority from 1 to 10: ")
            # budget = input("Please provide the budget: ")
            # year_entry = input("Please provide the deadline year: ")
            # month_entry = input("Please provide the month: ")
            # day_entry = input("Please provide the day: ")

            self.add_row(task, priority, budget, year_entry, month_entry, day_entry)
        except Exception as e:
            print(f"Error in data_add_row: {e}")

    def add_row(self, task, priority, budget, year_entry, month_entry, day_entry):
        print("Adding a row to the GUI...")
        while True:
            converted_values = self.convert_text_to_numbers(year_entry, month_entry, day_entry)
            if converted_values:
                year, month, day = converted_values
                try:
                    target_date = datetime(year, month, day)
                    today = datetime.now()
                    entry4 = target_date
                    remaining_time = target_date - today
                    result = remaining_time.days
                    self.task_database.insert_task(task, priority, budget, entry4, result)
                    self.display_database_data()
                    break  # exit the loop the date is valid
                except ValueError:
                    text_to_speech("Sorry, there was an error processing the date. Please try again.")
                    # check which part of the date caused the error and re-prompt only for that
                    if not isinstance(year, int):
                        year_entry = self.take_user_input("Please provide a valid deadline year")
                        text_to_speech(f"You said {year_entry}.")
                    elif not 1 <= month <= 12:
                        month_entry = self.take_user_input("Please provide a valid deadline month")
                        text_to_speech(f"You said {month_entry}.")
                    elif not 1 <= day <= 31:
                        day_entry = self.take_user_input("Please provide a valid deadline day")
                        text_to_speech(f"You said {day_entry}.")
            else:
                text_to_speech("Sorry, I couldn't understand the date. Please try again.")
                # Promp to enter the date again
                year_entry = self.take_user_input("Please provide deadline year")
                text_to_speech(f"You said {year_entry}.")
                month_entry = self.take_user_input("month")
                text_to_speech(f"You said {month_entry}.")
                day_entry = self.take_user_input("day")
                text_to_speech(f"You said {day_entry}.")

    def delete_task(self):
        # Ask the user for the task index to delete
        index_to_delete = self.take_user_input("Wich task do you to delete?")
        #index_to_delete = input("Enter the index of the task you want to delete: ")

        try:
            if not re.search(r"^\d+$",index_to_delete):
                index_to_delete = task_database.task_name_to_index(index_to_delete)
                
                success = self.task_database.delete_task(index_to_delete)

            else:
                print(f"Test")
                index_to_delete = int(index_to_delete)

                # Confirm with the user before deletion
            confirmation = self.take_user_input(f"Are you sure you want to delete task at index {index_to_delete}? (yes/no): ")

            if confirmation.lower() == 'yes':
                # Delete the task from the database
                success = self.task_database.delete_task(index_to_delete)

                if success:
                    print(f"Task at index {index_to_delete} deleted successfully.")
                    self.display_database_data()
                else:
                    print(f"Error: Unable to delete task at index {index_to_delete}.")
            else:
                print("Deletion canceled.")
        except ValueError:
            print("Error: Please enter a valid index.")

    def change_budget(self):
        try:
            task_to_update = input("task with budget to update")
            new_budget = input("pass new budget")
            task_database.budget_update(task_to_update, new_budget)
        except ValueError:
            print("Invalid input. Please enter a valid number for the new budget.")

        



    # ZDJAC KOMENTARZ DO URUCHOMIENIA MOWY
    def take_user_input(self, prompt):
        text_to_speech(prompt)
        user_input = speech_to_text()
        print("User input (from take_user_input):", user_input)
        return user_input

    # ZAKOMENTOWAC DO URUCHOMIENIA MOWY            
    # def take_user_input(self, prompt):
    #     user_input = input(prompt)  # Use input() to get user input
    #     print(f"User input: {user_input}")
    #     return user_input


   
         
    
    def listen_for_trigger(self):


        while self.listen_active:
            trigger_phrase = speech_to_text()
            if trigger_phrase and "Hi, Buddy." in trigger_phrase:
                action = self.take_user_input("Hi")
                text_to_speech(f"You said {action}.")
                print("User input:", action)
                self.queue.put(action)
                #time.sleep(1)  # Adjust as needed to prevent excess CPU usage

    # def stop_listening(self):
    #     self.listen_active = False

    # def resume_listening(self):
    #     self.listen_active = True

    
    # # ZAKOMENTOWAC DO URUCHOMIENIA MOWY
    # # Test object to trigger for testing 
    # def invoke_data_add_row(self):
    #     # Stop the listening loop to allow manual input
    #     self.listen_active = True

    # #     # Invoke the data_add_row method directly
        
    # #     #self.data_add_row()
    # #     self.change_budget( )


    # #     # Restart the listening loop after manual input
    # #     self.root.destroy()
    

    def handle_user_input(self, action):
        if action.lower() == "help.":
            print("Entered 'help' branch")
            text_to_speech("My name is WallBuddy. You can ask me to add a new task to your planner by saying 'add task' or get the weather in your current location by saying 'get weather'.")
            choice = self.take_user_input("Now tell me, what should I do?")

            # if choice.lower() == "get weather.":
            #     print("Entered 'cloud' branch")
            #    self.data_weather()
            if choice.lower() == "add task.":
                print("Entered 'one' branch")
                self.data_add_row()
            else:
                print("Entered 'else' branch")
                text_to_speech("I'm sorry, I didn't understand that. Please try again.")
        # elif action.lower() == "get weather.":
        #     print("Entered 'get weather' branch")
        #     self.data_weather()
        elif action.lower() == "delete task.":
            print("Entered 'delete_task' branch")
            self.delete_task()
        elif action.lower() == "add task.":
            print("Entered 'add row' branch")
            self.data_add_row()
        else:
            print("Entered 'else' branch")
            text_to_speech("I'm sorry, I didn't understand that. Please try again.")
        
    

if __name__ == "__main__":
    task_database = TaskDatabase()
    root = tk.Tk()  
    modern_gui = ModernGUI(root, task_database)
    modern_gui.get_budget_summary()
    task_manager = TaskManager(root, modern_gui)
    #task_manager.invoke_data_add_row()  
    task_manager.check_queue()  # Start checking the queue
    root.mainloop()
    
  


    
    




