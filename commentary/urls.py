from rest_framework.routers import DefaultRouter

from commentary.views import CommentaryViewSet


router = DefaultRouter()
router.register("", CommentaryViewSet)

app_name = "user"

urlpatterns = router.urls
