from django import forms

PRODUCT_QUATITY_CHIOCES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUATITY_CHIOCES, 
        coerce=int
    )
    update = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )
