from django import forms
from tasks.models import Task,TaskDetail

# Django Form


# class TaskForm(forms.Form):
#     title = forms.CharField(max_length=250, label="Task Title")
#     description = forms.CharField(
#         widget=forms.Textarea, label='Task Description')
#     due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
#     assigned_to = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')

#     def __init__(self, *args, **kwargs):
#         # print(args, kwargs)
#         employees = kwargs.pop("employees", [])
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].choices = [
#             (emp.id, emp.name) for emp in employees]


# class StyledFormMixin:
#     """ Mixing to apply style to form field"""

#     default_classes = "text-black border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"

#     def apply_styled_widgets(self):
#         for field_name, field in self.fields.items():
#             if isinstance(field.widget, forms.TextInput):
#                 field.widget.attrs.update({
#                     'class': self.default_classes,
#                     'placeholder': f"Enter {field.label.lower()}"
#                 })
#             elif isinstance(field.widget, forms.Textarea):
#                 field.widget.attrs.update({
#                     'class': f"{self.default_classes} resize-none",
#                     'placeholder':  f"Enter {field.label.lower()}",
#                     'rows': 5
#                 })
#             elif isinstance(field.widget, forms.SelectDateWidget):

#                 field.widget.attrs.update({
#                     "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"
#                 })
#             elif isinstance(field.widget, forms.CheckboxSelectMultiple):
       
#                 field.widget.attrs.update({
#                     'class': "space-y-2"
#                 })
#             elif isinstance(field.widget,forms.Select):
#                 field.widget.attrs.update({
#                     'class':"border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500 mt-3"
#                 })
#             else:
           
#                 field.widget.attrs.update({
#                     'class': self.default_classes
#                 })

class StyledFormMixin:
    """Mixin to apply style to form fields"""

    default_classes = "text-black border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():

            # ----- TextInput -----
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })

            # ----- Textarea -----
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })

            # ----- SelectDateWidget -----
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500"
                })

            # ----- CheckboxSelectMultiple -----
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })

            # ----- Select -----
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-green-500 focus:ring-rose-500 mt-3"
                })

            #  ----- Image / File Input -----
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class': "block w-full text-sm text-gray-700 border-2 border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-green-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-100 file:text-green-700 hover:file:bg-green-200",
                })

            # ----- Default case -----
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


# Django Model Form


class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

    """ Widget using mixins """

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
     


class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes','asset']

        widgets={
            'priority':forms.Select
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()
