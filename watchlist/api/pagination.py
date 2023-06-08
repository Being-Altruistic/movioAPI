
# PageNumber Pagination

from rest_framework.pagination import (PageNumberPagination, 
                                       LimitOffsetPagination,
                                       CursorPagination)

class WatchListPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p' # To use as an alias for PAGE in URL param.
    page_size_query_param = 'size' # If user wants size to be more than specified.
                                    # Items per page.
    max_page_size = 10  # Limiting the items per page.

    last_page_strings  = 'last_page'

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 7
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCPagination(CursorPagination):
    # Remember, CursorPagination comes with default ordering
    # Donot use filters.Ordering & CursorPagination Ordering at same time.
    # The OP will be latest 1st, as per creation time.

    # Use case to traverse through multiple pages in a document.
    page_size= 5

    ordering = 'created'
    cursor_query_param = 'record'

