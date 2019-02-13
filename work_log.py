import datetime
import os
import re
import sqlite3
import sys
import time

from textwrap import dedent
from peewee import *


db = SqliteDatabase('work_log.db')


class Entry(Model):
    """ Creates new database entries."""
    employee = CharField(max_length=255, unique=False)
    date = DateTimeField()
    task = CharField(max_length=255, unique=False)
    duration = IntegerField()
    notes = CharField(max_length=255, unique=False)

    class Meta:
        database = db


def initialize():
    """Create database and table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    """ Clears screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """ Prints a menu choice and directs to corresponding function"""
    clear()
    print(dedent("""
        WORK log
        What would you like to do? Enter a, b or c.
        a) Add new entry
        b) Search in existing entries
        c) Quit program"""))
    choice = input("> ")

    if choice == "a":
        return add()
    elif choice == "b":
        return search()
    elif choice == "c":
        print("Thanks for using WORK LOG!")
        sys.exit()
    else:
        print("Please enter a, b or c.")
        time.sleep(3)
        return main()


def add():
    """ Takes input for new entry and passes to Entry class"""
    try:
        date = input(str("Enter date of the task, use DD/MM/YYYY: "))
        date_test = datetime.datetime.strptime(date, '%d/%m/%Y')
    except:
        print("Must be in correct DD/MM/YYYY format.")
        return add()
    while True:
        employee = input("Enter the employee name: ")
        try:
            if employee == "":
                raise ValueError("Please enter a valid string.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    while True:
        task = input("Enter the name of this task: ")
        try:
            if task == "":
                raise ValueError("Please enter a valid string.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    while True:
        duration = input("Enter the duration of this task in minutes: ")
        try:
            if not duration.isdigit():
                raise ValueError("Please enter a valid integer.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    notes = input("Enter any notes (optional): ")
    Entry.create(employee=employee, date=date, task=task, duration=duration, notes=notes)
    print("Saved successfully!")
    time.sleep(2)
    return main()


def search():
    """ Presents user with search menu and directs to corresponding function"""
    clear()
    print(dedent("""
        What do you want to search by? Enter a through e.
        a) Employee
        b) Date
        c) Time Spent
        d) Search Term
        e) Return to main menu
        """))
    choice = input("> ")

    if choice == "a":
        return search_employee()
    elif choice == "b":
        return search_date()
    elif choice == "c":
        return search_duration()
    elif choice == "d":
        return search_exact()
    elif choice == "e":
        return main()
    else:
        print("Please enter a valid choice")
        time.sleep(3)
        return search()


def view_entries(entries):
    """View entries searched for, prompt user for next step"""
    num_entries = len(entries)
    choice = None
    entry_count = 0
    while choice != "e" and choice != "d" and choice != "r":
        clear()
        print(f"Date: {entries[entry_count].date}")
        print(f"Employee: {entries[entry_count].employee}")
        print(f"Task: {entries[entry_count].task}")
        print(f"Duration: {entries[entry_count].duration}")
        print(f"Notes: {entries[entry_count].notes}")
        print("\n"+f"Entry {entry_count+1} of {num_entries} ")
        print("\n")

        if num_entries == 1:
            print(dedent("""
            Please make a selection:
            (e)dit (d)elete (r)eturn to menu
            """))
        else:
            if entry_count+1 == 1:
                print(dedent("""
                Please make a selection:
                (n)ext (e)dit (d)elete (r)eturn to menu
                """))
            elif entry_count+1 == num_entries:
                print(dedent("""
                Please make a selection:
                (p)revious (e)dit (d)elete (r)eturn to menu
                """))
            else:
                print(dedent("""
                Please make a selection:
                (p)revious (n)ext (e)dit (d)elete (r)eturn to menu
                """))
        entry = entries[entry_count]
        choice = input("> ")
        if choice == "p" and entry_count != 0:
            entry_count -= 1
        elif choice == "n" and entry_count+1 != num_entries:
            entry_count += 1
        elif choice == "e":
            return edit(entry)
        elif choice == "d":
            return delete(entry)
        elif choice == "r":
            return search()
        else:
            print("Please enter a valid choice.")
            time.sleep(3)
            return view_entries(entries)


def search_employee():
    """ Presents user with choice to search by name or see a list"""
    clear()
    print(dedent("""
        What do you want to do? Enter a or b.
        a) Input a name to search
        b) See a list of employees
        c) Return to search menu
        """))
    choice = input("> ")
    if choice == "a":
        return search_employee_name()
    elif choice == "b":
        return search_employee_list()
    elif choice == "c":
        return search()
    else:
        print("Please enter a valid choice")
        time.sleep(3)
        return search()


def search_employee_name():
    """Search entries by employee name"""
    employee = input("Employee: ")
    entries = Entry.select()
    entries = entries.where(Entry.employee.contains(employee))
    employee_list = []
    for entry in entries:
        if entry.employee not in employee_list:
            employee_list.append(entry.employee)
        else:
            pass
    return search_employee_list(employee_list)


def search_employee_list(employee_list=None):
    """ Returns list of employees"""
    if employee_list == None:
        entries = Entry.select()
        employee_list = []
        for entry in entries:
            if entry.employee not in employee_list:
                employee_list.append(entry.employee)
            else:
                pass
    if len(employee_list) > 1:
        print("Multiple employees found, choose one by number:")
        for person in employee_list:
            print(f"{employee_list.index(person)}) {person}")

        while True:
            choice = input("> ")
            try:
                if not choice.isdigit():
                    raise ValueError("Please enter a valid integer.")
                choice = int(choice)
                if choice > (len(employee_list) - 1):
                    raise ValueError("Please enter a valid integer.")
                elif choice < 0:
                    raise ValueError("Please enter a valid integer.")
            except ValueError as err:
                    print(f"Whoops! {err}")
            else:
                break
        employee = employee_list[choice]
        entries = Entry.select()
        entries = entries.where(Entry.employee == employee)
    if entries:
        return view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)
        return search()


def search_date():
    """ Presents user with choice to search by list of dates or range"""
    clear()
    print(dedent("""
        What do you want to do? Enter a or b.
        a) Choose from a list of dates
        b) Search by a date range
        c) Return to search menu
        """))
    choice = input("> ")
    if choice == "a":
        return search_date_list()
    elif choice == "b":
        return search_date_range()
    elif choice == "c":
        return search()
    else:
        print("Please enter a valid choice")
        time.sleep(3)
        return search()

def search_date_list():
    """ Gives list of dates to search by """
    entries = Entry.select()
    date_list = []
    for entry in entries:
        if entry.date not in date_list:
            date_list.append(entry.date)
        else:
            pass
    if len(date_list) > 1:
        print("Multiple dates found, choose one by number:")
        for date in date_list:
            print(f"{date_list.index(date)}) {date}")
        while True:
            choice = input("> ")
            try:
                if not choice.isdigit():
                    raise ValueError("Please enter a valid integer.")
                choice = int(choice)
                if choice > (len(date_list) - 1):
                    raise ValueError("Please enter a valid integer.")
                elif choice < 0:
                    raise ValueError("Please enter a valid integer.")
            except ValueError as err:
                    print(f"Whoops! {err}")
            else:
                break
        date = date_list[choice]
        entries = Entry.select()
        entries = entries.where(Entry.date == date)
    if entries:
        return view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)
        return search()


def search_date_range():
    """ Searches for entries given date range."""
    start_date = input("Enter beginning date to search (DD/MM/YYYY): ")
    end_date = input("Enter end date to search (DD/MM/YYYY): ")
    try:
        start_date_test = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        end_date_test = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    except:
        print("Must be in correct DD/MM/YYYY format.")
        return search_date_range()

    entries = Entry.select()
    entries = entries.where(
            (Entry.date >= start_date) &
            (Entry.date <= end_date))
    if entries:
        return view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)
        return search()


def search_duration():
    """ Searches for entries given duration. Returns a list of results """
    while True:
        duration = input("Time Spent: ")
        try:
            if not duration.isdigit():
                raise ValueError("Please enter a valid integer.")
        except ValueError as err:
                print(f"Whoops! {err}")
        else:
            break
    entries = Entry.select()
    entries = entries.where(Entry.duration == duration)
    if entries:
        return view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)
        return search()


def search_exact():
    """ Searches for entries given any string. Returns a list of results """
    exact_string = input("Enter string to search for: ")
    entries = Entry.select()
    entries = entries.where(
            (Entry.task.contains(exact_string)) |
            (Entry.notes.contains(exact_string)))
    if entries:
        return view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)
        return search()


def delete(entry):
    """ Deletes entry in database """
    entry.delete_instance()
    print("Entry deleted!")
    time.sleep(2)
    return main()

def edit(entry):
    """ Prompts user what part of the entry to edit, edits database """
    print(dedent(f"""
    Which field would you like to edit?
    (D)ate, (E)mployee, (T)ask, D(u)ration, (N)otes
    """))
    choice = input("> ").upper()
    if choice == "D":
        while True:
            edit_val = input("Enter new value: ")
            try:
                edit_val = datetime.datetime.strptime(edit_val,
                '%d/%m/%Y')
                edit_val = edit_val.strftime("%d/%m/%Y")
            except:
                print("Must be in correct DD/MM/YYYY format.")
            else:
                break
        entry.date = edit_val
        entry.save()
    elif choice == "E":
        edit_val = input("Enter new value: ")
        entry.employee = edit_val
        entry.save()
    elif choice == "T":
        edit_val = input("Enter new value: ")
        entry.task = edit_val
        entry.save()
    elif choice == "U":
        while True:
            edit_val = input("Enter new value: ")
            try:
                if not edit_val.isdigit():
                    raise ValueError(
                    "Please enter a valid integer.")
            except ValueError as err:
                    print(f"Whoops! {err}")
            else:
                break
        entry.duration = edit_val
        entry.save()
    elif choice == "N":
        edit_val = input("Enter new value: ")
        entry.notes = edit_val
        entry.save()
    else:
        print("Please enter a valid choice.")
        time.sleep(1)
        return edit(entry)
    print("Entry updated!")
    time.sleep(2)
    return search()


if __name__ == '__main__':
    initialize()
    main()
