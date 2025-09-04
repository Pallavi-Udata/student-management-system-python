# Student Management System - Phase 1 (Console Version)

students = []  # list to store student records

def add_student():
    roll_no = int(input("Enter Roll No: "))
    name = input("Enter Name: ")
    course = input("Enter Course: ")
    marks = float(input("Enter Marks: "))
    students.append({"roll_no": roll_no, "name": name, "course": course, "marks": marks})
    print("✅ Student added successfully!\n")

def view_students():
    if not students:
        print("⚠️ No students found.\n")
        return
    print("\n--- Student Records ---")
    for s in students:
        print(f"Roll No: {s['roll_no']}, Name: {s['name']}, Course: {s['course']}, Marks: {s['marks']}")
    print()

def search_student():
    roll_no = int(input("Enter Roll No to search: "))
    for s in students:
        if s["roll_no"] == roll_no:
            print(f"✅ Found: {s}")
            return
    print("⚠️ Student not found.\n")

def update_student():
    roll_no = int(input("Enter Roll No to update: "))
    for s in students:
        if s["roll_no"] == roll_no:
            s["name"] = input("Enter New Name: ")
            s["course"] = input("Enter New Course: ")
            s["marks"] = float(input("Enter New Marks: "))
            print("✅ Student updated successfully!\n")
            return
    print("⚠️ Student not found.\n")

def delete_student():
    roll_no = int(input("Enter Roll No to delete: "))
    for s in students:
        if s["roll_no"] == roll_no:
            students.remove(s)
            print("✅ Student deleted successfully!\n")
            return
    print("⚠️ Student not found.\n")

def menu():
    while True:
        print("==== Student Management System ====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.\n")

# Run the program
if __name__ == "__main__":
    menu()
