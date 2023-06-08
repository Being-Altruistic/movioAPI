from rest_framework.throttling import UserRateThrottle

# Custom throttling classes

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'

class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'

