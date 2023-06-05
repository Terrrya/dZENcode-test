from rest_framework.routers import SimpleRouter

from commentary.views import CommentaryViewSet


router = SimpleRouter()
router.register("", CommentaryViewSet)

app_name = "user"

urlpatterns = router.urls
