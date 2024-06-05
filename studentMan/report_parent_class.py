from .models import *


class Report:
    def __init__(self, class_id="", student_number=0, passed_number=0, passed_rate=0):
        self.class_id = class_id
        self.student_number = student_number
        self.passed_number = passed_number
        self.passed_rate = passed_rate

    @staticmethod
    def remove_duplicate(list):
        met = []
        for i in list:
            if i.classId not in met:
                met.append(i.classId)
        return met

    def find_class_of_user(self, username, year):
        current_user = Teacher.objects.filter(user__username=username)
        if current_user:
            return current_user[0].classOfSchool.filter(year__year=year)
        current_user = Student.objects.filter(user__username=username)
        if current_user:
            return current_user[0].classOfSchool.filter(year__year=year)

        return ClassOfSchool.objects.filter(year__year=year)

    def get_average_mark(self, mark):
        return (mark.markFifteen + 2 * mark.markOne + 3 * mark.markFinal) / 6

    def check_passed(self, mark, subject):
        if (mark.markOne == None) or (mark.markFifteen == None) or (mark.markFinal == None):
            return -1
        if self.get_average_mark(mark) >= subject.approved_mark:
            return 1
        else:
            return 0
