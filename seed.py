from string import ascii_uppercase
import faker
from random import randint, choice
from db import session
from models import (Student, 
                    Group, 
                    Subject, 
                    Teacher, 
                    Journal, 
                    StudentTeacher, 
                    TeacherSubject,
                    StudentSubject)

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20
SUBJECTS = [
    "Mathematics",
    "Biology",
    "History",
    "Chemistry",
    "Physics",
    "Literature",
    "Computer Science",
    "Psychology",
]

GRADES = [1, 2, 3, 4, 5]
PROBABILITIES = [1, 5, 15, 45, 34]


def get_random_gread():
    rand_num = randint(1, 100)
    cumulative_prob = 0
    for i, prob in enumerate(PROBABILITIES):
        cumulative_prob += prob
        if rand_num <= cumulative_prob:
            return GRADES[i]
        

def generate_fake_data(number_students, 
                       number_groups, 
                       number_subjects, 
                       number_teachers, 
                       number_grades):

    fake_data = faker.Faker()
    generated_names = set()
    groups = []
    
    for _ in range(number_groups):
        group = fake_data.bothify(text="??-##", letters=ascii_uppercase)
        groups.append(Group(group_name=group))
    session.add_all(groups)        
    session.commit()
    students = []

    for _ in range(number_students):
        student_name = fake_data.name()
        while student_name in generated_names:
            student_name = fake_data.name()
        generated_names.add(student_name)
        group_id = randint(1, number_groups)
        students.append(Student(student=student_name, group_id=group_id))
    session.add_all(students)
    session.commit()
    subjects = []
    
    for subject in SUBJECTS:
        subjects.append(Subject(subject_name=subject))
    session.add_all(subjects)
    session.commit()
    teachers = []

    for _ in range(number_teachers):
        teachers.append(Teacher(teacher=fake_data.name()))
    session.add_all(teachers)
    session.commit()
    
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    student_subjects = []
    
    for student in students:
        used_subject_ids = set()
        for _ in range(1, 3):
            while True:
                subject = choice(subjects)
                if subject.id not in used_subject_ids:
                    used_subject_ids.add(subject.id)
                    student_subjects.append(StudentSubject(student_id=student.id, subject_id=subject.id))
                    break
            
    session.add_all(student_subjects)
    session.commit()
    student_subjects = session.query(StudentSubject).all()
    journals = []
           
    for student_subject in student_subjects:
        for _ in range(randint(1, number_grades + 1)):
            journals.append(Journal(student_id=student_subject.student_id,
                                     subject_id=student_subject.subject_id,
                                     grade=get_random_gread(),
                                     grade_date=fake_data.date_this_year()))
    session.add_all(journals)
    session.commit()
    teacher_subjects = []
    
    for teacher in session.query(Teacher).all():
        used_subject_ids = set()
        group_id = randint(1, number_groups)
        for _ in range(randint(1, 3)):
            while True:
                subject = choice(subjects)
                if subject.id not in used_subject_ids:
                    used_subject_ids.add(subject.id)
                    teacher_subjects.append(TeacherSubject(teacher_id=teacher.id,
                                                           subject_id=subject.id,
                                                           group_id=group_id))
                    break
    session.add_all(teacher_subjects)
    session.commit()

    student_group_mapping = {student.id: student.group_id for student in students}
    student_teacher_relations = []
    for student_subject in student_subjects:
        student_id = student_subject.student_id
        subject_id = student_subject.subject_id
        group_id = student_group_mapping.get(student_id)

        for teacher_subject in teacher_subjects:
            if group_id == teacher_subject.group_id and subject_id == teacher_subject.subject_id:
                student_teacher_relations.append(StudentTeacher(student_id=student_id, teacher_id=teacher_subject.teacher_id))
    session.add_all(student_teacher_relations)
    session.commit()

if __name__ == "__main__":
    generate_fake_data(NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_SUBJECTS, NUMBER_TEACHERS, NUMBER_GRADES)

