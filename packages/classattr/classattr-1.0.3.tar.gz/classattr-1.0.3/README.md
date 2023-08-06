# ClassAttr package

This package provides tools to manage objects attributes.

It can be usefull to deal with default value attributes.

# Installation

`pip install classattr`

# Use

ClassAttr can be a parent class wich gives methods to manage attributes.

Methods are : 

## `ClassAttr(attr={},mode=RAISE,**kwargs)`

When creating an object, you can give values to attributes using a dictionary or extra parameters.

` my_object = ClassAttr(x=3,y=2)`
or
` my_object = ClassAttr({'x':3,'y':2})`

## `obj.set(attr={},mode=RAISE,**kwargs)`

```
my_object = ClassAttr()
my_object.set(x=2)
```

If attribute already exist (object attribute) then modify value or create object attribute (if exist as a class attribute)
else Raise a ValueError if mode is RAISE or ignore the attribute if mode is IGNORE or create the object attribute if mode is FORCE

## `cls.set_default(attr={},mode=RAISE,**kwargs)`

set_default is a class method

```
ClassAttr.set_default(name='a name')
```

All class's object will have name attribute. If value is not set then attribute value is 'a name'

## `cls.clear_default()`

Clear all class attributes

##  `obj.del_attr(which,mode=RAISE)`

remove an abject attribute or list of attributes

## `obj.get_keys()`

return all class or parent class or object attributes as a list

## `obj.get(which)`

return attributes values as a dict.
wich can be a string or a list or an empty list.

If wich is an empty list, get will return all obj attributes.


# Example


```
from classattr import ClassAttr, RAISE, FORCE

class Point(ClassAttr):

    ## class atribute, can be default value
    x = 0
    y = 0
    color = 'red'

    def __init__(self,attr = {},mode=RAISE,**kwargs):

        ClassAttr.__init__(self,attr,mode,**kwargs)


class Dot(Point):

    ## class atribute, can be default value
    radius = 1

    def __init__(self,attr = {},mode=RAISE,**kwargs):

        ClassAttr.__init__(self,attr,mode,**kwargs)


p = Point(y=3)
print('x = {}, y = {}'.format(p.x,p.y))

p.set(x=6)
p.set({'y':8})
print('x = {}, y = {}'.format(p.x,p.y))

p.set(z=4,mode=FORCE)
print(p.get_keys())
print(p.get())

d = Dot(x=12,y=24,radius=3)
print('x = {}, y = {}, r = {}'.format(d.x,d.y,d.radius))

d.set(radius=1.5)
d.color = 'blue'
print(d.get())

d.set(unknown_var = 53) # raise an error, if you want to create use mode=FORCE
```

