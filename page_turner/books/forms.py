from django import forms

from .models import Book


class BookForm(forms.ModelForm):

    class Meta:
        
        model = Book
        
        exclude = ['uuid', 'active_status', 'created_at', 'updated_at']

        widgets = {
                    'title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Book Title'}),

                    'author': forms.Select(attrs={'class': 'form-select'}),

                    'genres': forms.SelectMultiple(attrs={'class': 'form-select'}),

                    'language': forms.Select(attrs={'class': 'form-select'}),

                    'description': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Book Description','rows': 4}),

                    'has_digital': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

                    'digital_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),

                    'has_physical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

                    'total_copies': forms.NumberInput(attrs={'class': 'form-control','min': 0}),
                    
                    'available_copies': forms.NumberInput(attrs={'class': 'form-control','min': 0}),

                    'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
                
                }
