from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from api.serializers import UserSerializer, ProductCategorySerializer, ProductSerializer, OfferSerializer, \
    StaffSerializer, PollSerializer, PollResultSerializer, PhotosSerializer
from main.models import TgUser, ProductCategory, Product, Offer, Staff, Poll, PollResult, Photos


class StaffViewset(viewsets.ModelViewSet):
    queryset = Staff.objects.filter(~Q(role="deliverer"))
    serializer_class = StaffSerializer

    @action(methods=['get'], detail=False)
    def get_deliverer(self, request):
        staffs = Staff.objects.filter(role="deliverer")
        serializer = StaffSerializer(staffs, many=True)
        return Response(serializer.data, 200)


class UserViewset(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def check_user(self, request):
        tg_id = request.GET.get("tg_id")
        user = TgUser.objects.filter(tg_id=tg_id)
        if user.exists():
            return Response("User exists", 400)
        else:
            return Response("User doesn't exist", 200)


class ProductCategoryViewset(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    @action(methods=['get'], detail=False)
    def get_products(self, request):
        category_name = request.GET.get("category_name")
        products = Product.objects.filter(category__name=category_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, 200)


class OfferViewset(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    @action(methods=['post'], detail=False)
    def post(self, request):
        tg_id = request.data.get("user_id")
        staff_id = request.data.get("user", None)
        rate = request.data.get("rate")
        product_id = request.data.get("product_id", None)
        offer_text = request.data.get("offer_text")
        user = TgUser.objects.get(tg_id=tg_id)
        staff = None
        if staff_id:
            staff = Staff.objects.get(id=staff_id)
            offer = Offer.objects.create(
                product_id=product_id,
                user_id=staff.id,
                tg_user=user,
                offer_text=offer_text,
                rate=rate,
            )
        else:
            offer = Offer.objects.create(
                product_id=product_id,
                tg_user=user,
                offer_text=offer_text,
                rate=rate,
            )
        return Response("Created", 201)


class PollViewset(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        product_id = request.GET.get("product_id", None)
        role = request.GET.get("role", None)
        if product_id:
            product = Product.objects.get(id=product_id)
            polls = Poll.objects.filter(category_product=product.category)
            serializer = PollSerializer(polls, many=True)
            return Response(serializer.data, 200)
        return Response("Error")

    @action(methods=['get'], detail=False)
    def get_staff(self, request):
        user_id = request.GET.get('user_id')

        user = Staff.objects.get(id=user_id)
        polls = Poll.objects.filter(Q(category="ofitsiant") | Q(category='boshqaruvchi') | Q(category='kassir'))
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, 200)

    @action(methods=['get'], detail=False)
    def get_deliverer(self, request):
        user_id = request.GET.get('user_id')

        user = Staff.objects.get(id=user_id)
        polls = Poll.objects.filter(category='deliverer')
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, 200)


class PollResultViewset(viewsets.ModelViewSet):
    queryset = PollResult.objects.all()
    serializer_class = PollResultSerializer

    @action(methods=['post'], detail=False)
    def post(self, request):
        tg_id = request.data.get("tg_user")
        variant_id = request.data.get("variant_id")
        poll = request.data.get("poll")

        tg_user_instance = TgUser.objects.get(tg_id=tg_id)
        poll_instance = PollResult.objects.create(
            tg_user=tg_user_instance,
            poll_id=poll,
            variant_id=variant_id,
        )
        return Response("Created", status=HTTP_201_CREATED)


class PhotosViewset(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer
