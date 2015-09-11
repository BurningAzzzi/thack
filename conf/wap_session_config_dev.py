# base session config

session_config = {
    'auto_session_enable' : True,
    'session_permanent' : False,
    'secret_key' : 'pandaria_project_start_time__2013-5-25',
    # Session config
    'session_engine' : 'redis',                                # the module to store session data
    'session_key_function' : None,
    'session_cookie_name' : 'sessionid',                       # Cookie name. This can be whatever you want.
    'session_cookie_age' : 60 * 60 * 24 * 7 * 2,               # Age of cookie, in seconds (default: 2 weeks).
    'session_cookie_domain' : 'dev.lanrenzhoumo.com',                            # A string like ".lawrence.com", or None for standard domain cookie.
    'session_cookie_secure' : False,                           # Whether the session cookie should be secure (https:// only).
    'session_cookie_path' : '/',                               # The path of the session cookie.
    'session_save_every_request' : True,                      # Whether to save the session data on every request.
    'session_expire_at_browser_close' : False,                 # Whether a user's session cookie expires when the Web browser is closed.
    'session_db_config' : {
        'db': 15,
        'host': 'cache_1',
        'port': 6380
        }
    }
