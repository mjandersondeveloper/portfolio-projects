#
# Copyright Â© 2021 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
# Template code for CS 6340 Software Analysis
# Instructors: Mayur Naik and Chris Poch
# Head TAs: Kelly Parks and Joel Cooper
#
# Georgia Tech asserts copyright ownership of this template and all derivative
# works, including solutions to the projects assigned in this course. Students
# and other users of this template code are advised not to share it with others
# or to make it available on publicly viewable websites including repositories
# such as GitHub and GitLab. This copyright statement should not be removed
# or edited. Removing it will be considered an academic integrity issue.
#
# We do grant permission to share solutions privately with non-students such
# as potential employers as long as this header remains in full. However, 
# sharing with other current or future students or using a medium to share
# where the code is widely available on the internet is prohibited and 
# subject to being investigated as a GT honor code violation.
# Please respect the intellectual ownership of the course materials 
# (including exam keys, project requirements, etc.) and do not distribute them 
# to anyone not enrolled in the class. Use of any previous semester course 
# materials, such as tests, quizzes, homework, projects, videos, and any other 
# coursework, is prohibited in this course.#
import sys


if len(sys.argv) != 3:
    print("Usage: compare.py <first_file> <second_file>")
    exit(1)
f1 = sys.argv[1]
f2 = sys.argv[2]
fp1 = open(f1, "r")
fp2 = open(f2, "r")
i=0
type_1_errors = 0
type_2_errors = 0
for line1, line2 in zip(fp1, fp2):
    i += 1
    if(line1 == line2):
        continue
    nl1 = " " + line1.strip("[]\n")
    nl2 = " " + line2.strip("[]\n")
    x1 = set(nl1.split(";"))
    x2 = set(nl2.split(";"))
    if x1 != x2:
        print("Line difference in line {}:".format(i))
        diff_set1 = x1.difference(x2)
        diff_set2 = x2.difference(x1)
        if bool(diff_set1):
            print("Values missing from second file:", diff_set1)
            type_2_errors += len(diff_set1)
        if bool(diff_set2):
            print("Values missing from first file:", diff_set2)
            type_1_errors += len(diff_set2)
        print("Type 1 errors: %d; Type 2 errors: %d; Total: %d)" %
            (type_1_errors, type_2_errors, type_1_errors + type_2_errors))
        print("#########################")
