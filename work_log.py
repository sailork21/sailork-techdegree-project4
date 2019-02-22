import datetime
import os
import re
import sqlite3
import sys
import time

from textwrap import dedent
from peewee import *

import menus


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


def get_date(error=None):
    """ Prompts user for date and returns"""
    while True:
        if error:
            print(error)
        date = input(str("Enter date, use DD/MM/YYYY: "))
        try:
            date_test = datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            error = "Must be in correct DD/MM/YYYY format."
        else:
            return date


def get_employee(error=None):
    """ Prompts user for employee and returns"""
    while True:
        if error:
            print(error)
        employee = input("Enter the employee name: ")
        if employee == "":
            error = "Please enter a valid string."
        else:
            return employee


def get_task(error=None):
    """ Prompts user for task and returns"""
    while True:
        if error:
            print(error)
        task = input("Enter the task name: ")
        if task == "":
            error = "Please enter a valid string."
        else:
            return task


def get_duration(error=None):
    """ Prompts user for duration and returns"""
    while True:
        if error:
            print(error)
        duration = input("Enter the duration of the task in minutes: ")
        if not duration.isdigit():
            error = "Please enter a valid integer"
        else:
            return duration


def entry_data():
    """ Calls functions for a new entry"""
    date = get_date()
    employee = get_employee()
    task = get_task()
    duration = get_duration()
    notes = input("Enter any notes (optional): ")

    entry = {
        'employee': employee,
        'date': date,
        'task': task,
        'duration': duration,
        'notes': notes,
    }
    create_entry(entry)


def create_entry(entry):
    """ Creates entry in database"""
    Entry.create(**entry)
    print("Saved successfully!")
    time.sleep(2)
    return entry


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
            edit(entry)
        elif choice == "d":
            delete(entry)
        elif choice == "r":
            break
        else:
            print("Please enter a valid choice.")
            time.sleep(3)


def search_employee_name():
    """Search entries by employee name"""
    employee = input("Employee: ")
    entries = Entry.select()
    entries = entries.where(Entry.employee.contains(employee))
    employee_list = []
    if entries:
        for entry in entries:
            if entry.employee not in employee_list:
                employee_list.append(entry.employee)
            else:
                pass
        search_employee_list(employee_list)
    else:
        print("No results found.")
        time.sleep(2)


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
        view_entries(entries)
    elif len(employee_list) == 1:
        employee = employee_list[0]
        entries = Entry.select()
        entries = entries.where(Entry.employee == employee)
        view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)


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
        view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)


def search_date_range():
    """ Searches for entries given date range."""
    print("Beginning date:")
    start_date = get_date()
    print("End date:")
    end_date = get_date()
    entries = Entry.select()
    entries = entries.where(
            (Entry.date >= start_date) &
            (Entry.date <= end_date))
    if entries:
        view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)


def search_duration():
    """ Searches for entries given duration. Returns a list of results """
    duration = get_duration()
    entries = Entry.select()
    entries = entries.where(Entry.duration == duration)
    if entries:
        view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)


def search_exact():
    """ Searches for entries given any string. Returns a list of results """
    exact_string = input("Enter string to search for: ")
    entries = Entry.select()
    entries = entries.where(
            (Entry.task.contains(exact_string)) |
            (Entry.notes.contains(exact_string)))
    if entries:
        view_entries(entries)
    else:
        print("No results found.")
        time.sleep(2)


def delete(entry):
    """ Deletes entry in database """
    entry.delete_instance()
    print("Entry deleted!")
    time.sleep(2)


def edit(entry):
    """ Prompts user what part of the entry to edit, edits database """
    print(dedent(f"""
    Which field would you like to edit?
    (D)ate, (E)mployee, (T)ask, D(u)ration, (N)otes
    """))
    while True:
        choice = input("> ").upper()
        if choice == "D":
            edit_val = get_date()
            entry.date = edit_val
            entry.save()
            break
        elif choice == "E":
            edit_val = get_employee()
            entry.employee = edit_val
            entry.save()
            break
        elif choice == "T":
            edit_val = get_task()
            entry.task = edit_val
            entry.save()
            break
        elif choice == "U":
            edit_val = get_duration()
            entry.duration = edit_val
            entry.save()
            break
        elif choice == "N":
            edit_val = input("Enter new notes: ")
            entry.notes = edit_val
            entry.save()
            break
        else:
            print("Please enter a valid choice.")
            time.sleep(1)
    print("Entry updated!")
    time.sleep(2)
