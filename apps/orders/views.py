from django.http import HttpResponse

def orders_list(request):
    return HttpResponse("Orders list OK")

def order_detail(request, pk):
    return HttpResponse(f"Order detail OK: {pk}")
