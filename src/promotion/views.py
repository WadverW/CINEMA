from django.shortcuts import render


# Create your views here.
def promos(request):
    return render(request, "promotion/promos.html")
