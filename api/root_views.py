from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.shortcuts import render


@api_view(['GET'])
def api_root_view(request, format=None):
    """
    API Root endpoint - shows available endpoints
    Requires authentication
    """
    if not request.user or not request.user.is_authenticated:
        # If not authenticated and accessing via browser, show template
        if request.accepted_renderer.format == 'html':
            return render(request, 'api/api_root.html')
        # For API clients, return 403
        return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=403
        )

    return Response({
        'equipment': reverse('api:equipment-list', request=request, format=format),
        'manufacturers': reverse('api:manufacturer-list', request=request, format=format),
        'categories': reverse('api:category-list', request=request, format=format),
        'maintenance': reverse('api:maintenance-list', request=request, format=format),
        'maintenance-types': reverse('api:maintenance-type-list', request=request, format=format),
        'inspections': reverse('api:inspection-list', request=request, format=format),
        'profiles': reverse('api:profile-list', request=request, format=format),
    })

