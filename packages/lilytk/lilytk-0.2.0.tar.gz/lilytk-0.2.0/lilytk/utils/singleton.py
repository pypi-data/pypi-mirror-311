'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

def Singleton(cls):
  instance = None
  def get_instance(*args, **kwargs):
    nonlocal instance
    if instance is None:
      instance = cls(*args, **kwargs)
    return instance
  return get_instance