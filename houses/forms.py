from django import forms
from .models import House, Reservation

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            MultipleFileInput()
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):

        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):

            return [
                single_file_clean(file, initial)
                for file in data
            ]

        return [
            single_file_clean(data, initial)
        ]


class HouseForm(forms.ModelForm):

    additional_images = MultipleImageField(
        required=False,
        label="Additional photos",
        widget=MultipleFileInput(
            attrs={
                "accept": "image/*"
            }
        )
    )

    class Meta:
        model = House

        fields = [
            "title",
            "description",
            "location",
            "price",
            "bedrooms",
            "bathrooms",
            "guests",
            "image",
        ]

        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*"
                }
            ),
        }

class ReservationForm (forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

        widgets = {
            "check_in": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "check_out": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),
        }

    def __init__(self, *args, house=None, **Kwargs):
        super().__init__(*args, **Kwargs)
        self.house = house

        if house:
            self.fields["guests"].widget.attrs["max"] = house.guests

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        guests = cleaned_data.get("guests")

        if check_in and check_out:

            if check_out <= check_in:
                raise forms.ValidationError(
                    "Check-out must be after check-in."
                )

            if self.house and guests:

                if guests > self.house.guests:
                    raise forms.ValidationError(
                        f"This house allows a maximum of "
                        f"{self.house.guests} guests"
                    )

        return cleaned_data
