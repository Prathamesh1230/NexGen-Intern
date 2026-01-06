# Student Report Card System

import re

class Student:
    def __init__(self,roll,name,marks):
        self.roll = roll
        self.name = name
        self.marks = marks

    def get_average(self):
        return sum(self.marks) / len(self.marks)
    
    def get_grade(self):
        return "Pass" if self.get_average() >= 40 else "Fail"
    
    def display(self):
        print(
            "Roll:", self.roll,
            "Name:", self.name,
            "Marks:", self.marks,
            "Average:", round(self.get_average(), 2),
            "Grade:", self.get_grade()
        )

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def display_all(students):
    if not students:
        print("No records found.")
        return
    for s in students:
        s.display()

def find_topper(students):
    if not students:
        print("No records to check")
        return
    topper = max(students, key=lambda s: s.get_average())
    print("Topper - ")
    topper.display()

def search_by_roll(students, roll): # Time Complexity - O(n)
    for s in students:
        if s.roll == roll:
            print("Student found - ")
            s.display()
            return
    print("No student found with roll:", roll)

def search_by_name(students, pattern):
    found = [s for s in students if re.search(pattern, s.name, re.IGNORECASE)]
    if not found:
        print(f"Students matching '{pattern}':")
        return
    for s in found:
        s.display()
    else:
        print("No student found matching:", pattern)

def bubble_sort(students, descending = False):
    n = len(students)
    for i in range(n):
        for j in range(0, n - i - 1):
            if descending:
                if students[j].get_average() < students[j + 1].get_average():
                    students[j], students[j + 1] = students[j + 1], students[j]
            else:
                if students[j].get_average() > students[j + 1].get_average():
                    students[j], students[j + 1] = students[j + 1], students[j]
    return students

def show_pass_fail(students):
    passed = [s.name for s in students if s.get_grade() == "Pass"]
    failed = [s.name for s in students if s.get_grade() == "Fail"]
    print("Passed Students:", passed)
    print("Failed Students:", failed)

def main():
    students = [
        Student(1, "Prathamesh",[54, 72, 81]),
        Student(2, "Adwait",[45, 63, 72]),
        Student(3, "Sujay",[36, 54, 63]),
        Student(4, "Soham",[55, 66, 77]),
    ]

    while True:
        print("\n--- Student Report Card Menu ---")
        print("1. Display all students")
        print("2. Find topper")
        print("3. Search student by roll number")       
        print("4. Sort students by average marks")
        print("5. Show pass/fail list")     
        print("6. Factorial of roll number (Recursion demo)")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                display_all(students)

            elif choice == '2':
                find_topper(students)

            elif choice == '3':
                roll = int(input("Enter Roll Number to search: "))
                search_by_roll(students, roll)

            elif choice == '4':
                order = input("Sort in (a)scending or (d)escending order? ").lower()
                descending = True if order == 'd' else False
                bubble_sort(students, descending)
                print("Sorted students:")
                display_all(students)

            elif choice == '5':
                show_pass_fail(students)
            
            elif choice == '6':
                n = int(input("Enter a number for factorial: "))
                print("Factorial:", factorial(n))

            elif choice == '7':
                print("Exiting...")
                break

            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
