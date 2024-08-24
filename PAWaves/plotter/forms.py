from django import forms

# Define a form class for user input
class MultiplierForm(forms.Form):
    
    # A floating-point field for the multiplier input
    multiplier = forms.FloatField(
        label='Multiplier',  # Label for the form field, displayed next to the input box
        widget=forms.NumberInput(attrs={
            'step': 'any'  # Allows the input to accept any floating-point number (including decimals)
        })
    )
    
    # A choice field for selecting the output format (PNG or SVG)
    format = forms.ChoiceField(
        choices=[('png', 'PNG'), ('svg', 'SVG')],  # The available choices: ('value', 'label')
        label='Output Format'  # Label for the form field, indicating the user should select the output format
    )
