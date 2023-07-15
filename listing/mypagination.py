from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyCursorPagination(PageNumberPagination):
    page_size = 7

    def get_paginated_response(self, data):
        try:
            return Response({
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'results': data
            })
        except Exception as e:
            # Log or handle the exception appropriately
            return Response({
                'error': 'An error occurred during pagination',
                'details': str(e)
            }, status=500)
