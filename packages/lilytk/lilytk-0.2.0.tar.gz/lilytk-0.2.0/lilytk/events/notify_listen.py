'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

from typing import Any, Callable
from lilytk.utils.singleton import Singleton

# ?? This would be LEAGUES better IMO if the events were type-checked better but this is python so IDK how easy that would be

def Notifies(event_name: str):
  def NotifyDecorator(func):
    def wrapper(*args, **kwargs):
      result = func(*args, **kwargs)
      NotifyListenerManager().notify(event_name, result)
      return result
    return wrapper
  return NotifyDecorator

def Listens(event_name: str):
  def ListensDecorator(func):
    NotifyListenerManager().register(event_name, func)
    def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
    return wrapper
  return ListensDecorator

def ClassListens(event_name: str, *listener_names: tuple[str, ...]):
  class ClassListensDecorator:
    def __init__(self, cls):
      self.cls = cls

    def __call__(self, *args, **kwargs):
      instance = self.cls(*args, **kwargs)
      for listener_name in listener_names:
        listener_attr = getattr(instance, listener_name, None)
        if listener_attr is None:
          raise ValueError(f"Method '{listener_name}' does not exist on class '{instance.__class__.__name__}'.")
        if not callable(listener_attr):
          raise ValueError(f"Method '{listener_name}' of class '{instance.__class__.__name__}' is not callable.")
        NotifyListenerManager().register(event_name, listener_attr)
      return instance
  return ClassListensDecorator

@Singleton
class NotifyListenerManager:
  def __init__(self):
    self.events_to_listeners: dict[str, list[Callable[..., None]]] = {}
  
  def notify(self, event_name: str, data: Any):
    #print(f"Notifying '{event_name}'...")
    if event_name in self.events_to_listeners:
      for listener in self.events_to_listeners[event_name]:
        listener(data)

  def register(self, event_name: str, listener: Callable[..., None]):
    #print(f"Registering '{event_name}'...")
    if event_name not in self.events_to_listeners:
      self.events_to_listeners[event_name] = [listener]
    elif event_name in self.events_to_listeners and listener not in self.events_to_listeners[event_name]:
      self.events_to_listeners[event_name].append(listener)
    #else:
      #print("WOAH THERE WE DON'T WANT TO DUPLICATE THE LISTENERS")

  # TODO need to get the decorators using this. Like in the class destructors
  #def deregister(self, event_name: str, listener: Callable[..., None]):
  #  print(f"Deregistering listener from '{event_name}'...")
  #  if event_name in self.events_to_listeners:
  #    self.events_to_listeners[event_name].remove(listener)
