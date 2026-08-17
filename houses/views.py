from django.shortcuts import render, redirect, get_object_or_404

from .models import House, HouseImage, Reservation
from .forms import HouseForm, ReservationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):

    houses = House.objects.all()
    search = request.GET.get("search")

    if search:

        houses = houses.filter(
            Q(title__icontains=search) | Q(location__icontains=search)
        )

    return render(
        request,
        "home.html",
        {
            "houses": houses,
        },
    )


@login_required
def house_create(request):

    if request.method == "POST":

        form = HouseForm(request.POST, request.FILES)

        if form.is_valid():

            house = form.save(commit=False)
            house.owner = request.user
            house.save()

            additional_images = form.cleaned_data.get(
                "additional_images",
                []
            )

            for image in additional_images:
                HouseImage.objects.create(
                    house=house,
                    image=image
                )

            return redirect("host")

    else:
        form = HouseForm()

    return render(
        request,
        "houses/house_form.html",
        {
            "form": form,
        },
    )

@login_required
def house_update(request, pk):

    house = get_object_or_404(
        House,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":

        form = HouseForm(
            request.POST,
            request.FILES,
            instance=house
        )

        if form.is_valid():

            form.save()

            additional_images = form.cleaned_data.get(
                "additional_images",
                []
            )

            for image in additional_images:

                HouseImage.objects.create(
                    house=house,
                    image=image
                )

            return redirect(
                "house_detail",
                pk=house.pk
            )

    else:

        form = HouseForm(
            instance=house
        )

    return render(
    request,
    "houses/house_form.html",
    {
        "form": form,
        "house": house
    }
)

@login_required
def house_image_delete(request, pk):

    image = get_object_or_404(
        HouseImage,
        pk=pk,
        house__owner=request.user
    )

    house_pk = image.house.pk

    if request.method == "POST":
        image.image.delete(save=False)
        image.delete()

    return redirect(
        "house_update",
        pk=house_pk
    )

@login_required
def house_reserve(request, pk):

    house = get_object_or_404(House, pk=pk)

    if request.method == "POST":

        form = ReservationForm(
            request.POST,
            house=house
        )

        if form.is_valid():

            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]

            overlapping_reservation = Reservation.objects.filter(
                house=house,
                status=Reservation.Status.CONFIRMED,
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exists()

            if overlapping_reservation:

                form.add_error(
                    None,
                    "This house is not available for these dates."
                )

            else:

                reservation = form.save(commit=False)

                reservation.house = house
                reservation.guest = request.user
                reservation.status = Reservation.Status.CONFIRMED

                reservation.save()

                return redirect(
                    "house_detail",
                    pk=house.pk
                )

    else:

        form = ReservationForm(
            house=house
        )

    return render(
        request,
        "houses/house_reserve.html",
        {
            "house": house,
            "form": form,
        }
    )

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(
        guest=request.user
    ).select_related("house").order_by("-check_in")

    return render(
        request,
        "houses/my_reservations.html",
        {
            "reservations": reservations,
        }
    )

@login_required
def host_reservations(request):

    reservations = Reservation.objects.filter(
        house__owner=request.user
    ).select_related(
        "house",
        "guest"
    ).order_by("-check_in")

    return render(
        request,
        "houses/my_reservations.html",
        {
            "reservations": reservations,
            "mode": "host",
        }
    )

def house_detail(request, pk):

    house = get_object_or_404(House, pk=pk)

    return render(
        request,
        "houses/house_detail.html",
        {
            "house": house,
        },
    )