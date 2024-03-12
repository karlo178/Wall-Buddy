import sqlite3

class TaskDatabase:
    def __init__(self, db_file="tasks.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()
        self.fetch_all_tasks_sorted_by_priority()

    def delete_task(self, index_to_delete):
        try:
            query = '''DELETE FROM tasks WHERE id=?'''
            with self.conn:
                self.conn.execute(query, (index_to_delete,)) #Tuple can prevent sql injection this means that the values provided in the tuple are treated as data, not as part of the SQL query, preventing any potential SQL injection
                
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            priority INTEGER,
            budget INTEGER,
            deadline DATE,
            days_remaining INTEGER
        );
        '''
        with self.conn:
            self.conn.execute(query)
            

    def insert_task(self, task, priority, budget, deadline, days_remaining):
        query = "INSERT INTO tasks (task, priority, budget, deadline, days_remaining) VALUES (  ?, ?, ?, ?, ?)"
        with self.conn:
            self.conn.execute(query, (task, priority, budget, deadline, days_remaining))

    def calculate_budget_summary(self):
        try:
            query = "SELECT SUM(budget) FROM tasks"
            cursor = self.conn.execute(query)
            total_budget = cursor.fetchone()[0]  # Retrieve the sum from the query result
            return total_budget
        except Exception as e:
            print(f"Error calculating budget summary: {e}")
            return None
    
    def task_name_to_index(self, search_task):
        try:
            query = "SELECT rowid, task FROM tasks WHERE task LIKE ?"
            
            with self.conn as conn:
                cursor = conn.execute(query, ('%' + search_task + '%',))
                result = cursor.fetchall()

            if result:
                for row in result:
                    index, task = row
                    print(f"Index: {index}, Task: {task}")
                    
            return int(index)

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def budget_update(self, task_to_update, new_budget):
        try:
            select_query = "SELECT rowid, task, budget FROM tasks WHERE task = ?"
            cursor = self.conn.execute(select_query, (task_to_update,))
            selected_record = cursor.fetchone()

            if selected_record:
                update_query = "UPDATE tasks SET budget = ? WHERE rowid = ?"
                self.conn.execute(update_query, (new_budget, selected_record[0]))

                self.conn.commit()
                print("Budget updated successfully.")
            else:
                print("Task not found.")
        except Exception as e:
            print(f"Error: {e}")

    def fetch_all_tasks_sorted_by_priority(self):
        try:
            query = "SELECT * FROM tasks ORDER BY priority DESC"
            
            cursor = self.conn.execute(query)
            return cursor.fetchall()
        
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return None


