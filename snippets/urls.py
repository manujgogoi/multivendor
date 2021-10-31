from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)

urlpatterns = [
    path('', include(router.urls))
]

# urlpatterns = [
#     path('', views.api_root),
#     path('snippets/', views.SnippetList.as_view()),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
#     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)
