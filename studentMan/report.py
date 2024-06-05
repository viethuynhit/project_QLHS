from .models import *


class Report:
    def __init__(self, lop="", siSo=0, soLuongDat=0, tiLe=0):
        self.lop = lop
        self.siSo = siSo
        self.soLuongDat = soLuongDat
        self.tiLe = tiLe

    def findClassID(self, currentID):
        currentUser = Teacher.objects.filter(user=currentID)
        if not currentUser:
            currentUser = Student.objects.filter(StudentID=currentID)
        return currentUser[0].classOfSchool.id

    def countPassedSubject(self, student, semester):
        marks = Mark.objects.filter(student=student, semester_mark=semester)
        count = 0
        for mark in marks:
            minMark = mark.subject.approved_mark
            m = (mark.markFifteen + 2 * mark.markOne + 3 * mark.markFinal) / 6
            if m >= minMark:
                count += 1
        return count

    def passedSemester(self, student, semester):
        passedSubject = self.countPassedSubject(student, semester)
        if passedSubject == 9:
            return True
        else:
            False

    def passedRate(self, students, semester):
        count = 0
        for student in students:
            if self.passedSemester(student, semester):
                count += 1
        return [count, (count / len(students)) * 100]

    def createReport(self, classID, semester):
        students = Student.objects.filter(classOfSchool__id=classID)
        Lop = ClassOfSchool.objects.filter(id=classID)[0].classId
        passed_count, passed_rate = self.passedRate(students, semester)
        return Report(Lop, len(students), passed_count, passed_rate)

    def show(self, currentID, className, semester, year):
        if className == "---":
            classID = self.findClassID(currentID)
        else:
            classID = ClassOfSchool.objects.filter(classId=className, year__year=year)[0].id

        return self.createReport(classID, semester)
