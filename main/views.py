from time import sleep
import time
from django.contrib import messages, auth
import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
# Create your views here.
from main.models import Staff, Poll, ProductCategory, Product, Offer, Variant, PollResult, TgUser, Photos

BOT_TOKEN = "5479684297:AAGlqYSVymaRrohMiNL3nZbEQRxFJS0uln0"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
GET_PATH_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id="
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"

@login_required(login_url='/login')
def index(request):
    staff_complaint = Offer.objects.filter(~Q(user__role='deliverer'), rate__lt=3, user__isnull=False).count()
    staff_offer = Offer.objects.filter(~Q(user__role='deliverer'), rate__gte=3, user__isnull=False).count()
    deliverer_complaint = Offer.objects.filter(user__role='deliverer', rate__lt=3, user__isnull=False).count()
    deliverer_offer = Offer.objects.filter(user__role='deliverer', rate__gte=3, user__isnull=False).count()
    product_complaint = Offer.objects.filter(product__isnull=False, rate__lt=3).count()
    product_offer = Offer.objects.filter(product__isnull=False, rate__gte=3).count()

    total_staff = Offer.objects.filter(~Q(user__role='deliverer'), user__isnull=False).count()
    total_deliverer = Offer.objects.filter(user__role='deliverer', user__isnull=False).count()
    total_product = Offer.objects.filter(product__isnull=False, user__isnull=True).count()

    get_staff_complaint = Offer.objects.filter(~Q(user__role='deliverer'), rate__lt=3, user__isnull=False).order_by(
        'user__full_name').values('user__full_name').annotate(count=Count('user__id')).order_by('-count')[:5]
    get_staff_offer = Offer.objects.filter(~Q(user__role='deliverer'), rate__gte=3, user__isnull=False).order_by(
        'user__full_name').values('user__full_name').annotate(count=Count('user__id')).order_by('-count')[:5]
    get_deliverer_complaint = Offer.objects.filter(user__role='deliverer', rate__lt=3, user__isnull=False).order_by(
        'user__full_name').values('user__full_name').annotate(count=Count('user__id')).order_by('-count')[:5]
    get_deliverer_offer = Offer.objects.filter(user__role='deliverer', rate__gte=3, user__isnull=False).order_by(
        'user__full_name').values('user__full_name').annotate(count=Count('user__id')).order_by('-count')[:5]

    get_product_complaint = Offer.objects.filter(product__isnull=False, rate__lt=3).order_by(
        'product__name').values('product__name').annotate(count=Count('product__id')).order_by('-count')[:5]
    get_product_offer = Offer.objects.filter(product__isnull=False, rate__gte=3).order_by(
        'product__name').values('product__name').annotate(count=Count('product__id')).order_by('-count')[:5]
    context = {
        'staff_complaint': staff_complaint,
        'staff_offer': staff_offer,
        'deliverer_complaint': deliverer_complaint,
        'deliverer_offer': deliverer_offer,
        'product_complaint': product_complaint,
        'product_offer': product_offer,

        'total_staff': total_staff,
        'total_deliverer': total_deliverer,
        'total_product': total_product,

        'get_staff_complaint': get_staff_complaint,
        'get_staff_offer': get_staff_offer,
        'get_deliverer_complaint': get_deliverer_complaint,
        'get_deliverer_offer': get_deliverer_offer,
        'get_product_complaint': get_product_complaint,
        'get_product_offer': get_product_offer,
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def staff(request):
    if request.method == "POST":
        data = request.POST
        full_name = data['full_name']
        phone_number = data['phone_number']
        role = data['role']
        avatar = None
        if request.FILES.get('avatar', None):
            avatar = request.FILES['avatar']
        user = Staff.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            role=role,
            avatar=avatar,
        )
        return redirect("/staff")
    staffes = Staff.objects.filter(~Q(role="deliverer")).order_by('-id')
    paginator = Paginator(staffes, 10)
    page_number = request.GET.get('page')
    staffes_final = paginator.get_page(page_number)
    total_pages = staffes_final.paginator.num_pages
    context = {
        'staffes': staffes_final,
        "total_pages": [n + 1 for n in range(total_pages)],
    }
    return render(request, 'staff.html', context)

@login_required(login_url='/login')
def update_staff(request, pk):
    if request.method == "POST":
        data = request.POST
        id = data['id']
        full_name = data['full_name']
        phone_number = data['phone_number']
        role = data['role']
        avatar = None
        if request.FILES.get('avatar', None):
            avatar = request.FILES['avatar']
        staff = Staff.objects.get(id=id)
        staff.full_name = full_name
        staff.phone_number = phone_number
        staff.role = role
        if avatar:
            staff.avatar = avatar
        staff.save()
    staff = Staff.objects.get(id=pk)
    context = {
        "staff": staff
    }
    return render(request, "update_staff.html", context)

@login_required(login_url='/login')
def delete_staff(request, pk):
    staff = Staff.objects.get(id=pk).delete()
    return redirect("/staff")

@login_required(login_url='/login')
def deliverer(request):
    if request.method == "POST":
        data = request.POST
        full_name = data['full_name']
        phone_number = data['phone_number']
        car_brand = data['car_brand']
        car_color = data['car_color']
        car_number = data['car_number']
        # avatar = None
        # if request.FILES.get('avatar', None):
        #     avatar = request.FILES['avatar']
        user = Staff.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            role="deliverer",
            # avatar=avatar,
            car_brand=car_brand,
            car_color=car_color,
            car_number=car_number,
        )
        return redirect("/deliverer")

    staffes = Staff.objects.filter(role="deliverer").order_by('-id')
    paginator = Paginator(staffes, 10)
    page_number = request.GET.get('page')
    staff_final = paginator.get_page(page_number)
    total_pages = staff_final.paginator.num_pages
    context = {
        'staffes': staff_final,
        "total_pages": [n + 1 for n in range(total_pages)],
    }
    return render(request, 'deliverer.html', context)

@login_required(login_url='/login')
def update_deliverer(request, pk):
    if request.method == "POST":
        data = request.POST
        id = data['id']
        full_name = data['full_name']
        phone_number = data['phone_number']
        car_brand = data['car_brand']
        car_color = data['car_color']
        car_number = data['car_number']
        avatar = None
        if request.FILES.get('avatar', None):
            avatar = request.FILES['avatar']
        staff = Staff.objects.get(id=id)
        staff.full_name = full_name
        staff.phone_number = phone_number
        staff.car_brand = car_brand
        staff.car_color = car_color
        staff.car_number = car_number
        if avatar:
            staff.avatar = avatar
        staff.save()
    staff = Staff.objects.get(id=pk)
    context = {
        "staff": staff
    }
    return render(request, "update_deliverer.html", context)

@login_required(login_url='/login')
def update_product(request, pk):
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']

        image = None
        if request.FILES.get('image', None):
            image = request.FILES['image']
        product = Product.objects.get(id=pk)
        product.name = name
        product.category_id = category
        if image:
            product.image = image
        product.save()
    products = Product.objects.get(id=pk)
    categories = ProductCategory.objects.all()
    context = {
        "product": products,
        "categories": categories,
    }
    return render(request, "update_product.html", context)

@login_required(login_url='/login')
def offer(request):
    offers = Offer.objects.filter(rate__gt=3).order_by('-id')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    offers_final = paginator.get_page(page_number)
    total_pages = offers_final.paginator.num_pages
    context = {
        "offers": offers_final,
        "total_pages": [n + 1 for n in range(total_pages)],
    }
    return render(request, 'offers.html', context)

@login_required(login_url='/login')
def update_offer(request, pk):
    if request.method == "POST":
        desc = request.POST['desc']
        offer = Offer.objects.get(id=pk)
        offer.admin_description = desc
        offer.save()
        if offer.rate > 2:
            return redirect("/offers")
        return redirect("/complaint")
    offers = Offer.objects.filter(rate__gte=3)
    context = {
        "offers": offers
    }
    return render(request, 'offers.html', context)

@login_required(login_url='/login')
def complaint(request):
    complaints = Offer.objects.filter(rate__lt=3).order_by('-id')
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    complaints_final = paginator.get_page(page_number)
    total_pages = complaints_final.paginator.num_pages
    context = {
        "complaints": complaints_final,
        "total_pages": [n + 1 for n in range(total_pages)],
    }
    return render(request, 'complaint.html', context)

@login_required(login_url='/login')
def filter_complaint(request, id):
    complaints = Offer.objects.filter(rate__lt=3).order_by('-id')
    if id == 1:
        complaints = Offer.objects.filter(rate__lt=3).order_by('-id')
    elif id == 2:
        complaints = Offer.objects.filter(user__isnull=True, rate__lt=3, ).order_by('-id')
    elif id == 3:
        complaints = Offer.objects.filter(product__isnull=True)
    context = {
        "complaints": complaints,
        "role_id": id,
    }
    return render(request, 'complaint.html', context)

@login_required(login_url='/login')
def filter_offer(request, id):
    complaints = Offer.objects.filter(rate__lt=3).order_by('-id')
    if id == 1:
        complaints = Offer.objects.filter(rate__lt=3).order_by('-id')
    elif id == 2:
        complaints = Offer.objects.filter(user__isnull=True, rate__lt=3, ).order_by('-id')
    elif id == 3:
        complaints = Offer.objects.filter(product__isnull=True)
    context = {
        "complaints": complaints,
        "role_id": id,
    }
    return render(request, 'complaint.html', context)

@login_required(login_url='/login')
def products(request):
    if request.method == "POST":
        name = request.POST['name']
        category = request.POST['category']
        image = None
        if request.FILES.get('image', None):
            image = request.FILES['image']
        product = Product.objects.create(
            name=name,
            category_id=category,
            image=image
        )
        return redirect("/products")
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products_final = paginator.get_page(page_number)
    total_pages = products_final.paginator.num_pages

    categories = ProductCategory.objects.all()
    cotext = {
        "categories": categories,
        "products": products_final,
        "total_pages": [n + 1 for n in range(total_pages)],
    }
    return render(request, 'products.html', context=cotext)

@login_required(login_url='/login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk).delete()
    return redirect("/products")

@login_required(login_url='/login')
def category(request):
    if request.method == "POST":
        name = request.POST['name']
        category = ProductCategory.objects.create(
            name=name
        )
        return redirect("/category")
    categories = ProductCategory.objects.all()
    cotext = {
        "categories": categories
    }
    return render(request, 'category.html', context=cotext)

@login_required(login_url='/login')
def poll(request):
    if request.method == "POST":
        data = request.POST
        question = data['question']
        variant1 = data['variant1']
        variant2 = data['variant2']
        variant3 = data['variant3']
        variant4 = data['variant4']
        variant5 = data['variant5']
        category = data['category']

        image = None
        if request.FILES.get("image", None):
            image = request.FILES.get('image')

        poll = Poll.objects.create(
            question=question,
            category=None,
            category_product_id=None,
            image=image,
        )
        if variant1:
            variant1 = Variant.objects.create(
                name=variant1
            )
            poll.variant.add(variant1)
        if variant2:
            variant2 = Variant.objects.create(
                name=variant2
            )
            poll.variant.add(variant2)
        if variant3:
            variant3 = Variant.objects.create(
                name=variant3
            )
            poll.variant.add(variant3)
        if variant4:
            variant4 = Variant.objects.create(
                name=variant4
            )
            poll.variant.add(variant4)
        if variant5:
            variant5 = Variant.objects.create(
                name=variant5
            )
            poll.variant.add(variant5)

        if category.isdigit():
            poll.category_product_id = category
        else:
            poll.category = category
        poll.save()
        return redirect('/poll')
    polls = Poll.objects.all().order_by('-id')
    poll_results = PollResult.objects.all().order_by('-id')
    paginator = Paginator(poll_results, 10)
    page_number = request.GET.get('page')
    poll_final = paginator.get_page(page_number)
    total_pages = poll_final.paginator.num_pages

    paginator_ = Paginator(polls, 10)
    page_number_ = request.GET.get('page_poll')
    poll_final_ = paginator_.get_page(page_number_)
    total_pages_ = poll_final_.paginator.num_pages
    categories = ProductCategory.objects.all()
    context = {
        "polls": poll_final_,
        "poll_results": poll_final,
        "categories": categories,
        "total_pages": [n + 1 for n in range(total_pages)],
        "total_pages_poll": [n + 1 for n in range(total_pages_)],
    }
    return render(request, 'poll.html', context)

@login_required(login_url='/login')
def delete_poll(request, pk):
    poll = Poll.objects.get(id=pk).delete()
    return redirect("/poll")

@login_required(login_url='/login')
def ads(request):
    if request.method == "POST":
        desc = request.POST.get('desc', None)
        image = request.FILES.get('image', None)
        video = request.FILES.get('video', None)
        users = TgUser.objects.all()
        for user in users:
            try:
                if image:
                    url = f"{URL}sendPhoto?chat_id={user.tg_id}&caption={desc}&parse_mode=HTML"
                    response = requests.post(url, files={'photo': image})
                elif video:
                    url = f"{URL}sendVideo?chat_id={user.tg_id}&caption={desc}&parse_mode=HTML"
                    response = requests.post(url, files={'video': video})
                else:
                    url = f"{URL}sendMessage?chat_id={user.tg_id}&text={desc}&parse_mode=HTML"
                    response = requests.request('GET', url)
            except Exception as e:
                print(e)
            time.sleep(0.5)
        redirect('/ads')
    return render(request, 'ads.html')

@login_required(login_url='/login')
def photos(request):
    photos = Photos.objects.all().last()
    if request.method == 'POST':
        register = request.FILES.get('registration', None)
        start = request.FILES.get('start', None)
        products = request.FILES.get('products', None)

        if register is not None:
            photos.registration = register
            photos.save()

        if start is not None:
            photos.start = start
            photos.save()

        if products is not None:
            photos.product = products
            photos.save()

        redirect('/photos')
    context = {
        "photo": photos
    }

    return render(request, 'photos.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            print("aa")
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Login yoki parol xato!")
                return redirect('/login')
        except:
            messages.info(request, "Login yoki parol xato!")
            return redirect('/login')
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('/login')
