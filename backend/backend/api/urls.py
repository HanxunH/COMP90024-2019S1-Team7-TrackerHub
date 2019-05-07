# coding: utf-8

from django.urls import path, re_path
from backend.api.views.tweets import *
from backend.api.views.tweet_pics import tweet_pic_router
from backend.api.views.statistics import statistics_time_router, statistics_track_router


urlpatterns = [
    path('tweet/pic/<str:resource>/', tweet_pic_router),
    path('tweet/pic/', tweet_pic_router),
    path('tweet/untrained/<int:resource>/', tweet_untrained_router),
    path('tweet/untrained/', tweet_untrained_router),
    path('tweet/untrained/text/<int:resource>/', tweet_untrained_text_router),
    path('tweet/untrained/text/', tweet_untrained_text_router),
    path('tweet/trained/', tweet_trained_router),
    path('tweet/trained/text/', tweet_trained_text_router),
    path('tweet/', tweet_router),
    path('tweet/<str:resource>/', tweet_router),
    path('statistics/time/', statistics_time_router),
    path('statistics/track/random/', statistics_track_router),
    path('statistics/track/random/<int:number>/', statistics_track_router),
    path('statistics/track/<str:user_id>/', statistics_track_router),
]
