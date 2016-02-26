from django.views.decorators.cache import cache_control

__all__ = ('CacheControlMixin',)


class CacheControlMixin(object):
    """Mixin that allows setting Cache-Control options.

    Specify Cache-Control options as class attributes
    on the view class.

    Cache-Control directive explanations:
    http://condor.depaul.edu/dmumaugh/readings/handouts/SE435/HTTP/node24.html

    Django's `django.views.decorators.cache.cache_control` options:
    https://docs.djangoproject.com/en/1.7/topics/cache/#controlling-cache-using-other-headers
    """
    # These are all `None`, which indicates unset.
    cachecontrol_public = None
    cachecontrol_private = None
    cachecontrol_no_cache = None
    cachecontrol_no_transform = None
    cachecontrol_must_revalidate = None
    cachecontrol_proxy_revalidate = None
    cachecontrol_max_age = None
    cachecontrol_s_maxage = None

    @classmethod
    def get_cachecontrol_options(cls):
        opts = (
            'public', 'private', 'no_cache', 'no_transform',
            'must_revalidate', 'proxy_revalidate', 'max_age',
            's_maxage')
        options = {}
        for opt in opts:
            value = getattr(cls, 'cachecontrol_{}'.format(opt), None)
            if value is not None:
                options[opt] = value
        return options

    @classmethod
    def as_view(cls, *args, **kwargs):
        view_func = super(CacheControlMixin, cls).as_view(*args, **kwargs)
        options = cls.get_cachecontrol_options()
        if options:
            return cache_control(**options)(view_func)
        return view_func
