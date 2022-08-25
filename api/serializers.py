from rest_framework import serializers

from main.models import TgUser, ProductCategory, Product, Offer, Staff, Poll, PollResult, Variant, Photos


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant
        fields = ['id','name']


class PollSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', "question", "variants","image"]

    def get_variants(self, obj):
        variants = obj.variant.all()
        serializer = VariantSerializer(variants, many=True)
        return serializer.data


class PollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollResult
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photos
        fields = '__all__'
