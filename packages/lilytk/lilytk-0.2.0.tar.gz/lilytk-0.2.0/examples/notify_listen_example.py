'''
This example shows off the notify_listen decorators:
- Notifies: notifies the listeners of an event passing the listener 
            whatever data the function/method returns
- Listens: registers a non-instance function to listen to a particular
            event
- ClassListens: registers instance methods of a class to listen to a 
            particular event
'''
from lilytk.events import Notifies, Listens, ClassListens

'''
This is our notifier class. We have @Notifies on the constructor
and on the 'set_value' method but they produce different events!
'''
class MyVariable:
  @Notifies("MyVariable.Initialized")
  def __init__(self, initial_value):
    self.internal_value = initial_value
    return self.internal_value

  @Notifies("MyVariable.Set")
  def set_value(self, value):
    self.internal_value = value
    return self.internal_value

'''
Here we set up some non-instance functions that listen to our
MyVariable events
'''
@Listens("MyVariable.Initialized")
def listener_init(data):
  print(f'listener_init: {data}')

@Listens("MyVariable.Set")
def listener_set(data):
  print(f'listener_set: {data}')

'''
Here we have a listener class with some methods that listen 
to our MyVariable events
'''
@ClassListens("MyVariable.Initialized", "listener_init")
@ClassListens("MyVariable.Set", "listener_set", "listener_set")
class MyClassListener:
  def __init__(self, listener_name):
    self.name = listener_name

  def listener_init(self, data):
    print(f'{self.name} listener_init: {data}')

  def listener_set(self, data):
    print(f'{self.name} listener_set: {data}')

'''
Class method listeners get registered at initialization.
This makes it so those listener methods are able to utilize
instance variables.
'''
my_sweet_listener = MyClassListener("MyClassListener uwu")

'''
Initialize our MyVariable class. After this line,
You will see the following printed out in the console:
```
listener_init: 50
MyClassListener uwu listener_init: 50
```
'''
my_variable = MyVariable(50)


for i in range(20, 30):
  '''
  After each call to set_value, the listeners that listen
  to 'MyVariable.Set' events are called so after each 'set_value'
  call you will see the following in the console:
  ```
  listener_set: {i}
  MyClassListener uwu listener_set: {i}
  ```
  where '{i}' is the value of i
  '''
  my_variable.set_value(i)
