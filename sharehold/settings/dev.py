from sharehold.settings.base import *
from sharehold.settings.config import *

#compromised key not to be used in prod environment
SECRET_KEY = 'm(9xlaurd!-%!x1!q5^_)byn##_nr32%@3v&gxz)v#hke^_xun'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ['127.0.0.1', ]

ALLOWED_HOSTS = []
