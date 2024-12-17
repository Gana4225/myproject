from django.shortcuts import render,HttpResponse
from django.http import request
import razorpay
from .models import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.method == "POST":
        name = request.POST.get("nm")
        at = request.POST.get("amt")
        amount= int(at)*100
        client = razorpay.Client(auth=("rzp_test_fdXm1LWL9qmt0N","7uhH9YraGtUn5tGMthG20A6L"))
        payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        coffee = coff(name=name,amount=amount,pid=payment['id'])
        coffee.save()
        return render(request,"index.html",{'payment':payment})
    return render(request,"index.html")
@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key , val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                user = coff.objects.filter(pid=order_id).first()
                user.paid = True
                user.save()
    return render (request,"status.html")
