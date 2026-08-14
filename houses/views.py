from django.shortcuts import render, redirect, get_object_or_404

from .models import House
from .forms import HouseForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):

    houses = House.objects.all()
    search = request.GET.get("search")

    if search:

        houses = houses.filter(
            Q(title__icontains=search) |
            Q(location__icontains=search)
        )

    return render(
        request,
        "home.html",
        {
            "houses": houses,
        }
    )

@login_required
def house_create(request):

    if request.method == "POST":

        form = HouseForm(request.POST, request.FILES)

        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user
            house.save()
            return redirect("host")

    else:
        form = HouseForm()

    return render(
        request,
        "houses/house_form.html",
        {
            "form": form,
        }
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
            return redirect("house_detail", pk=house.pk)

    else:
        form = HouseForm(instance=house)

    return render(
        request,
        "houses/house_form.html",
        {"form": form}
    )

def house_detail(request, pk):

    house = get_object_or_404(House, pk=pk)

    return render(
        request,
        "houses/house_detail.html",
        {
            "house": house,
        }
    )