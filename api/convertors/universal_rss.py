from datetime import time, datetime, timedelta
from time import mktime

import feedparser
import pytz
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.utils import timezone

from api.models import Channel, Rss, Feed, RssStatus, BlacklistChannel
from api.tools.thread_manager import ThreadManager
import time


class UniversalRss:

    def __init__(self):
        pass

    def get_date(self, struc_date):
        if struc_date is None:
            return datetime.min.replace(tzinfo=pytz.utc)
        return datetime.fromtimestamp(mktime(struc_date), tz=pytz.UTC)

    def rss(self, request):
        if not request.user.is_anonymous:
            blchs = [blch.channel.id for blch in BlacklistChannel.objects.filter(user=request.user)]
            chs = [ch.id for ch in Channel.objects.filter(Q(user=None) | Q(user=request.user))]
            feeds = list(Channel.objects.filter(pk__in=[ch for ch in chs if ch not in blchs]))
        else:
            feeds = list(Channel.objects.filter(user=None))

        rss_list = []

        for feed in feeds:
            news_feed = feedparser.parse(feed.url)
            for rss in news_feed.entries[:8]:
                try:
                    r = Rss.objects.get(url_origin=rss.get('link', None))
                except:
                    r = Rss.objects.create(channel_id=feed.id,
                                           title=rss.get('title', None),
                                           description=rss.get('summary', None),
                                           url_image=rss.get('r', None),
                                           url_origin=rss.get('link', None),
                                           date=self.get_date(rss.get('published_parsed', None)))

                if request.user.is_anonymous or len(RssStatus.objects.filter(user=request.user, rss=r)) == 0:
                    if not next((x for x in rss_list if x.url_origin == rss.get('link', None)), None):
                        rss_list.append(r)
        # if not isinstance(user, AnonymousUser):
        #     rss.user_read.add(user)
        return sorted(rss_list, key=lambda x: x.date, reverse=True)
