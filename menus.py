import datetime
import os
import re
import sqlite3
import sys
import time

from textwrap import dedent
from peewee import *

import work_log


def clear():
    """ Clears screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu(choice=None):
    """ Prints a menu choice and directs to corresponding function"""
    while True:
        clear()
        print(dedent("""
            WORK log
            What would you like to do? Enter a, b or c.
            a) Add new entry
            b) Search in existing entries
            c) Quit program"""))
        choice = input("> ")

        if choice == "a":
            work_log.add()
        elif choice == "b":
            search()
        elif choice == "c":
            print("Thanks for using WORK LOG!")
            sys.exit()
        else:
            print("Please enter a, b or c.")
            time.sleep(3)


def search():
    """ Presents user with search menu and directs to corresponding function"""
    while True:
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
            search_employee()
        elif choice == "b":
            search_date()
        elif choice == "c":
            work_log.search_duration()
        elif choice == "d":
            work_log.search_exact()
        elif choice == "e":
            break
        else:
            print("Please enter a valid choice")
            time.sleep(3)


def search_employee():
    """ Presents user with choice to search by name or see a list"""
    while True:
        clear()
        print(dedent("""
            What do you want to do? Enter a, b or c.
            a) Input a name to search
            b) See a list of employees
            c) Return to search menu
            """))
        choice = input("> ")
        if choice == "a":
            work_log.search_employee_name()
        elif choice == "b":
            work_log.search_employee_list()
        elif choice == "c":
            break
        else:
            print("Please enter a valid choice")
            time.sleep(3)


def search_date():
    """ Presents user with choice to search by list of dates or range"""
    while True:
        clear()
        print(dedent("""
            What do you want to do? Enter a or b.
            a) Choose from a list of dates
            b) Search by a date range
            c) Return to search menu
            """))
        choice = input("> ")
        if choice == "a":
            work_log.search_date_list()
        elif choice == "b":
            work_log.search_date_range()
        elif choice == "c":
            break
        else:
            print("Please enter a valid choice")
            time.sleep(3)


if __name__ == '__main__':
    work_log.initialize()
    main_menu()
