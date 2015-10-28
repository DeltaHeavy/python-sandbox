#!/usr/bin/env python3

from sys import exit

VALID_GPAS = [0, 0.7, 1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0]

GRADE_GPA_MAP = {
    "A":4.0,
    "A-":3.7,
    "B+":3.3,
    "B":3.0,
    "B-":2.7,
    "C+":2.3,
    "C":2.0,
    "C-":1.7,
    "D+":1.3,
    "D":1.0,
    "D-":0.7,
    "F":0,
}

def get_count():
    try:
        class_count = int(input("How many classes have you taken? "))
        if not class_count in range(1, 100):
            raise ValueError
    except KeyboardInterrupt:
        exit(1)
    except:
        print("Invalid input, enter a number between 1 and 100")
        return
    return class_count

def get_grade(ndx):
    try:
        grade = input("Enter grade for class %s: " % str(ndx + 1)).upper()
        if grade in GRADE_GPA_MAP:
            gpa = GRADE_GPA_MAP[grade]
        elif float(grade) in VALID_GPAS:
            gpa = float(grade)
        else:
            raise ValueError
    except KeyboardInterrupt:
        exit(1)
    except:
        print("Invalid input, enter a valid GPA or letter grade")
        return None
    return gpa

def gpa_to_grade(avg):
    grade_tuples = sorted(list(GRADE_GPA_MAP.items()), key=lambda t: t[1], reverse=True)
    for grade, gpa in grade_tuples:
        if avg >= gpa:
            return grade

def main():
    class_count = None
    while class_count is None:
        class_count = get_count()
    scores = []
    for i in range(class_count):
        gpa = None
        while gpa is None:
            gpa = get_grade(i)
            if gpa is not None:
                scores.append(gpa)
    avg = sum(scores)/len(scores)
    grade = gpa_to_grade(avg)
    print(avg, "(" + grade + ")")
    redo = input("Start over? [yN] ").lower()
    if redo == 'y' or redo == "yes":
        main()

if __name__ == '__main__':
    main()
