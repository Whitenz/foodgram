from rest_framework.pagination import PageNumberPagination


class CustomLimitPagination(PageNumberPagination):
    """Custom pagination class allows set page size from query parameters."""
    page_size_query_param = 'limit'
