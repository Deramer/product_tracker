from rest_framework import routers

from product.views import ProductViewSet


router = routers.DefaultRouter()

router.register(r'product', ProductViewSet)
