import sqlite3
import datetime


from tabulate import tabulate

conn = sqlite3.connect("todo.db")
cur = conn.cursor()

now  = datetime.datetime.now()

current_time :str = str(now.strftime("%Y %M %D %H %M %S"))

class TodoInterface:

    def __init__(self):
        self.choice = ""

    def display(self):
        interface = """
                TODO APPLICATION
                
            1.Create an event 
            2.Open an event
            3.Delete event
            4.Exit            

                    """
        print(interface)
        self.choice = input("\t\tEnter choice (1-4): ")

    # create a table in the database and update the events table
    def create_event(self) -> str:
        event_name: str = input("Enter Event Name: ").strip()
        query1 = (f"CREATE TABLE IF NOT EXISTS {event_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                  f"tasks VARCHAR,status VARCHAR,time_taken CURRENT_TIME)"
                  )

        cur.execute(query1)
        conn.commit()

        return event_name

    def update_event_table(self, event: str):

        cur.execute(f"INSERT INTO event_table VALUES (?)", (event,))
        conn.commit()

        print("Event created successfully!")

    def open_event(self) -> str | None:
        event_name: str = input("Enter Event name: ").strip()
        query_events = "SELECT * FROM event_table"

        cur.execute(query_events)

        row = cur.fetchall()

        for events in row:
            if event_name not in events:
                return None

            return event_name

    def delete_event(self):
        event_name: str = input("Enter Name of Event you want to delete: ").strip()


        search_query = f"SELECT event_name FROM event_table WHERE event_name = ?"
        cur.execute(search_query,(event_name,))

        row = cur.fetchone()

        if row:
            try:
                cur.execute(f"DELETE FROM event_table WHERE event_name  = ?",(event_name,))
                conn.commit()
                print("Deleted Successfully")
            except Exception as e:
                print(e)
        else:
            print("Invalid event name")


todo_interface = TodoInterface()


class TodoCommands:

    def __init__(self):
        self.commands: list[str] = ["--add", "--del", "--quit", "--view", "--done", "--back","--help"]

    def add_to_events(self, event_name: str, tasks: str):

        cur.execute(f"INSERT INTO {event_name} (tasks,status,time_taken) VALUES (?,?,?)",
                    (tasks, "✖",current_time))

        conn.commit()

        print("Tasks Added")

    def read_from_list(self, event_name: str):
        view_query = f"SELECT * FROM {event_name}"

        cur.execute(view_query)
        row = cur.fetchall()
    

        first_row = ["ID", "TASK", "STATUS", "TIME"]
        data: list = []
        for tasks in row:
            data .append([tasks[0],tasks[1],tasks[2],tasks[3]])
                
                    
        table = tabulate(data,headers=first_row,tablefmt="grid")

        print(table)
    def delete_from_list(self, event_name: str, id: int) -> None:

        if isinstance(id, int):

            try:
                cur.execute(f"DELETE  FROM {event_name} WHERE id = ?",(id,))
                conn.commit()
            except Exception as e:
                print(f"Error: {e}")

            print("Deleted")
        else:
            print("Unable to Delete")

    def update_completed_tasks(self, event_name: str, id: int):
        if isinstance(id, int):

            cur.execute(f"UPDATE {event_name} SET status = ?,time_taken = ? WHERE id = ?",
                        ("✔", current_time,id))
            conn.commit()



        else:
            print("Can't update")

    def run_program(self):
        while True:
            todo_interface.display()
            if todo_interface.choice == "1":
                event_name = todo_interface.create_event()
                todo_interface.update_event_table(event_name)
                while True:
                    self.compute_command(event_name)
            elif todo_interface.choice == "2":
                event_name = todo_interface.open_event()

                if event_name is None:
                    print("Event name doesn't exist")
                else:
                    while True:
                        self.compute_command(event_name)

            elif todo_interface.choice == "3":
                todo_interface.delete_event()
            elif todo_interface.choice == "4":
                quit()
            else:
                print("Invalid input ")
            self.resume = input("Do you want to continue? (y/n)").lower()

            if self.resume != "y":
                break

    def get_commands(self):
        cmd: str = input("").lower()


        return cmd.strip()

    def help(self):
        help_list = """
        Available commands
          --add  add to list
          --view open todo list
          --del delete from to do list
          --back Navigate back to main menu
          --quit Exit the program
          --done Update an existing as completed
          --help Open help list
          """
        print(help_list)
    def compute_command(self, event_name: str):

        cmd = self.get_commands()


        cmd1, cmd2, cmd3, cmd4 = cmd[0:5], cmd[1:6], cmd[0:6],cmd[1:]
        tasks1, tasks2, task3, tasks4 = cmd[5::], cmd[0], cmd[6::], cmd[0]

        if cmd1 == self.commands[0]:
            self.add_to_events(event_name, tasks1)
        elif cmd2 == self.commands[1]:
            id = int(tasks2.strip())
            self.delete_from_list(event_name, id)
        elif cmd3 == self.commands[2]:
            quit()
        elif cmd3 == self.commands[3]:
            self.read_from_list(event_name)
        elif cmd4 == self.commands[4]:
            id = int(tasks4)
            self.update_completed_tasks(event_name, id)
        elif cmd3 == self.commands[5]:
            self.run_program()

        elif cmd == self.commands[6]:
            self.help()
        else:
            print("Invalid command")


def main() -> None:
    todo_app = TodoCommands()
    todo_app.run_program()


if __name__ == '__main__':
    main()

