import os
import matplotlib.pyplot as plt


def load_students(filepath):
    students = {}
    with open(filepath, 'r') as f:
        for line in f:
            name, student_id = line.strip().rsplit(" ", 1)
            students[student_id] = name
    return students


def load_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()] 
        for i in range(0, len(lines), 3):
            name = lines[i]
            assignment_id = lines[i+1]
            points = int(lines[i+2])
            assignments[assignment_id] = {
                'name': name,
                'points': points
            }
    return assignments



def load_submissions(directory):
    submissions = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        student_id, assignment_id, percent = parts
                        submissions.append({
                            'student_id': student_id,
                            'assignment_id': assignment_id,
                            'percent': float(percent)
                        })
    return submissions


def get_student_grade(name, students, assignments, submissions):
    student_id = None
    for sid, sname in students.items():
        if sname.lower() == name.lower():
            student_id = sid
            break

    if not student_id:
        print("Student not found")
        return

    total_score = 0
    for sub in submissions:
        if sub['student_id'] == student_id:
            points = assignments[sub['assignment_id']]['points']
            total_score += (sub['percent'] / 100) * points

    grade = round((total_score / 1000) * 100)
    print(f"{grade}%")


def assignment_statistics(name, assignments, submissions):
    assignment_id = None
    for aid, info in assignments.items():
        if info['name'].lower() == name.lower():
            assignment_id = aid
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = [
        sub['percent']
        for sub in submissions
        if sub['assignment_id'] == assignment_id
    ]

    if not scores:
        print("No submissions found for this assignment.")
        return

    print(f"Min: {int(min(scores))}%")
    print(f"Avg: {int(sum(scores) / len(scores))}%")
    print(f"Max: {int(max(scores))}%")


def assignment_graph(name, assignments, submissions):
    assignment_id = None
    for aid, info in assignments.items():
        if info['name'].lower() == name.lower():
            assignment_id = aid
            break

    if not assignment_id:
        print("Assignment not found")
        return

    scores = [
        sub['percent']
        for sub in submissions
        if sub['assignment_id'] == assignment_id
    ]

    if not scores:
        print("No submissions found for this assignment.")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Score Distribution for {name}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()


def main():
    students = load_students("data/students.txt")
    assignments = load_assignments("data/assignments.txt")
    submissions = load_submissions("data")

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    selection = input("Enter your selection: ")

    if selection == '1':
        name = input("What is the student's name: ")
        get_student_grade(name, students, assignments, submissions)
    elif selection == '2':
        name = input("What is the assignment name: ")
        assignment_statistics(name, assignments, submissions)
    elif selection == '3':
        name = input("What is the assignment name: ")
        assignment_graph(name, assignments, submissions)

if __name__ == "__main__":
    main()

