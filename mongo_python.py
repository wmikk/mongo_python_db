from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")

db = client["student_grade_db"]

courses_collection = db["courses"]
grades_collection = db["grades"]

print("Welcome to the library application!")

def print_commands():
    print("Commands:")
    print("\t1) List courses")
    print("\t2) Add a course")
    print("\t3) Edit a course")
    print("\t4) Delete a course")
    print("\t5) Add a grade")
    print("\t6) Edit grade")
    print("\t7) list grade by course")
    print("\t8) delete a grade") 

def list_courses():
    print("List all the courses")
    all_courses = courses_collection.find()
    for courses_document in all_courses:
        print(courses_document["name"])     
    
def add_course():
    print("Provide the courses information")
    name = input("course name:")
    teacher = input("course teacher:")
    credits = input("number of credits:")
    year = input("year:")
    semester = input("semester:")
    isArchived = input("is archived (true/false):")
    topics = input("course topics (comma separated):")
    
    new_course = {
        "name": name,
        "teacher": teacher,
        "credits": int(credits),
        "year": int(year),
        "semester": semester,
        "isArchived": isArchived.lower() == "true", 
        "topics": topics.split(",")
    }

    courses_collection.insert_one(new_course)
    
    print(f"course {name} has been added!")

def add_grade():
    print("Provide the grade information")
    course_id_str = input("Enter the ID of the course for this grade:")
    try:
        course_oid = ObjectId(course_id_str)

    except Exception:
        print("Invalid ID format. Cannot add grade.")
        return

    student_name = input("Student name:")
    grade = input("Grade:")
    student_number = input("student_number:")
    comment = input("comment:")

    new_grade = {
            "course_id": course_oid,
            "student_name": student_name,
            "student_number": student_number,
            "grade": int(grade),
            "comment": comment
        }
    
    grades_collection.insert_one(new_grade)
    print(f"Grade added for {student_name}")

def list_grades_by_course():
    course_id_str = input("\nEnter the Course ID to view grades: ")
    
    try:
        course_oid = ObjectId(course_id_str)
    except Exception:
        print("Invalid ID format.")
        return
    course_grades = grades_collection.find({"course_id": course_oid})

    for entry in course_grades:
        print(f"Student: {entry['student_name']} | Grade: {entry['grade']}")

def edit_grade():
    print("Provide the grade information")
    grade_id_str = input("Enter the ID of the grade:")
    try:
        grade_oid = ObjectId(grade_id_str)

    except Exception:
        print("Invalid ID format. Cannot edit grade.")
        return

    print("Provide new info (press Enter to skip):")
    new_grade_val = input("New Grade (0-5): ")
    new_student_name = input("Corrected Student Name: ")
    new_student_number = input("New student number")
    new_comment = input("edit a comment")

    new_grade = {
            "student_name": new_student_name,
            "student_number": new_student_number,
            "grade": int(new_grade_val),
            "comment": new_comment
        }
    
    grades_collection.update_one(new_grade)
    print(f"Grade edited for {new_student_name}")

def delete_grade():
    print("Provide the grade information")
    grade_id_str = input("Enter the ID of the grade:")
    try:
        grade_oid = ObjectId(grade_id_str)

    except Exception:
        print("Invalid ID format. Cannot delete grade.")
        return

    grades_collection.delete_one({"_id": grade_oid})
    print("Course deleted successfully")

def edit_course():
    print("Which course do you want to edit?")
    course_id_str = input("Enter the Course ID to edit:")
    
    try:
        course_oid = ObjectId(course_id_str)
    except Exception:
        print("Invalid ID")
        return
    
    print("Provide the new information for the course")
    new_name = input("New Course Name: ")
    new_credits = input("New Credits: ")
    new_teacher = input("New Teacher: ")

    updates = {}
    if new_name: 
        updates["name"] = new_name
    if new_teacher:
        updates["teacher"] = new_teacher
    if new_credits:
        updates["credits"] = new_credits

    courses_collection.update_one({"_id": course_oid}, {"$set": updates})
    print("Course updated successfully")
    

def delete_course():
    course_id_str = input("Enter the Course Id to delete")
    
    try:
        course_oid = ObjectId(course_id_str)
    except Exception:
        print("Invalid ID")
        return
    
    courses_collection.delete_one({"_id": course_oid})
    print("Course deleted successfully")

while True:
    command = input("Type in the command number:")
    
    if command == "1":
        list_courses()
    elif command == "2":
        add_course()
    elif command == "3":
        edit_course()
    elif command == "4":
        delete_course()
    elif command == "5":
        add_grade()
    elif command == "6":
        edit_grade()
    elif command == "7":
        list_grades_by_course()
    elif command == "8":
        delete_grade()
        break
    else:
        print("I don't know that command")

print("Goodbye!")

