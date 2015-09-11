#! /usr/bin/env python
#coding:utf8
""" for everyting countable
"""

from sputnik.SpuCountServer import SpuCountServer
from sputnik.SpuLogging import SpuLogging

class LeoCount(SpuCountServer):
    """ a drive base class base on SpuCountServer

    complete method get_key
    """
    _logging = SpuLogging(module_name = 'SpuCountServer',
                          class_name = 'SpuCountServer')

    def __init__(self, count_type, key_prefix):
        self._key_prefix = key_prefix
        SpuCountServer.__init__(self, count_type)

    def _gen_key(self, key_value):
        """ generate specific key
        """
        return '_'.join((self._key_prefix, str(key_value)))

    def reset_count(self, key_value, count):
        """ reset count of specific key
        """
        self._logging.set_function('reset_count')
        try:
            self._connection.ping()
        except Exception as e:
            self._logging.error('{}'.format(e))
        else:
            key = self._gen_key(key_value)
            self._connection.set(key, count)
            self._logging.info('reset_count {0} to {1}'.format(key, count))

    def inc_count(self, key_value, amount=1):
        """
        Increments the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``
        """
        self._logging.set_function('inc_count')
        try:
            self._connection.ping()
        except Exception as e:
            self._logging.error('{}'.format(e))
        else:
            key = self._gen_key(key_value)
            self._connection.incr(key, amount)
            self._logging.info('inc_count {0} by {1}'.format(key, amount))

    def desc_count(self, key_value, amount=1):
        """
        Decrements the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``
        """
        self._logging.set_function('desc_count')
        try:
            self._connection.ping()
        except Exception as e:
            self._logging.error('{}'.format(e))
        else:
            key = self._gen_key(key_value)
            self._connection.decr(key, amount)
            self._logging.info('desc_count {0} by {1}'.format(key, amount))
            # test the value should greater than 0
            count = self._connection.get(key)
            if int(count) > 0:
                self._connection.decr(key, amount)
                self._logging.info('desc_count {0} by {1}'.format(key, amount))
            else:
                self._logging.info('could not decrease count because the count of {0} is {1}'.format(key, count))
    
    def get_count(self, key_value):
        """get count of key
        """
        self._logging.set_function('get_count')
        try:
            self._connection.ping()
        except Exception as e:
            self._logging.error('{}'.format(e))
            return 0
        else:
            key = self._gen_key(key_value)
            count = self._connection.get(key)
            self._logging.info('get_count {0} values: {1}'.format(key, count))
            if not count:
                return 0
            return int(count)

        
class SingletonDecorator(object):
    """ a singleton decorator class
    """

    def __init__(self, kclass):
        self.kclass = kclass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.kclass(*args, **kwargs)
        return self.instance


class LeoCollectCount(LeoCount):
    """ count for leo collect, key format: leo_collect_suffix
    """
    def __init__(self, count_type='leo_collect', key_prefix='leo_collect'):
        LeoCount.__init__(self, count_type=count_type, key_prefix=key_prefix)

    def __str__(self):
        return 'Leo Count on collect, key_prefix: {}'.format(self._key_prefix)


class LeoDetailCount(LeoCount):
    """ count for leo detail, key format: leo_detail_suffix 
    """
    def __init__(self, count_type='leo_detail', key_prefix='leo_detail'):
        LeoCount.__init__(self, count_type=count_type, key_prefix=key_prefix)

    def __str__(self):
        return 'Leo Count on detail, key_prefix: {}'.format(self._key_prefix)

leo_collect_count = LeoCollectCount()
leo_detail_count = LeoDetailCount()
