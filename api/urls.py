from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('user', UserViewset, basename='UserViewSet')
router.register('staff', StaffViewset, basename='StaffViewset')
router.register('product-category', ProductCategoryViewset, basename='ProductCategoryViewset')
router.register('offer', OfferViewset, basename='OfferViewset')
router.register('poll', PollViewset, basename='PollViewset')
router.register('poll-result', PollResultViewset, basename='PollResultViewset')
router.register('photos', PhotosViewset, basename='PhotosViewset')
