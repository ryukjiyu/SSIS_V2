import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="ssisv2"
)

class Student:
    def __init__(self, course, name, student_id, gender, year_level):
        self.course = course
        self.name = name
        self.student_id = student_id
        self.gender = gender
        self.year_level = year_level

    def __str__(self):
        return f"{self.course} {self.student_id}, {self.name}, {self.gender}, {self.year_level}"

    def edit(self, course, name, student_id, gender, year_level):
        self.course = course
        self.name = name
        self.student_id = student_id
        self.gender = gender
        self.year_level = year_level


class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"{self.code}, {self.name}"

    def edit(self, code, name):
        self.code = code
        self.name = name


class StudentManagementSystem:
    def __init__(self):
        self.course_management_system = None

    def check_studentID(self, student_id):
        cursor = db.cursor()
        query = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    def add_student(self, student_id, name, gender, year_level, course):
        cursor = db.cursor()
        query = "INSERT INTO student (studentID, name, gender, year_level, course_code) VALUES (%s, %s, %s, %s, %s)"
        values = (student_id, name, gender, year_level, course.upper())
        cursor.execute(query, values)
        db.commit()
        print("Student added successfully!")

    def delete_student(self, student_id):
        cursor = db.cursor()
        query = "DELETE FROM student WHERE studentID = %s"
        cursor.execute(query, (student_id,))
        db.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student not found.")

    def edit_student(self, student_id, name, gender, year_level, course_code):
        cursor = db.cursor()
        query = "SELECT * FROM student"
        cursor.execute(query)
        data = cursor.fetchall()

        found = False
        for row in data:
            if row[0] == student_id:
                found = True
                new_name = name or row[1]
                new_gender = gender or row[2]
                new_year_level = year_level or row[3]
                new_course_code = course_code or row[4]
                query = "UPDATE student SET name = %s, gender = %s, year_level = %s, course_code = %s WHERE studentID = %s"
                values = (new_name, new_gender, new_year_level, new_course_code, student_id)
                cursor.execute(query, values)
                db.commit()
                print("Student Information edited successfully.")
        if not found:
            print("Student not found.")

    def list_students(self):
        cursor = db.cursor()
        query = "SELECT * FROM student"
        cursor.execute(query)
        data = cursor.fetchall()

        for row in data:
            print(row)

    def search_student(self, search_key):
        cursor = db.cursor()
        query = "SELECT * FROM student WHERE studentID LIKE %s OR name LIKE %s OR gender LIKE %s OR year_level LIKE %s OR course_code LIKE %s"
        values = (f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%", f"%{search_key}%")
        cursor.execute(query, values)
        results = cursor.fetchall()

        found = False
        if results:
            found = True
            for row in results:
                print("\nStudent ID: ", row[0])
                print("Name: ", row[1])
                print("Gender: ", row[2])
                print("Year Level: ", row[3])
                print("Course Code: ", row[4])
        if not found:
            print("Student not found.")


class CourseManagementSystem:
    def __init__(self):
        self.student_management_system = None

    def check_course_code(self, course_code):
        cursor = db.cursor()
        query = "SELECT course_code FROM course WHERE course_code = %s"
        cursor.execute(query, (course_code,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    def add_course(self, code, name):
        cursor = db.cursor()
        query = "INSERT INTO course (course_code, course_name) VALUES (%s, %s)"
        values = (code, name)
        cursor.execute(query, values)
        db.commit()
        print("Course added successfully!")

    def delete_course(self, code):
        cursor = db.cursor()
        query = "SELECT course_code FROM course WHERE course_code = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()

        if result:
            while True:
                choice = input("Are you sure to delete this course? Students under this course will also be deleted.\n1. Yes\n2. No\nEnter your choice: ")
                if choice == '1':
                    delete_query = "DELETE FROM course WHERE course_code = %s"
                    cursor.execute(delete_query, (code,))
                    db.commit()
                    print("Course deleted successfully.")
                    break
                elif choice == '2':
                    print("Course not deleted.")
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Course not found.")

    def edit_course(self, code, name):
        cursor = db.cursor()
        query = "UPDATE course SET course_name = %s WHERE course_code = %s"
        values = (name, code)
        cursor.execute(query, values)
        db.commit()
        print("Course edited successfully.")

    def list_courses(self):
        print("\nList of Courses:")
        cursor = db.cursor()
        query = "SELECT * FROM course"
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            print(row[0], "-", row[1])

    def search_course(self, search_key):
        cursor = db.cursor()
        query = "SELECT * FROM course WHERE course_code LIKE %s OR course_name LIKE %s"
        values = (f"%{search_key}%", f"%{search_key}%")
        cursor.execute(query, values)
        result = cursor.fetchall()

        if result:
            for row in result:
                print("\nCourse Code: ", row[0])
                print("Course Name: ", row[1])
        else:
            print("Course not found.\n")

def main():
    course_management_system = CourseManagementSystem()
    student_management_system = StudentManagementSystem()
    course_management_system.student_management_system = student_management_system
    student_management_system.course_management_system = course_management_system

    while True:
        print("\n1. CRUDL operations for students")
        print("2. CRUDL operations for courses")
        print("3. Exit\n")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                print("\n1. Add student")
                print("2. Delete student")
                print("3. Edit student")
                print("4. List of students")
                print("5. Search student")
                print("6. Go back\n")
                student_choice = input("Enter your choice: ")

                if student_choice == '1':
                    course = input("Enter the course: ")
                    if not course_management_system.check_course_code(course):
                        print("Course does not exist. Do you want to add it?")
                        print("[1] Yes")
                        print("[2] No")
                        choice = input("Enter your choice:")
                        if choice == '1':
                            course_name = input("Enter the course name(BS of Computer Science): ")
                            course_management_system.add_course(course, course_name)
                        elif choice == '2':
                            print("Course and student not added.")
                            continue
                        else:
                            print("Invalid choice. Course and student not added.\n")
                            continue

                    student_id = input("Enter the ID: ")
                    if student_management_system.check_studentID(student_id):
                        print("Student already added.")
                        continue
                    else:
                        student_name = input("Enter the student name: ")
                        gender = input("Enter the gender: ")
                        year_level = input("Enter the year level: ")
                        student_management_system.add_student(student_id, student_name, gender, year_level, course)
                        print("Student successfully added.")
                        continue

                elif student_choice == '2':
                    student_id = input("Enter the ID of the student to be deleted: ")
                    student_management_system.delete_student(student_id)

                elif student_choice == '3':
                    student_id = input("Enter the ID of the student to be edited: ")
                    if student_management_system.check_studentID(student_id):
                        name = input("Enter the new name: ")
                        gender = input("Enter the new gender: ")
                        year_level = input("Enter the new year level: ")
                        course_code = input("Enter the new course code: ")
                        if not course_code.strip():
                            student_management_system.edit_student(student_id, name, gender, year_level, course_code.upper())
                        else:
                            if not course_management_system.check_course_code(course_code):
                                while True:
                                    choice = input("Course does not exist. Do you want to add it?\n1. Yes\n2.No\nEnter your choice:")
                                    if choice == '1':
                                        course_name = input("Enter the course name(BS of Computer Science): ")
                                        course_management_system.add_course(course_code, course_name)
                                        student_management_system.edit_student(student_id, name, gender, year_level,course_code.upper())
                                        break
                                    elif choice == '2':
                                        print("Course not added. Student not edited.")
                                        break
                                    else:
                                        print("Invalid choice. Course and student not added.")
                            else:
                                student_management_system.edit_student(student_id, name, gender, year_level,course_code.upper())
                    else:
                        print("Student not found.")
                        continue

                elif student_choice == '4':
                    student_management_system.list_students()

                elif student_choice == '5':
                    search_key = input("Enter the search key: ")
                    student_management_system.search_student(search_key)

                elif student_choice == '6':
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == '2':
            while True:
                print("\n1. Add course")
                print("2. Delete course")
                print("3. Edit course")
                print("4. List of courses")
                print("5. Search course")
                print("6. Go back\n")
                course_choice = input("Enter your choice:")

                if course_choice == '1':
                    code = input("Enter the code: ")
                    name = input("Enter the name: ")
                    course_management_system.add_course(code, name)

                elif course_choice == '2':
                    code = input("Enter the code of the course to be deleted: ")
                    course_management_system.delete_course(code)

                elif course_choice == '3':
                    code = input("Enter the code of the course to be edited: ")
                    if course_management_system.check_course_code(code):
                        name = input("Enter the new name: ")
                        course_management_system.edit_course(code, name)
                    else:
                        print("Course not found.")

                elif course_choice == '4':
                    course_management_system.list_courses()

                elif course_choice == '5':
                    search_key = input("Enter the search key: ")
                    course_management_system.search_course(search_key)

                elif course_choice == '6':
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == '3':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()