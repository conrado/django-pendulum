from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class PendulumApphook(CMSApp):
    name = _('Pendulum Apphook')
    urls = ['pendulum.urls']

apphook_pool.register(PendulumApphook)
