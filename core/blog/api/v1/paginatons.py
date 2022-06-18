from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DefaultPagination(PageNumberPagination):
    # page_size = 10
    # page_size_query_param = 'page_size'
    # max_page_size = 100
    # up lines work singularly but for more option we can user belows
    page_size = 10
    def get_paginated_response(self, data):
            return Response({
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_objects_count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'results': data
            })