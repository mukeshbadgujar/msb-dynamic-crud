
msb-dynamic-crud
=====

A reusable Django app for simply implementing a advance CRUD on any Model. Go here to get started: https://github.com/mukeshbadgujar/msb-dynamic-crud


Quick start
-----------
1. Install Srvup Comments & Dependancies:

    ```
    pip install msb-dynamic-crud django djangorestframework django-cors-headers
    ```
    

2. Add "msb-dynamic-crud" to your INSTALLED_APPS setting like this:

    ```
    INSTALLED_APPS = [
        ...
        'corsheaders', 
        'rest_framework',
        'msb-dynamic-crud',
    ]
    ```

3. Implement Django Dependancy Settings:
    - [Django Rest Framework](http://www.django-rest-framework.org/)
    - [Django Cors Headers](https://github.com/ottoyiu/django-cors-headers)

    Such as:
    ```
    MIDDLEWARE = [
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        )
    }



    CORS_URLS_REGEX = r'^/api.*'
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = (
        '*',
    )

    ```

4. Add the following to `ROOT_URLCONF`:
       ```
       from django.conf.urls import url, include
       urlpatterns = [
           ...
           url(r'^product$', views.product_list),
           url(r'^product/(?P<pk>[0-9]+)$', views.products_detail),
       ]
       ```
5. Views
   ```
   @api_view(['GET', 'POST']) 
   def product_list(request):
       return object_list(request, ProductMaster, ProductsSerializer, 'product_name', 'product_name')
   
   
   @api_view(['GET', 'PUT', 'DELETE'])
   def products_detail(request, pk):
       return object_detail(request, pk, ProductMaster, ProductsSerializer)

   ```
   
6. Serializer

   ```
   class ProductsSerializer(serializers.ModelSerializer):
       class Meta:
           model = ProductMaster
           fields = ("product_name", "product_category", "product_desc", 'is_active')
   ```

7. Models

   ```
   class ProductMaster(models.Model):
       product_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
       product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=False, null=False)
       product_desc = models.TextField(blank=True, null=True)
       is_active = models.BooleanField(default=True,  null=False, unique=False)
   ```
   
For Test on Postman 
https://documenter.getpostman.com/view/13676001/2s7YYmhnSU