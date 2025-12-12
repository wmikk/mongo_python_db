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
    print("\t5) Exit application")

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
        break
    else:
        print("I don't know that command")

print("Goodbye!")

