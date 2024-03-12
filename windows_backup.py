import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry
from datetime import datetime
#from voice_engine import init_voice, text_to_speech
#from mozilla_deep_speech import take_voice_input
from word2number import w2n
import wikipedia
import python_weather
import asyncio
import os
from wether_api import get_weather
from Azure_STT_TTS_API import text_to_speech, speech_to_text
import threading
from queue import Queue
from GUI_build import ModernGUI
from database import TaskDatabase


class ChooseActivity:
    pass  

class TaskManager:
    def __init__(self, root, modern_gui):
        self.root = root
        self.modern_gui = modern_gui
        self.year, self.month, self.day = 0, 0, 0
        self.queue = Queue()  # Queue for communication between threads
        self.listen_thread = threading.Thread(target=self.listen_for_trigger)
        self.listen_thread.start()
        self.task_database = TaskDatabase()
 
    def check_queue(self): 
        try:
            while True:
                action = self.queue.get_nowait()
                self.handle_user_input(action)
        except:
            pass
        self.root.after(10, self.check_queue)  # Schedule the next check

    def convert_text_to_numbers(self, year_entry, month_entry, day_entry):
        try:
            str_year = year_entry.rstrip('.')
            str_month = month_entry.rstrip('.')
            str_day = day_entry.rstrip('.')

            year = int(str_year)
            month = int(str_month)
            day = int(str_day)

            # Additional input validation if needed
            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("Invalid month or day")

            return year, month, day

        except ValueError as e:
            print(f"Conversion error: {e}")
            return None

        
    
        

    
    
    
    def data_add_row(self):
        #init_voice()

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
        self.task_database


    def add_row(self, task, priority, budget, year_entry, month_entry, day_entry):
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
                    data = (task, priority, budget, entry4, result)
                    modern_gui.tree.insert('', 'end', values=data)  
                    break  # Exit the loop if the date is valid
                except ValueError:
                    text_to_speech("Sorry, there was an error processing the date. Please try again.")
                    # Determine which part of the date caused the error and re-prompt only for that part
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
                # Prompt the user to enter the date again
                year_entry = self.take_user_input("Please provide deadline year")
                text_to_speech(f"You said {year_entry}.")
                month_entry = self.take_user_input("month")
                text_to_speech(f"You said {month_entry}.")
                day_entry = self.take_user_input("day")
                text_to_speech(f"You said {day_entry}.")


    # def data_weather(self):
    #     city = 'Krakow,pl'
    #     # Assuming you have a get_weather function in your 'wether_api' module
    #     weather_data = get_weather(city)
    #     if weather_data:
    #         print(f"Weather in {city}: {weather_data['description']}")
    #         print(f"Temperature: {weather_data['temperature']}°C")
    #         print(f"Humidity: {weather_data['humidity']}%")
    #     else:
    #         text_to_speech("Sorry, I couldn't retrieve the weather information.")

    def take_user_input(self, prompt):
        text_to_speech(prompt)
        user_input = speech_to_text()
        print("User input (from take_user_input):", user_input)
        return user_input

    # def main_loop(self):
    #     #init_voice()
         
    
    def listen_for_trigger(self):


        while True:
            trigger_phrase = speech_to_text()
            if trigger_phrase and "Hi, Buddy." in trigger_phrase:
                action = self.take_user_input("Hi")
                text_to_speech(f"You said {action}.")
                print("User input:", action)
                self.queue.put(action)
                #time.sleep(1)  # Adjust as needed to prevent excess CPU usage

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
        elif action.lower() == "add task.":
            print("Entered 'add row' branch")
            self.data_add_row()
        else:
            print("Entered 'else' branch")
            text_to_speech("I'm sorry, I didn't understand that. Please try again.")
        
    

if __name__ == "__main__":
    root = tk.Tk()
    modern_gui = ModernGUI(root)
    task_manager = TaskManager(root, modern_gui)
    task_manager.check_queue()  # Start checking the queue
    root.mainloop()
    
  


    
    




