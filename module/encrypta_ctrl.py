#! /usr/bin/env python
# -*- coding: utf-8 -*-

from py_util.encrypta.encrypta import Encrypta, EncryptaException, ModifiedException

class EncryptaCtrl(object):
    def __init__(self, ):
        self._encrypta = Encrypta()

    def decrypt(self, data):
        try:
            self._encrypta.dec(data)
            return dict(ok=self._encrypta.ok, data=self._encrypta.data, why='')
        except ModifiedException as e:
            return dict(ok=self._encrypta.ok, data=1, why=str(e))
        except EncryptaException as e:
            return dict(ok=self._encrypta.ok, data=2, why=str(e))
        except Exception as e:
            return dict(ok=self._encrypta.ok, data=3, why=str(e))

    def encrypt(self, data, version=3):
        try:
            self._encrypta.enc(data, version)
            return dict(ok=self._encrypta.ok, data=self._encrypta.data_encrypted, why='')
        except ModifiedException as e:
            return dict(ok=self._encrypta.ok, data=1, why=str(e))
        except EncryptaException as e:
            return dict(ok=self._encrypta.ok, data=2, why=str(e))
        except Exception as e:
            return dict(ok=self._encrypta.ok, data=3, why=str(e))

    def supportedVersions(self,):
        return self._encrypta.supportedVersions() or []
