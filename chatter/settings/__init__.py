from envparse import env

ENVIRONMENT_TYPE = env.str('ENVIRONMENT_TYPE', default='development')

if ENVIRONMENT_TYPE == 'production':
    from chatter.settings.production import *
else:
    from chatter.settings.development import *

del env
