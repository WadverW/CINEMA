from django.shortcuts import render


def booking_view(request):
    rows = list(range(1, 11))
    seats = list(range(1, 16))
    context = {"rows": rows, "seats": seats}
    return render(request, "booking/booking.html", context)
