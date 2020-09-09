# File Name: Roshan_Sreekanth_Project.py
# Author Name: Roshan Sreekanth
# Description: Employee Management System

import random


class Employee (object):
    def __init__(self, uid, f_name, s_name, email, salary):
        self.uid = uid
        self.f_name = f_name
        self.s_name = s_name
        self.email = email
        self.salary = salary

    def __str__(self):
        return "{:<10} {:10}{:10}{:20}{:15}".format(self.uid, self.f_name, self.s_name, self.email, self.salary)


def read_range_integer(prompt, min_range, max_range):  # done
    while True:
        try:
            user_input = int(input(prompt))
            while user_input < min_range or user_input > max_range:
                user_input = int(input("Enter value between " + str(min_range) + " and " + str(max_range) + ": "))
            return user_input
        except ValueError:
            print("Wrong value entered! Try again")
            continue


def read_positive_integer(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            while user_input < 0:
                user_input = int(input("Enter a positive number: "))
            return user_input
        except ValueError:
            print("Wrong value entered! Try again")
            continue


def read_positive_float(prompt):
    while True:
        try:
            user_input = float(input(prompt))
            while user_input < 0:
                user_input = float(input("Enter a positive number: "))
            return user_input
        except ValueError:
            print("Wrong value entered! Try again")
            continue


def read_nonempty_alphabetical_word(prompt):
    user_input = input(prompt)
    while len(user_input) == 0 or not user_input.isalpha():
        user_input = input("Enter non empty, alphabetical characters: ")
    return user_input


def process_file_data(filename):
    employee_list = []
    connection = open(filename, "r")
    for line in connection:
        data_list = line.split(",")
        uid = int(data_list[0])
        fname = data_list[1]
        lname = data_list[2]
        email = data_list[3]
        salary = float(data_list[4])
        employee_list.append(Employee(uid, fname, lname, email, salary))
    return employee_list


def get_choice():
    print("=" * 80)
    print("1. View all employees")
    print("2. View a particular employee")
    print("3. Edit the salary of an employee")
    print("4. Add a new employee")
    print("5. Delete an employee")
    print("6. Give a bonus to each employee, writing details to a file")
    print("7. Generate a report for management")
    print("8. Quit")
    print("="*80)

    prompt = "Enter a choice: "

    min_range = 1
    max_range = 8  # The choices go from 1-8

    choice = read_range_integer(prompt, min_range, max_range)
    print()  # For formatting

    return choice


def process_choice(choice, employee_list):
    if choice == 1:
        display_details(employee_list)
    if choice == 2:
        prompt = "Enter the employee's number: "
        query = read_positive_integer(prompt)
        result = employee_search(query, employee_list)
        if result is not None:
            print(result)
            input("Press Enter to continue...")
        else:
            print("Employee not found!")
            input("Press Enter to continue...")
    if choice == 3:
        prompt = "Enter the employee's number: "
        query = read_positive_integer(prompt)
        result = employee_search(query, employee_list)
        if result is not None:
            edit_salary(result)
        else:
            print("Employee not found!")
            input("Press Enter to continue...")
    if choice == 4:
        add_employee(employee_list)
    if choice == 5:
        prompt = "Enter the employees number: "
        query = read_positive_integer(prompt)
        result = employee_search(query, employee_list)
        if result is not None:
            delete_employee(result, employee_list)
        else:
            print("Employee not found!")
            input("Press Enter to continue...")
    if choice == 6:
        assign_bonus(employee_list)
    if choice == 7:
        generate_report(employee_list)


def employee_search(query, employee_list):
    return_value = None
    for employee in employee_list:
        if query == employee.uid:
            return_value = employee
            break
    return return_value


def display_details(employee_list):
    for employee in employee_list:
        print(employee)
    input("Press Enter to continue...")


def edit_salary(employee_object):
    prompt = "Enter new salary of " + employee_object.f_name + " " + employee_object.s_name + " : "
    employee_object.salary = read_positive_float(prompt)
    print(employee_object)
    input("Press Enter to continue...")


def generate_unique_email(f_name, s_name, employee_list):
    email_list = [employees.email for employees in employee_list]
    email = f_name.lower() + "." + s_name.lower() + "@cit.ie"
    counter = 1
    while email in email_list:  # Makes sure that two employees with the same name have different emails.
        email = f_name.lower() + "." + s_name.lower() + str(counter) + "@cit.ie"
        counter += 1
    return email


def generate_unique_id(employee_list):
    uid_list = [employees.uid for employees in employee_list]
    uid = random.randint(10000, 99999)
    while uid in uid_list:  # Makes sure the same ID is not generated twice
        uid = random.randint(10000, 99999)
    return uid


def add_employee(employee_list):
    f_name = read_nonempty_alphabetical_word("Enter the employee's first name: ")
    s_name = read_nonempty_alphabetical_word("Enter the employee's surname: ")
    salary = read_positive_float("Enter the employee's salary: ")
    email = generate_unique_email(f_name, s_name, employee_list)
    uid = generate_unique_id(employee_list)

    employee_object = Employee(uid, f_name, s_name, email, salary)
    employee_list.append(employee_object)
    print(employee_object)
    input("Press Enter to continue...")


def delete_employee(employee_object, employee_list):
    removed_name = employee_object.f_name + " " + employee_object.s_name
    employee_list.pop(employee_list.index(employee_object))
    print(removed_name, "has been removed")
    input("Press Enter to continue...")


def assign_bonus(employee_list):
    bonus_file = open("bonus.txt", "w")
    prompt = "Enter the end-of-year bonus percentage for employees: "
    percentage = read_positive_float(prompt)
    for employee in employee_list:
        increase = round(employee.salary * (percentage / 100), 2)  # Rounds the value to 2 decimal places
        bonus_file.write(str(employee.uid) + "," + employee.f_name + "," + employee.s_name + "," + str(increase) + "\n")
        print(employee.f_name, employee.s_name, "has received a bonus of ", increase)
    input("Press Enter to continue...")


def generate_report(employee_list):
    salary_list = [employees.salary for employees in employee_list]
    average_salary = round((sum(salary_list) / len(salary_list)), 2)  # Rounds the value to 2 decimal spaces
    max_salary = max(salary_list)

    print("The average salary is", average_salary)
    print("The highest salary is", max_salary)
    print("The highest salary is earned by: ")

    for employee in employee_list:
        if employee.salary == max_salary:
            print(employee.f_name, employee.s_name)
    input("Press Enter to continue...")


def save_details(filename, employee_list):
    employee_file = open(filename, "w")
    data = ""
    for employee in employee_list:
        data += str(employee.uid) + "," + employee.f_name + "," + employee.s_name + "," + employee.email + "," + str(employee.salary) + "\n"
    employee_file.write(data)
    employee_file.close()


def main():
    filename = "employees.txt"
    employee_list = process_file_data(filename)
    while True:  # Makes sure choices continue to be asked
        choice = get_choice()
        if choice == 8:
            save_details(filename, employee_list)
            input("Thank you for using the program! Press Enter to close")
            break
        process_choice(choice, employee_list)


main()
