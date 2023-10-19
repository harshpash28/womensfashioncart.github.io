from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from fashioncartapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=='' or upass=='':
            context['errmsg']="fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            # print(u.username)
            if u is not None:
                login(request,u)#start session of this login user and store userid in session table
                return redirect('/home')
            else:
                context['errmsg']="invalid user and password"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/home')

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=='' or upass=='' or ucpass=='':
            context['errmsg']="fields cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="password did not match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="user already created"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def shopmore(request):
    context={}
    p=Product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'shopmore.html',context)

def hot(request):
    return render(request,'hot.html')

def newarrivals(request):
    return render(request,'newarrivals.html')

def accessories(request):
    return render(request,'accessories.html')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'shopmore.html',context)

def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'shopmore.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'shopmore.html',context)

def product_details(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['msg']="product already addded to cart"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            #context={}
            context['success']="product addedd successfully"
            context['products']=p
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    a=0
    for x in c:
        s = s+x.pid.price * x.qty
        a=len(c)
    context={}
    context['products']=c
    context['total']=s
    context['totalitems']=a
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv == '1':
        t = c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("orderid:",oid)
    print(c)
    for x in c:
        print(x)
        print(x.pid)
        print(x.uid)
        o=Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s = s+x.pid.price * x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['n']=np
    return render(request,'place_order.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s = s+x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(auth=("rzp_test_b1g8lWV0LfKKFi", "NlMFPzof3egNLSpqujtWlWmx"))
    data = { "amount": s * 100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)

def sendusermail(request):
    uemail=request.user.email
    send_mail(
    "Order Placed Successfully",
    "Order Details are:",
    "harshal.pashte28@gmail.com",
    [uemail],
    fail_silently=False,
)
    return HttpResponse("mail send successfully")
