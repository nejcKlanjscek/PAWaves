from django import forms

class MultiplierForm(forms.Form):
    ibias = forms.FloatField(label='ibias', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i1 = forms.FloatField(label='i1', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i2 = forms.FloatField(label='i2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i3 = forms.FloatField(label='i3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i4 = forms.FloatField(label='i4', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i5 = forms.FloatField(label='i5', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i6 = forms.FloatField(label='i6', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    i7 = forms.FloatField(label='i7', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))


    vknee = forms.FloatField(label='vknee', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    vdc = forms.FloatField(label='vdc', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    vmin = forms.CharField(label='vmin', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    mag_v1 = forms.FloatField(label='mag_v1', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v2 = forms.FloatField(label='mag_v2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v3 = forms.FloatField(label='mag_v3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v4 = forms.FloatField(label='mag_v4', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v5 = forms.FloatField(label='mag_v5', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v6 = forms.FloatField(label='mag_v6', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    mag_v7 = forms.FloatField(label='mag_v7', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))

    ang_v1 = forms.FloatField(label='ang_v1', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v2 = forms.FloatField(label='ang_v2', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v3 = forms.FloatField(label='ang_v3', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v4 = forms.FloatField(label='ang_v4', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v5 = forms.FloatField(label='ang_v5', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v6 = forms.FloatField(label='ang_v6', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))
    ang_v7 = forms.FloatField(label='ang_v7', required=False, widget=forms.NumberInput(attrs={'step': 'any', 'class': 'form-control'}))

    output_format = forms.ChoiceField(choices=[('svg', 'SVG'),('png', 'PNG')], label='Graph Save Format', widget=forms.Select(attrs={'class': 'form-select'}), initial='svg')
    preset = forms.ChoiceField(choices=[('A', 'Class A'), ('AB', 'Class AB'),('B', 'Class B'),('C', 'Class C'), ('F', 'Class F'), ('custom', 'Custom')], label='Graph Save Format', widget=forms.Select(attrs={'class': 'form-select'}), initial='A')

