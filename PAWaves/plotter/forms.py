from django import forms

class MultiplierForm(forms.Form):
    ibias = forms.FloatField(label='ibias', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    isig = forms.FloatField(label='isig', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i2 = forms.FloatField(label='i2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i3 = forms.FloatField(label='i3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))

    vknee = forms.FloatField(label='vknee', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    vdc = forms.FloatField(label='vdc', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    vmin = forms.CharField(label='vmin', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    mag_v1 = forms.FloatField(label='mag_v1', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v2 = forms.FloatField(label='mag_v2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v3 = forms.FloatField(label='mag_v3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v1 = forms.FloatField(label='ang_v1', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v2 = forms.FloatField(label='ang_v2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v3 = forms.FloatField(label='ang_v3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))

    output_format = forms.ChoiceField(choices=[('svg', 'SVG'),('png', 'PNG')], label='Graph Save Format', widget=forms.Select(attrs={'class': 'form-select'}), initial='svg')
    preset = forms.ChoiceField(choices=[('A', 'Class A'),('B', 'Class B'), ('AB', 'Class AB'),('C', 'Class C'), ('E', 'Class E'), ('F', 'Class F'), ('custom', 'Custom')], label='Graph Save Format', widget=forms.Select(attrs={'class': 'form-select'}), initial='A')

