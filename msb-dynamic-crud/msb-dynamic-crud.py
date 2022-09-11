from django.http import JsonResponse
from rest_framework import status


def object_list(request, ModalObject, ModalObjectSerializer, search_modal_field, input_field):
    """Get All, Filter Active/Deactive, Filter by Field Given, Insert"""
    search_modal_field = search_modal_field + '__icontains'
    if request.method == 'GET':
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            if is_active.lower() == "true" or is_active.lower() == "t":
                is_active = True
            else:
                is_active = False

            product = ModalObject.objects.filter(is_active=is_active)
        else:
            product = ModalObject.objects.all()

        product_name = request.query_params.get(input_field, None)
        if product_name is not None:
            product = ModalObject.objects.filter(**{search_modal_field: product_name})

        product_serializer = ModalObjectSerializer(product, many=True)
        print(product_serializer.data)
        if not product_serializer.data:
            return JsonResponse("No product Please Add", safe=False, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse(product_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        category_data = request.data  # JSONParser().parse(request)
        print(category_data)
        product_serializer = ModalObjectSerializer(data=category_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def object_detail(request, pk,  ModalObject, ModalObjectSerializer):
    """Get One, Update One, Delete One Item by ID,"""
    try:
        product = ModalObject.objects.get(pk=pk)
    except ModalObject.DoesNotExist:
        return JsonResponse({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        product_serializer = ModalObjectSerializer(product)
        return JsonResponse(product_serializer.data)

    elif request.method == 'PUT':
        prod_category_data = request.data  # JSONParser().parse(request)
        product_serializer = ModalObjectSerializer(product, data=prod_category_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)