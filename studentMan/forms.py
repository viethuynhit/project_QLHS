from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class transcriptForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester_mark'].widget.attrs.update(
            {'class': 'form-select'}
        )


class CreateClassForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        self.age_id = kwargs.pop('age_id', None)
        super(CreateClassForm,self).__init__(*args,**kwargs)
        age = Age.objects.get(id =self.age_id)
        class_choices = set([(c.classId, c.classId) for c in ClassOfSchool.objects.filter(year = age)])
        self.fields['classId'].label = ''
        self.fields['classId'].widget=forms.Select(
            choices=class_choices, 
            attrs={'class': 'form-select'
            
        })

    class Meta:
        model = ClassOfSchool
        fields = ['classId']


class classForm(forms.ModelForm):
    class Meta:
        model = ClassOfSchool
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(classForm, self).__init__(*args, **kwargs)
        self.fields['classId'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['year'].widget.attrs.update({'class': 'form-select'})


class ageForm(forms.ModelForm):
    class Meta:
        model = Age
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ageForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_age'].widget.attrs.update({'class': 'form-control'})
        self.fields['min_age'].widget.attrs.update({'class': 'form-control'})

class YearForm(forms.ModelForm):
    try:
        year_choices = set([(a, a.year) for a in Age.objects.all()])
        year = forms.CharField(label="",widget=forms.Select(
            choices=year_choices, 
            attrs={'class': 'form-select'
        }))
    except:
        ''''''
    class Meta:
        model = Age
        fields = ['year']


class CustomUserForm(forms.ModelForm):
    try:
        username = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':"username_user", 'class':"form-control"
        }))

        password = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':"password_user", 'class':"form-control"
        }))

        name = forms.CharField(label='', widget=forms.TextInput(
            attrs={'id':"name_user", 'class':"form-control"
        }))
        dateOfBirth = forms.CharField(label="",widget=forms.DateInput(
            attrs={'type': 'date', 'id':"datepicker", 'class': 'form-control' 
        }))

        sex = forms.CharField(label="",widget=forms.Select(
            choices=CustomUser().SEX_CATELOGY, 
            attrs={'class': 'form-select', 'id': 'sex_user'
        }))

        email = forms.CharField(label="",widget=forms.TextInput(
            attrs={'type': 'email', 'id':'email_user', 'class': 'form-control',
        }))

        address = forms.CharField(label="",widget=forms.Textarea(
            attrs={"rows":4, 'class': 'form-control', 'id': 'address_user', 
                'placeholder':"12, đường 01, quận 1, tp HCM"
        }))


        phone = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':'phone_user', 'class': 'form-control',
        }))
    except:
        ''''''
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserForm, self).__init__(*args, **kwargs)
    #     if kwargs.get('instance'):
    #         instance = kwargs.get('instance').admin.__dict__
    #         self.fields['password'].required = False
    #         for field in CustomUserForm.Meta.fields:
    #             self.fields[field].initial = instance.get(field)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name', 'dateOfBirth', 'sex', 'email','address', 'phone']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Admin
        fields = CustomUserForm.Meta.fields



class TeacherForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['subject'].required = False
        self.fields['classOfSchool'].required = False
        self.fields['subject'].widget.attrs.update({'class': 'form-select'})
        self.fields['classOfSchool'].widget.attrs.update({'class': 'form-select'})
    class Meta:
        model = Teacher
        fields = CustomUserForm.Meta.fields +  ['subject', 'classOfSchool']


class StudentForm(CustomUserForm):
    try:
        class_choices = {(None, '-----')}
        class_choices.update(set([(c.classId, c.classId) for c in ClassOfSchool.objects.all()]))
        classOfSchool = forms.CharField(label="",widget=forms.Select(
            choices=class_choices, 
            attrs={'class': 'form-select'
        }), required = False)
    except:
        ''''''
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['classOfSchool'].required = False
        self.fields['classOfSchool'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Student
        fields = CustomUserForm.Meta.fields +  ['classOfSchool']
        # widgets = {
        #     'classOfSchool': forms.Select()
        # }

class subjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(subjectForm, self).__init__(*args, **kwargs)
        self.fields['SubjectID'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['approved_mark'].widget.attrs.update({'class': 'form-control'})
        self.fields['year'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Subject
        fields = YearForm.Meta.fields + ['SubjectID', 'name', 'approved_mark']

class userUpdateForm(forms.ModelForm):
    try:
        name = forms.CharField(label='', widget=forms.TextInput(
            attrs={'id':"name_user", 'class':"form-control"
        }))
        dateOfBirth = forms.CharField(label="",widget=forms.DateInput(
            attrs={'type': 'date', 'id':"datepicker", 'class': 'form-control' 
        }))

        sex = forms.CharField(label="",widget=forms.Select(
            choices=CustomUser().SEX_CATELOGY, 
            attrs={'class': 'form-select', 'id': 'sex_user'
        }))

        email = forms.CharField(label="",widget=forms.TextInput(
            attrs={'type': 'email', 'id':'email_user', 'class': 'form-control',
        }))

        address = forms.CharField(label="",widget=forms.Textarea(
            attrs={"rows":4, 'class': 'form-control', 'id': 'address_user', 
                'placeholder':"12, đường 01, quận 1, tp HCM"
        }))


        phone = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':'phone_user', 'class': 'form-control',
        }))
    except:
        ''''''
    class Meta:
        model = CustomUser
        fields = ('name', 'dateOfBirth', 'sex', 'phone', 'email', 'address')


class updateCustomUserForm(forms.ModelForm):
    try:
        username = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':"username_user", 'class':"form-control"
        }))

        name = forms.CharField(label='', widget=forms.TextInput(
            attrs={'id':"name_user", 'class':"form-control"
        }))
        dateOfBirth = forms.CharField(label="",widget=forms.DateInput(
            attrs={'type': 'date', 'id':"datepicker", 'class': 'form-control' 
        }))

        sex = forms.CharField(label="",widget=forms.Select(
            choices=CustomUser().SEX_CATELOGY, 
            attrs={'class': 'form-select', 'id': 'sex_user'
        }))

        email = forms.CharField(label="",widget=forms.TextInput(
            attrs={'type': 'email', 'id':'email_user', 'class': 'form-control',
        }))

        address = forms.CharField(label="",widget=forms.Textarea(
            attrs={"rows":4, 'class': 'form-control', 'id': 'address_user', 
                'placeholder':"12, đường 01, quận 1, tp HCM"
        }))


        phone = forms.CharField(label="",widget=forms.TextInput(
            attrs={'id':'phone_user', 'class': 'form-control',
        }))
    except:
        ''''''
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'dateOfBirth', 'sex', 'email','address', 'phone']


class ClassTeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassTeacherForm, self).__init__(*args, **kwargs)
        self.fields['subject'].required = False
        self.fields['classOfSchool'].required = False
        self.fields['subject'].widget.attrs.update({'class': 'form-select'})
        self.fields['classOfSchool'].widget.attrs.update({'class': 'form-select'})
    class Meta:
        model = Teacher
        fields = ['subject', 'classOfSchool']