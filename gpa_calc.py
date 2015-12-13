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

def get_count(msg):
    try:
        class_count = int(input(msg))
        if not class_count in range(100):
            raise ValueError
    except KeyboardInterrupt:
        exit(1)
    except:
        print("Invalid input, enter a number under 100")
        return
    return class_count

def get_grade(msg):
    try:
        grade = input(msg).upper()
        if grade in GRADE_GPA_MAP:
            gpa = GRADE_GPA_MAP[grade]
        else:
            gpa = float(grade)
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

def get_init():
    grade = None
    count = None
    while count is None:
        count = get_count("How many classes have you taken previously? ")
    if count:
        while grade is None:
            grade = get_grade("What is your current GPA? ")
    return count, grade

def usage():
    print("Usage:\n./gpa_calc.py [-i,--init]")

def main(init=False):
    init_count = None
    init_gpa = None
    if init:
        init_count, init_gpa = get_init()
    class_count = None
    while class_count is None:
        class_count = get_count("How many classes would you like to average in? ")
    scores = []
    for i in range(class_count):
        gpa = None
        while gpa is None:
            gpa = get_grade("Enter grade for class %s: " % str(i + 1))
            if gpa is not None:
                scores.append(gpa)
    if init_count:
        scores.extend([init_gpa for i in range(init_count)])
    avg = sum(scores)/len(scores)
    grade = gpa_to_grade(avg)
    print(avg, "(" + grade + ")")
    redo = input("Start over? [yN] ").lower()
    if redo == 'y' or redo == "yes":
        main(init)

if __name__ == '__main__':
    from sys import argv
    if "-h" in argv or "--help" in argv or "-?" in argv:
        usage()
    elif "-i" in argv or "--init" in argv:
        main(True)
    else:
        main()
    exit(0)
