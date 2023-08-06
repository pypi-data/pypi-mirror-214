# ClassAttr package

This package provides tools to manage objects attributes.

It can be usefull to deal with default value attributes.


## Example:

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

