# class FerroForm(forms.ModelForm):
#     class Meta:
#         model = Ferro
#         fields = ['nombre', 'descripcion', 'tipo', 'peso', 'dimensiones', 'fecha_creacion']
#         widgets = {
#             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
#             'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
#             'tipo': forms.Select(attrs={'class': 'form-control'}),
#             'peso': forms.NumberInput(attrs={'class': 'form-control'}),
#             'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
#             'fecha_creacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         }