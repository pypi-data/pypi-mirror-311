'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

import platform
import tkinter as tk
from typing import Callable, Literal, Optional

from lilytk.events import EMPTY_HANDLER
from lilytk.typing import Orientation, TkEventHandler


class MouseScrollEvent:
  def __init__(self, x: int, y: int, delta: float, what: Literal['units', 'pages']):
    self.x = x
    self.y = y
    self.delta = delta
    self.what = what


MouseScrollEventHandler = Callable[[MouseScrollEvent], None]


class Scrollable:
  '''
  Capability for responding to mouse scroll events
  '''

  def __init__(self, target: Optional[tk.BaseWidget] = None, 
                bind_all: bool = True, 
                bind_enter_leave: bool = True, 
                orient: Orientation = tk.VERTICAL, 
                scrolling_factor: float = 1.0):
    scroll_target = target if target is not None else self

    def internal_bind(top_level, scroll_target):
      mouse_scroll_vertical_binding_0: Optional[str] = None
      mouse_scroll_vertical_binding_1: Optional[str] = None
      mouse_scroll_horizontal_binding_0: Optional[str] = None
      mouse_scroll_horizontal_binding_1: Optional[str] = None

      def __base_event_binding_helper(bind_all: bool, event_sequence: str, event_handler: TkEventHandler):
        nonlocal scroll_target
        if bind_all:
          return scroll_target.bind_all(event_sequence, event_handler, True)
        else:
          return scroll_target.bind(event_sequence, event_handler, True)

      def __bind_vertical_scroll(action: MouseScrollEventHandler = EMPTY_HANDLER, bind_all: bool = True, scrolling_factor: float = 1.0):
        nonlocal mouse_scroll_horizontal_binding_0
        nonlocal mouse_scroll_horizontal_binding_1
        nonlocal mouse_scroll_vertical_binding_0
        nonlocal mouse_scroll_vertical_binding_1
        match platform.system():
          case 'Windows':
            mouse_scroll_vertical_binding_0 = __base_event_binding_helper(bind_all, "<Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, -1*(event.delta/120)*scrolling_factor, 'units')))

          case 'Darwin':
            mouse_scroll_vertical_binding_0 = __base_event_binding_helper(bind_all, "<Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, event.delta * scrolling_factor, 'units')))
          case 'Linux':
            mouse_scroll_vertical_binding_0 = __base_event_binding_helper(bind_all, "<Button-4>", lambda event: action(MouseScrollEvent(event.x, event.y, -scrolling_factor, 'units')))
            mouse_scroll_vertical_binding_1 = __base_event_binding_helper(bind_all, "<Button-5>", lambda event: action(MouseScrollEvent(event.x, event.y, scrolling_factor, 'units')))
          case _:
            raise NotImplementedError(f"We don't know how to bind mouse scroll to '{platform.system()}'")
          
      def __bind_horizontal_scroll(action: MouseScrollEventHandler = EMPTY_HANDLER, bind_all: bool = True, scrolling_factor: float = 1.0):
        nonlocal mouse_scroll_horizontal_binding_0
        nonlocal mouse_scroll_horizontal_binding_1
        nonlocal mouse_scroll_vertical_binding_0
        nonlocal mouse_scroll_vertical_binding_1
        match platform.system():
          case 'Windows':
            mouse_scroll_horizontal_binding_0 = __base_event_binding_helper(bind_all, "<Shift-Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, -1*(event.delta/scrolling_factor), 'units')))
          case 'Darwin':
            mouse_scroll_horizontal_binding_0 = __base_event_binding_helper(bind_all, "<Shift-Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, event.delta, 'units')))
          case 'Linux':
            mouse_scroll_horizontal_binding_0 = __base_event_binding_helper(bind_all, "<Shift-Button-4>", lambda event: action(MouseScrollEvent(event.x, event.y, 120 / scrolling_factor, 'units')))
            mouse_scroll_horizontal_binding_1 = __base_event_binding_helper(bind_all, "<Shift-Button-5>", lambda event: action(MouseScrollEvent(event.x, event.y, -120 / scrolling_factor, 'units')))
          case _:
            raise NotImplementedError(f"We don't know how to bind mouse scroll to '{platform.system()}'")

      def __bind_scroll(bind_all: bool = False, orient: Orientation = tk.VERTICAL, scrolling_factor: float = 1.0,
                        xscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER, 
                        yscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER):
        if orient == tk.VERTICAL or orient == tk.BOTH:
          __bind_vertical_scroll(yscrollcommand, bind_all, scrolling_factor)
        if orient == tk.VERTICAL or orient == tk.BOTH:
          __bind_horizontal_scroll(xscrollcommand, bind_all, scrolling_factor)

      def __unbind_scroll():
        nonlocal scroll_target
        nonlocal mouse_scroll_horizontal_binding_0
        nonlocal mouse_scroll_horizontal_binding_1
        nonlocal mouse_scroll_vertical_binding_0
        nonlocal mouse_scroll_vertical_binding_1
        if mouse_scroll_vertical_binding_0 is not None:
          if platform.system() == 'Linux':
            scroll_target.unbind("<Button-4>", mouse_scroll_vertical_binding_0)
          else:
            scroll_target.unbind("<Mousewheel>", mouse_scroll_vertical_binding_0)

        if mouse_scroll_vertical_binding_1 is not None:
          scroll_target.unbind("<Button-5>", mouse_scroll_vertical_binding_1)

        if mouse_scroll_horizontal_binding_0 is not None:
          if platform.system() == 'Linux':
            scroll_target.unbind("<Shift-Button-4>", mouse_scroll_horizontal_binding_0)
          else:
            scroll_target.unbind("<Shift-Mousewheel>", mouse_scroll_horizontal_binding_0)
        
        if mouse_scroll_horizontal_binding_1 is not None:
          scroll_target.unbind("<Shift-Button-5>", mouse_scroll_horizontal_binding_1)

      def __bind_enter_leave_mouse_scroll(bind_all: bool = False, orient: Orientation = tk.VERTICAL, scrolling_factor: int = 120,
                                      xscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER, 
                                      yscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER):
        nonlocal top_level
        top_level.bind('<Enter>', lambda event: __bind_scroll(bind_all, orient, scrolling_factor, xscrollcommand, yscrollcommand), True)
        top_level.bind('<Leave>', lambda event: __unbind_scroll(), True)

      if bind_enter_leave:
        __bind_enter_leave_mouse_scroll(bind_all, orient, scrolling_factor, top_level.horizontal_scroll, top_level.vertical_scroll)
      else:
        __bind_scroll(bind_all, orient, scrolling_factor, top_level.horizontal_scroll, top_level.vertical_scroll)

    internal_bind(self, scroll_target)

  def horizontal_scroll(self, event: MouseScrollEvent):
    pass

  def vertical_scroll(self, event: MouseScrollEvent):
    pass
