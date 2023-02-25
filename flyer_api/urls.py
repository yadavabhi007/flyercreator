from django.urls import include, path, re_path
from rest_framework import routers, permissions
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from flyer_api.views import  UserProductListView, ProjectViewSet, CurrentUserView, CatalogProductListView, UserProductCreateView,CategoryListView,PageFormatListView,PageLayoutTemplateListView,StopperListView,PosterListView,CreateProject
# from rest_framework_nested import routers

schema_view = get_schema_view(
    openapi.Info(
        title="Flyer Builder API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

# router = routers.SimpleRouter()
# router.register(r'projects', ProjectViewSet, basename='project')

# project_pages_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
# project_pages_router.register(r'pages', ProjectPageViewSet, base_name='project-pages')

urlpatterns = [
    path('', include(router.urls)),
    # re_path(r'^', include(router.urls)),
    # re_path(r'^', include(project_pages_router.urls)),  
    # re_path(r'^/users/{pk}', views.UserViewSet, name='user-detail'),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api-token-auth/', views.obtain_auth_token)
    # re_path(r'^token-auth/', views.obtain_auth_token),
    re_path(r'docs/', include_docs_urls(title='Flyer Builder API')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),

    # path('test/', TestView.as_view()),
    path('user/profile', CurrentUserView.as_view()),
    path('catalog/products/search', CatalogProductListView.as_view(), name='product-search'),
    path('products/add', UserProductCreateView.as_view(), name='product-add'),
    path('products/', UserProductListView.as_view(), name='products'),
    # path('catalog/products/{code}/add-image', ProductListView.as_view(), name='product-add-image'),
    
    path('category/', CategoryListView.as_view(), name='category'),
    path('page_format/', PageFormatListView.as_view(), name='page_format'),
    path('stopper_format/', StopperListView.as_view(), name='stopper_format'),
    path('poster_format/', PosterListView.as_view(), name='poster_format'),
    path('page_layout_template/', PageLayoutTemplateListView.as_view(), name='page_layout_template'),
    path('create_project/', CreateProject.as_view(), name='create_project'),
    
]
