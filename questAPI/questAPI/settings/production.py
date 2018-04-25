from questAPI.settings.common import *
from .common import *             # NOQA

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!p6$_1bwp8*m#i7h*c-&u+nsk(u9tzy_usty4ds9)bbi1tupy7'
DEBUG=False
STATIC_ROOT = join(BASE_DIR, '..', 'static/')