from django.shortcuts import render
from houses.models import House
from django.contrib.auth.decorators import login_required

def home(request):

    houses = House.objects.all()

    location = request.GET.get("location")
    guests = request.GET.get("guests")

    if location:
        houses = houses.filter(
            location__icontains=location
        )

    if guests:
        houses = houses.filter(
            guests__gte=guests
        )

    return render(
        request,
        "home.html",
        {
            "houses": houses,
        }
    )

@login_required
def host(request):
    houses = House.objects.filter(
        owner=request.user
    )

    return render(
        request,
        "dashboard/host.html",
        {
            "houses": houses,
        }
    )