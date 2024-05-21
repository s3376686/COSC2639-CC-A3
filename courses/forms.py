from django import forms
from .models import Course
from .models import StudyMaterial

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'instructor', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }



class StudyMaterialForm(forms.ModelForm):
    # Display-only field for the course name
    course_name = forms.CharField(max_length=255, required=False, disabled=True, label="Course")
    file = forms.FileField(required=False)
    class Meta:
        model = StudyMaterial
        fields = ['course_name', 'title', 'description']  

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Optionally receive the course instance when initializing the form
        self.course = kwargs.pop('course', None)
        super(StudyMaterialForm, self).__init__(*args, **kwargs)
        
        # Initialize the course_name field if a course is provided
        if self.course:
            self.fields['course_name'].initial = self.course.name
