from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import *
from .report import *
from datetime import datetime
from .decorators import *
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .filters import *
from .forms import *
from .models import *
from .report_child_classes import *
from django.db.models import Max

semester = 2


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def admin_home(request):
    total_admins = Admin.objects.all().count()
    total_teachers = Teacher.objects.all().count()
    total_students = Student.objects.all().count()
    total_subjects = Subject.objects.all().count()
    total_classes = ClassOfSchool.objects.all().count()
    total_classes = ClassOfSchool.objects.all().count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
        'total_subjects': total_subjects,
        'total_classes': total_classes,
    }
    return render(request, 'admin_template/home_content.html', context=context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)     
            if request.user.role == '1':
                return redirect(reverse("admin_home"))
            elif request.user.role == '2':
                return redirect(reverse("dsLop"))
            else:
                return redirect(reverse("dsLopHS"))
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'admin_template/login.html')


@login_required(login_url='login')
def capNhatTaiKhoan(request):
    if request.method == 'POST':
        profile_form = userUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Cập nhật thành công')
            return redirect(to='capNhatTaiKhoan')
    else:
        profile_form = userUpdateForm(instance=request.user)

    return render(request, 'admin_template/capNhatTaiKhoan.html', {'profile_form': profile_form})


class doiMatKhau(SuccessMessageMixin, PasswordChangeView):
    template_name = 'admin_template/capNhatMatKhau.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('capNhatTaiKhoan')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def themAdmin(request):
    form = AdminForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            try:
                admin = Admin()
                user = CustomUser.objects.create_superuser(
                    username=username, password=password, name=name,
                    dateOfBirth=datetime.strptime(dateOfBirth, '%Y-%m-%d'),
                    sex=sex, email=email, phone=phone, address=address)
                user.save()
                admin.user = user
                admin.save()
                messages.success(request, "Thêm thành công")
                return redirect(reverse('dsTaiKhoan'))
            except:
                messages.error(request, "Không thể thêm")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    return render(request, 'admin_template/themAdmin.html', context=context)


@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def themGV(request):
    form = TeacherForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            subject = form.cleaned_data.get('subject')
            classOfSchool = form.cleaned_data.get('classOfSchool')
            try:
                user = CustomUser.objects.create_staff(
                    username=username, password=password, name=name, role='2',
                    dateOfBirth=datetime.strptime(dateOfBirth, '%Y-%m-%d'),
                    sex=sex, email=email, phone=phone, address=address)
                teacher = Teacher(user=user)
                if subject:
                    teacher.subject = subject
                teacher.save()
                for c in classOfSchool:
                    teacher.classOfSchool.add(c)
                teacher.save()
                messages.success(request, "Thêm thành công")
                return redirect(reverse('dsTaiKhoan'))
            except:
                messages.error(request, "Không thể thêm")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    return render(request, 'admin_template/themGV.html', context=context)


@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def tiepNhanHS(request):
    form = StudentForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            try:
                print("aaaaaaaaaaaaaaaaaaâ")
                user = CustomUser.objects._create_user(
                    username=username, password=password, name=name, role='3',
                    dateOfBirth=datetime.strptime(dateOfBirth, '%Y-%m-%d'),
                    sex=sex, email=email, phone=phone, address=address)
                student = Student(user=user)
                print(student)
                student.save()
                messages.success(request, "Thêm thành công")
            except:
                messages.error(request, "Không thể thêm")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    return render(request, 'admin_template/tiepNhanHS.html', context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Teacher'])
def dsLop(request):
    students = Student.objects.all().order_by('user__name')
    classFilter = ClassFilter(request.GET, queryset=students)
    students = classFilter.qs.order_by('user__name')
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in students]
    context = {
        'students': zip(students,formatDate),
        'classFilter': classFilter,
    }
    return render(request, 'admin_template/dsLop.html', context=context)


@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def chonNienKhoaLop(request):
    form = YearForm()
    age = Age.objects.all()
    context = {
        'form': form,
        'age': age
    }
    return render(request, 'admin_template/chonNienKhoaLop.html', context=context)


@allowed_users(allowed_roles=['Admin'])
@login_required(login_url='login')
def lapDSLop(request,age_id):
    year = Age.objects.get(id =age_id)
    student_with_year = []
    for student in Student.objects.all():
        for c in student.classOfSchool.all():
            if c.year == year:
                student_with_year.append(student)
                break
    student_dont_with_year = []
    for student in Student.objects.all():
        if student not in student_with_year:
            student_dont_with_year.append(student)
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in student_dont_with_year]
    form = CreateClassForm(request.POST, age_id=age_id)
    if request.method == 'POST':
        usernames = request.POST.getlist('username_class')
        cl = request.POST.get('classId')
        class_list = ClassOfSchool.objects.all()
        for classOfSchool in class_list:
            if classOfSchool.classId == cl:
                studentsInClass = Student.objects.filter(classOfSchool__classId=cl)
                if classOfSchool.max_number >= (len(studentsInClass) + len(usernames)):
                    for username in usernames:
                        student = Student.objects.get(user__username=username)
                        student.classOfSchool.add(classOfSchool)
                        student.save()
                        for sub in Subject.objects.all():
                            for semester_mark in range(1, semester + 1):
                                mark = Mark()
                                mark.student = student
                                mark.subject = sub
                                mark.semester_mark = semester_mark
                                mark.markFifteen = 0
                                mark.markOne = 0
                                mark.markFinal = 0
                                mark.save()
                    messages.success(request, "Thêm thành công")
                    return redirect(reverse('lapDSLop', kwargs={'age_id': age_id}))
                else:
                    messages.success(request, "Số lượng học sinh vượt quá qui định")
    context = {
        'students': zip(student_dont_with_year,formatDate),
        'form': form,
    }
    return render(request, 'admin_template/lapDS.html', context=context)


def trungBinhMon(subject, student):
    for mark in Mark.objects.filter(student=student).filter(subject=subject):
        if mark.semester_mark == '1':
            avgMarks1 = round((mark.markFifteen + 2 * mark.markOne + 3 * mark.markFinal) / 6, 2)
        else:
            avgMarks2 = round((mark.markFifteen + 2 * mark.markOne + 3 * mark.markFinal) / 6, 2)
    return avgMarks1, avgMarks2


@allowed_users(allowed_roles=['Admin', 'Teacher'])
@login_required(login_url='login')
def chonNienKhoaTraCuu(request):
    form = YearForm()
    age = Age.objects.all()
    context = {
        'form': form,
        'age': age
    }
    return render(request, 'admin_template/chonNienKhoaTraCuu.html', context=context)


@allowed_users(allowed_roles=['Admin', 'Teacher'])
@login_required(login_url='login')
def traCuu(request,age_id):
    year = Age.objects.get(id =age_id)
    marks = Mark.objects.filter(subject__year= year)
    marksFilter = StudentInMarkFilter(request.GET, queryset=marks)
    marks = marksFilter.qs.order_by('student__user__name')
    students = []
    avgMarks1 = []
    avgMarks2 = []
    classOfSchool = []
    marks_in_year = marks
    students_in_year = set([mark.student for mark in marks_in_year])
    print(students_in_year)
    for student in students_in_year:
        students.append(student)
        subjects_in_year = set([mark.subject for mark in marks_in_year])
        m = [trungBinhMon(subject, student) for subject in subjects_in_year]
        s1 =0
        s2 = 0
        for i in m:
            s1+= i[0]
            s2 += i[1]
        avgMarks1.append(s1/len(m))
        avgMarks2.append(s2/len(m))
        for c in student.classOfSchool.all():
            if c.year == year:
                classOfSchool.append(c)
                break

    marks = zip(students, classOfSchool, avgMarks1, avgMarks2)
    context = {
        'marks': marks,
        'marksFilter': marksFilter
    }
    return render(request, 'admin_template/traCuu.html', context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def bangDiem(request):
    marks = Mark.objects.all()
    myFilter = MarkFilter(request.GET, queryset=marks)
    marks = myFilter.qs
    context = {
        'marks': marks,
        'myFilter': myFilter,
    }
    return render(request, 'admin_template/bangDiem.html', context=context)

@login_required(login_url='login')
def baoCaoMonHoc(request, lop, mon, hocKy, nienKhoa):
    all_classes = Subject_Report().remove_duplicate(ClassOfSchool.objects.all())
    subjects = Subject.objects.all()
    years = Age.objects.all()
    id = request.user.username
    reports = Subject_Report().report_to_show(id, lop, mon, hocKy, nienKhoa)
    context = {'reports': reports,
               'classes': all_classes,
               'current_class': lop,
               'semester': hocKy,
               'years': years,
               'year': nienKhoa,
               'subjects': subjects,
               'subject': mon}
    return render(request, 'admin_template/baoCaoMonHoc.html', context)


@login_required(login_url='login')
def baoCaoMH(request):
    years = Age.objects.all()
    current_year = years.aggregate(Max('year'))
    return baoCaoMonHoc(request, '---', '---', 1, current_year['year__max'])

@unauthenticated_user
@login_required(login_url='login')
def baoCaoHocKy(request, lop, hocKy, nienKhoa):
    all_classes = Semester_Report().remove_duplicate(ClassOfSchool.objects.all())
    reports = Semester_Report().report_to_show(request.user.username, lop, hocKy, nienKhoa)
    all_nienKhoa = Age.objects.all()
    context = {'reports': reports,
               'classes': all_classes,
               'lop': lop,
               'hocky': hocKy,
               'nienKhoa': nienKhoa,
               'all_nienKhoa': all_nienKhoa}

    return render(request, 'admin_template/baoCaoHocKi.html', context)


def baoCaoHK(request):
    years = Age.objects.all()
    current_year = years.aggregate(Max('year'))
    return baoCaoHocKy(request, "---", 1, current_year['year__max'])


@allowed_users(allowed_roles=['Admin'])
def quanLiTuoi(request):
    age = Age.objects.all()
    context = {'age': age}
    return render(request, 'admin_template/quanLiTuoi.html', context=context)


@allowed_users(allowed_roles=['Admin'])
def capNhatTuoi(request, age_id):
    age = get_object_or_404(Age, id=age_id)
    form = ageForm(request.POST or None, instance=age)
    context = {
        'form': form,
        'subject_id': age_id,
        'page_title': 'capNhatTuoi'
    }
    if request.method == 'POST':
        if form.is_valid():
            year = form.cleaned_data.get('year')
            max_age = form.cleaned_data.get('max_age')
            min_age = form.cleaned_data.get('min_age')
            if max_age < min_age:
                messages.error(request, "Could Not Update")
                return render(request, "admin_template/capNhatTuoi.html", context)
            else:
                try:
                    Year = Age.objects.get(id=age.id)
                    Year.year = year
                    Year.max_age = max_age
                    Year.min_age = min_age
                    Year.save()
                    messages.success(request, "Cập nhật thành công")
                    return redirect(reverse('quanLiTuoi'))
                except Exception as e:
                    messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Hãy điều đầy đủ vào ô thông tin !!!")
    else:
        return render(request, "admin_template/capNhatTuoi.html", context)


@allowed_users(allowed_roles=['Admin'])
def xoaTuoi(request, age_id):
    age = get_object_or_404(Age, id=age_id)
    age.delete()
    messages.success(request, "Age deleted successfully!")
    return redirect(reverse('quanLiTuoi'))


@allowed_users(allowed_roles=['Admin'])
def themTuoi(request):
    form = ageForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'themTuoi'
    }
    if request.method == 'POST':
        if form.is_valid():
            year = form.cleaned_data.get('year')
            max_age = form.cleaned_data.get('max_age')
            min_age = form.cleaned_data.get('min_age')
            if max_age < min_age:
                messages.error(request, "Could Not Add")
                render(request, 'admin_template/themTuoi.html', context)
            else:
                try:
                    Year = Age()
                    Year.year = year
                    Year.max_age = max_age
                    Year.min_age = min_age
                    Year.save()
                    messages.success(request, "Successfully Added")
                    return redirect(reverse('quanLiTuoi'))
                except:
                    messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Lỗi định dạng")
    return render(request, 'admin_template/themTuoi.html', context)


@allowed_users(allowed_roles=['Admin'])
def quanLiLop(request):
    classes = ClassOfSchool.objects.all()
    yearFilter = YearFilter(request.GET, queryset=classes)
    classes = yearFilter.qs
    context = {
        'classes': classes,
        'yearFilter': yearFilter
    }
    return render(request, 'admin_template/quanLiLop.html', context=context)


@allowed_users(allowed_roles=['Admin'])
def capNhatLop(request, class_id):
    Class = get_object_or_404(ClassOfSchool, id=class_id)
    form = classForm(request.POST or None, instance=Class)
    context = {
        'form': form,
        'page_title': 'capNhatLop'
    }
    if request.method == 'POST':
        if form.is_valid():
            classId = form.cleaned_data.get('classId')
            year = form.cleaned_data.get('year')
            max_number = form.cleaned_data.get('max_number')
            print(classId)
            if len(classId) > 10:
                messages.error(request, "Tên lớp quá dài")
            elif len(classId) ==0:
                messages.error(request, "Tên lớp quá ngắn")
            try:
                Class = ClassOfSchool.objects.get(id=Class.id)
                Class.ClassId = classId
                Class.year = year
                Class.max_number = max_number
                Class.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(reverse('quanLiLop'))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Hãy điều đầy đủ vào ô thông tin !!!")
    else:
        return render(request, "admin_template/capNhatLop.html", context)


@allowed_users(allowed_roles=['Admin'])
def xoaLop(request, class_id):
    Class = get_object_or_404(ClassOfSchool, id=class_id)
    Class.delete()
    messages.success(request, "Class deleted successfully!")
    return redirect(reverse('quanLiLop'))


@allowed_users(allowed_roles=['Admin'])
def themLop(request):
    form = classForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'themLop'
    }
    if request.method == 'POST':
        if form.is_valid():
            classId = form.cleaned_data.get('classId')
            year = form.cleaned_data.get('year')
            max_number = form.cleaned_data.get('max_number')
            try:
                Class = ClassOfSchool()
                Class.classId = classId
                Class.year = year
                Class.max_number = max_number
                Class.save()
                messages.success(request, "Thêm thành công")
                return redirect(reverse('quanLiLop'))
            except:
                messages.error(request, "Không thể thêm")
        else:
            messages.error(request, "Lỗi định dạng")
    return render(request, 'admin_template/themLop.html', context)


@allowed_users(allowed_roles=['Admin'])
def quanLiMon(request):
    subjects = Subject.objects.all()
    subjectWithYearFilter = SubjectWithYearFilter(request.GET, queryset=subjects)
    subjects = subjectWithYearFilter.qs
    context = {
        'subjects': subjects,
        'subjectWithYearFilter': subjectWithYearFilter,
    }
    return render(request, 'admin_template/quanLiMon.html', context)


@allowed_users(allowed_roles=['Admin'])
def capNhatMon(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    form = subjectForm(request.POST or None, instance=subject)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'capNhatMon'
    }
    if request.method == 'POST':
        if form.is_valid():
            subjectId = form.cleaned_data.get('SubjectID')
            name = form.cleaned_data.get('name')
            approved_mark = form.cleaned_data.get('approved_mark')
            try:
                subject = Subject.objects.get(id=subject.id)
                subject.SubjectID = subjectId
                subject.name = name
                subject.approved_mark = approved_mark
                subject.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(reverse('quanLiMon'))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Hãy điều đầy đủ vào ô thông tin !!!")
    else:
        return render(request, "admin_template/capNhatMon.html", context)


@allowed_users(allowed_roles=['Admin'])
def xoaMon(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully!")
    return redirect(reverse('quanLiMon'))


@allowed_users(allowed_roles=['Admin'])
def themMon(request):
    form = subjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'themMon'
    }
    if request.method == 'POST':
        if form.is_valid():
            SubjectID = form.cleaned_data.get('SubjectID')
            if len(SubjectID) > 10 : 
                messages.error(request, "Quá dài")
                return render(request, 'admin_template/themMon.html', context)
            name = form.cleaned_data.get('name')
            approved_mark = form.cleaned_data.get('approved_mark')
            year = form.cleaned_data.get('year')
            try:
                subject = Subject()
                subject.SubjectID = SubjectID
                subject.name = name
                subject.approved_mark = approved_mark
                subject.year = Age.objects.get(year=year)
                subject.save()
                # thêm điểm vào tất cả học sinh có trong hệ thống
                students = Student.objects.all()
                for student in students:
                    for semester_mark in range(1, semester + 1):
                        mark = Mark()
                        mark.student = student
                        mark.subject = subject
                        mark.semester_mark = semester_mark
                        mark.markFifteen = 0
                        mark.markOne = 0
                        mark.markFinal = 0
                        mark.save()
                messages.success(request, "Thêm thành công")
                return redirect(reverse('quanLiMon'))
            except:
                messages.error(request, "không thể thêm")
        else:
            messages.error(request, "Lỗi định dạng")
    return render(request, 'admin_template/themMon.html', context)




@allowed_users(allowed_roles=['Admin'])
def dsTaiKhoanHS(request):
    accountsStudent = Student.objects.all()
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in accountsStudent]
    accounts = zip(accountsStudent, formatDate)
    context = {
        'accounts': accounts,
    }
    return render(request, 'admin_template/dsTaiKhoanHS.html', context=context)



@allowed_users(allowed_roles=['Admin'])
def capNhatTKHS(request,account_id):
    account = get_object_or_404(Student, id=account_id)
    user = get_object_or_404(CustomUser, id=account.user.id)
    form = updateCustomUserForm(request.POST or None, instance=user)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            try:
                account = Student.objects.get(id=account.id)
                user = CustomUser.objects.get(id = account.user.id)
                user.username = username
                user.name = name
                user.dateOfBirth = dateOfBirth
                user.sex = sex
                user.email = email
                user.phone = phone
                user.address = address
                user.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(to='dsTaiKhoanHS')
            except:
                messages.error(request, "Không thể Không thể cập nhật")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    else:
        return render(request, "admin_template/capNhatHS.html", context)



@allowed_users(allowed_roles=['Admin'])
def xoaTKHS(request, account_id):
    account = get_object_or_404(Student, id=account_id)
    user = CustomUser.objects.get(username = account.user.username)
    user.delete()
    messages.success(request, "Xóa thành công !")
    return redirect(reverse('dsTaiKhoanHS'))


@allowed_users(allowed_roles=['Admin'])
def dsTaiKhoanGV(request):
    accountsTeacher = Teacher.objects.all()
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in accountsTeacher]
    classes = []
    for a in accountsTeacher:
        classes.append([c.classId for c in a.classOfSchool.all()])

    accounts = zip(accountsTeacher, formatDate, classes)
    context = {
        'accounts': accounts,
    }
    return render(request, 'admin_template/dsTaiKhoanGV.html', context=context)


@allowed_users(allowed_roles=['Admin'])
def capNhatTKGV(request,account_id):
    account = get_object_or_404(Teacher, id=account_id)
    user = get_object_or_404(CustomUser, id=account.user.id)
    form = updateCustomUserForm(request.POST or None, instance=user)
    formTeacher = ClassTeacherForm(request.POST or None, instance=account)
    context = {
        'form': form,
        'formTeacher': formTeacher,
    }
    if request.method == 'POST':
        print(form.is_valid(),formTeacher.is_valid())
        if form.is_valid() and formTeacher.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            subject = formTeacher.cleaned_data.get('subject')
            classOfSchool = formTeacher.cleaned_data.get('classOfSchool')
            try:
                account = Teacher.objects.get(id=account.id)
                user = CustomUser.objects.get(id = account.user.id)
                user.username = username
                user.name = name
                user.dateOfBirth = dateOfBirth
                user.sex = sex
                user.email = email
                user.phone = phone
                user.address = address
                user.save()
                if subject:
                    account.subject = subject
                account.save()
                for c  in classOfSchool:
                    account.classOfSchool.add(c)
                account.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(to='dsTaiKhoanGV')
            except:
                messages.error(request, "Không thể Không thể cập nhật")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    else:
        return render(request, "admin_template/capNhatGV.html", context)



@allowed_users(allowed_roles=['Admin'])
def xoaTKGV(request, account_id):
    account = get_object_or_404(Teacher, id=account_id)
    user = CustomUser.objects.get(username = account.user.username)
    user.delete()
    messages.success(request, "Xóa thành công !")
    return redirect(reverse('dsTaiKhoanGV'))


@allowed_users(allowed_roles=['Admin'])
def dsTaiKhoanAdmin(request):
    accountsAdmin = Admin.objects.all()
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in accountsAdmin]
    accounts = zip(accountsAdmin, formatDate)
    context = {
        'accounts': accounts,
    }
    return render(request, 'admin_template/dsTaiKhoanAdmin.html', context=context)


@allowed_users(allowed_roles=['Admin'])
def capNhatTKAdmin(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    user = get_object_or_404(CustomUser, id=account.user.id)
    form = updateCustomUserForm(request.POST or None, instance=user)
    context = {
        'form': form,
        'account_id': account_id,
    }
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            dateOfBirth = form.cleaned_data.get('dateOfBirth')
            sex = form.cleaned_data.get('sex')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            try:
                account = Admin.objects.get(id=account.id)
                user = CustomUser.objects.get(id=account.user.id)
                user.username = username
                user.name = name
                user.dateOfBirth = dateOfBirth
                user.sex = sex
                user.email = email
                user.phone = phone
                user.address = address
                user.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(to='dsTaiKhoanAdmin')
            except:
                messages.error(request, "Không thể Không thể cập nhật")
        else:
            messages.error(request, "Dữ liệu không phù hợp")
    else:
        return render(request, "admin_template/capNhatAdmin.html", context)


@allowed_users(allowed_roles=['Admin'])
def xoaTKAdmin(request, account_id):
    account = get_object_or_404(Admin, id=account_id)
    user = CustomUser.objects.get(username = account.user.username)
    user.delete()
    messages.success(request, "Xóa thành công !")
    return redirect(reverse('dsTaiKhoanAdmin'))


# Teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['Teacher'])
def bangDiemGVFilter(request, lop,hocKy, nienKhoa):
    mark_query = []
    classes = []
    years = []
    teacher = Teacher.objects.get(user = request.user)
    for c in teacher.classOfSchool.all():
        classes.append(c.classId) 
        years.append(c.year)
        mark_query.append(Mark.objects.filter(subject=teacher.subject).filter(student__classOfSchool__classId=c.classId))
    marks = mark_query[0]
    for i in range(1,len(mark_query)):
        marks = marks | mark_query[i]

    if lop != '---':
        marks = marks.filter(student__classOfSchool__classId = lop)
    if hocKy != '---':
        marks = marks.filter(semester_mark = hocKy)
    if nienKhoa != '---':
        marks = marks.filter(subject__year__year = nienKhoa)

    context = {
        'marks': marks,
        'classes': classes,
        'years': years,
        'current_class': lop,
        'semester': hocKy,
        'year': nienKhoa,
    }
    return render(request, 'teacher_template/bangDiemGV.html', context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Teacher'])
def bangDiemGV(request):
    return bangDiemGVFilter(request, '---', '---', '---')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Teacher'])
def capNhatDiem(request, mark_id):
    mark = get_object_or_404(Mark, id=mark_id)
    form = transcriptForm(request.POST or None, instance=mark)
    context = {
        'form': form,
        'mark_id': mark_id,
        'page_title': 'capNhatDiem'
    }
    if request.method == 'POST':
        if form.is_valid():
            markFifteen = form.cleaned_data.get('markFifteen')
            markOne = form.cleaned_data.get('markOne')
            markFinal = form.cleaned_data.get('markFinal')

            try:
                mark = Mark.objects.get(id=mark.id)
                mark.markFifteen = markFifteen
                mark.markOne = markOne
                mark.markFinal = markFinal
                mark.save()
                messages.success(request, "Cập nhật thành công")
                return redirect(reverse('bangDiemGV'))
            except Exception as e:
                messages.error(request, "Không thể cập nhật " + str(e))
        else:
            messages.error(request, "Hãy điều đầy đủ vào ô thông tin !!!")
    else:
        return render(request, "teacher_template/capNhatDiem.html", context)

# Student
@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def bangDiemHSFilter(request, lop, mon, hocKy, nienKhoa):
    marks = Mark.objects.filter(student__user=request.user)
    if lop != '---':
        marks = marks.filter(student__classOfSchool__classId = lop)
    if mon != '---':
        marks = marks.filter(subject__name = mon)
    if hocKy != '---':
        marks = marks.filter(semester_mark = hocKy)
    if nienKhoa != '---':
        marks = marks.filter(subject__year__year = nienKhoa)
    student = Student.objects.get(user = request.user)
    classes = [c.classId for c in student.classOfSchool.all()]
    subjects = set([ m.subject for m in marks])
    years = [c.year for c in student.classOfSchool.all()]
    context = {
        'marks': marks,
        'classes': classes,
        'subjects': subjects,
        'years': years,
        'current_class': lop,
        'semester': hocKy,
        'year': nienKhoa,
        'subject': mon,
    }
    return render(request, 'student_template/bangDiemHS.html', context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])
def bangDiemHS(request):
    return bangDiemHSFilter(request, '---', '---', '---', '---')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Student'])

def dsLopHSFilter(request, lop):
    user = Student.objects.get(user=request.user)
    classofuser = user.classOfSchool.all()
    stds = []
    listStd = Student.objects.all().order_by('user__name')
    for c in classofuser:
        for std in listStd:
            if c in std.classOfSchool.all():
                stds.append(std.id)
    resultStd=Student.objects.filter(pk__in=stds)
    print(lop)
    if lop != '---':
        resultStd = resultStd.filter(classOfSchool__classId = lop)
    formatDate = [a.user.dateOfBirth.strftime("%d-%m-%y") for a in resultStd]
    context = {
        'resultStd': zip(resultStd,formatDate),
        'current_class': lop,
        'classofuser': classofuser,

    }
    return render(request, 'student_template/dsLopHS.html', context=context)

def dsLopHS(request):
    return dsLopHSFilter(request, '---')
