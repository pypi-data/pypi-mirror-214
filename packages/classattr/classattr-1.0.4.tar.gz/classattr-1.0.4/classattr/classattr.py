"""
ClassAttr package

This package provides tools to manage objects attributes

Examples:

>>> class Point(ClassAttr):
...     x = 0
...     y = 0
...     color = 'red'
...     def __init__(self,attr = {},mode=RAISE,**kwargs):
...         ClassAttr.__init__(self,attr,mode,**kwargs)

>>> class Dot(Point):
...     radius = 1
...     def __init__(self,attr = {},mode=RAISE,**kwargs):
...         ClassAttr.__init__(self,attr,mode,**kwargs)

>>> a = Point(y=3)
>>> a.x
0
>>> a.y
3
>>> a.color
'red'
>>> a.set(x=6)
>>> a.x
6
>>> a.set({'y':8})
>>> a.y
8
>>> a.set(z=4,mode=FORCE)
>>> a.z
4
>>> a.get_keys()
['color', 'x', 'y', 'z']
>>> a.get()
{'x': 6, 'y': 8, 'color': 'red', 'z': 4}
>>> d = Dot(x=12,y=24,radius=3)
>>> d.x
12
>>> d.set(radius=1.5)
>>> d.get_keys()
['color', 'radius', 'x', 'y']
>>> d.get()
{'x': 12, 'y': 24, 'color': 'red', 'radius': 1.5}

"""

RAISE = 0
FORCE = 1
IGNORE = 2

class ClassAttr():
    """
    ClassAttr class

    Provides tools to manage objects attributes 
    """
    
    def __init__(self,attr={},mode=RAISE,**kwargs):
        """
        Create an object with attributes

        attr attributes dictionary
        
        mode can be RAISE, FORCE or IGNORE
        if RAISE raise an error if attribute doesn't already exist in the objet
        if FORCE create attribute if not already exist
        if IGNORE ignore attribute if not already exist

        Examples :
        >>> obj1 = ClassAttr()

        >>> obj2 = ClassAttr({'x':1,'y':-3},mode=FORCE)
        >>> obj2.x
        1
        """
        
        self.set(attr,mode,**kwargs)


    def set(self,attr={},mode=RAISE,**kwargs):
        """
        add or modify an object attribute

        mode can be RAISE, FORCE or IGNORE
        if RAISE raise an error if attribute doesn't already exist in the objet
        if FORCE create attribute if not already exist
        if IGNORE ignore attribute if not already exist

        Examples :
        >>> obj = ClassAttr()
        >>> obj.set({'x':1},mode=FORCE)
        >>> obj.x
        1
        >>> obj.set(x=-3)
        >>> obj.x
        -3
        >>> obj.x = 8
        >>> obj.x
        8
        """
        
        classes = (self.__class__,) + self.__class__.__bases__

        class_attr = []
        for c in classes:
            class_attr += [x for x in c.__dict__.keys() if x[:2] != '__' and not callable(c.__dict__[x]) and not isinstance(c.__dict__[x],classmethod)]

        attr = {**attr,**kwargs}
        
        for key,value in attr.items():
            if mode == FORCE or key in self.__dict__.keys() or key in class_attr:
                self.__dict__[key] = value
            elif mode == RAISE:
                raise ValueError('Unavailable attribute {}'.format(key))


    @classmethod                
    def set_default(cls,attr={},mode=RAISE,**kwargs):
        """
        add or modify an attribute as a class attribute

        mode can be RAISE, FORCE or IGNORE
        if RAISE raise an error if attribute doesn't already exist in the class
        if FORCE create attribute if not already exist
        if IGNORE ignore attribute if not already exist

        Examples :
        >>> ClassAttr.set_default({'x':1},mode=FORCE)
        >>> obj = ClassAttr()
        >>> obj.x
        1
        >>> ClassAttr.x
        1
        >>> obj.set(x=-3)
        >>> obj.x
        -3
        >>> ClassAttr.x
        1
        """

        classes = (cls,) + cls.__bases__

        class_attr = []
        for c in classes:
            class_attr += [x for x in c.__dict__.keys() if x[:2] != '__' and not callable(c.__dict__[x]) and not isinstance(c.__dict__[x],classmethod)]


        attr = {**attr,**kwargs}

        for key,value in attr.items():
            if mode == FORCE or key in class_attr:
                setattr(cls,key,value)
            elif mode == RAISE:
                raise ValueError('Unavailable attribute {}'.format(key))


    @classmethod                
    def clear_default(cls):
        """
        remove all class attributes

        >>> ClassAttr.set_default({'x':1},mode=FORCE)
        >>> ClassAttr.x
        1
        >>> ClassAttr.clear_default()
        """

        class_attr = [x for x in cls.__dict__.keys() if x[:2] != '__' and not callable(cls.__dict__[x]) and not isinstance(cls.__dict__[x],classmethod)]

        for key in class_attr:
            delattr(cls,key)


    def del_attr(self,which,mode=RAISE):
        """
        remove an object attribute

        which str or str list, attributes list

        mode can be RAISE or IGNORE
        if RAISE raise an error if attribute doesn't exist
        if IGNORE ignore attribute if not exists

        Examples :
        >>> ClassAttr.set_default({'x':1},mode=FORCE)
        >>> obj = ClassAttr()
        >>> obj.set(x=-3,y=2,mode=FORCE)
        >>> obj.x
        -3
        >>> obj.del_attr(['x','y'])
        >>> obj.x
        1
        """

        if isinstance(which,str):
            which = [which,]

        for key in which:
            if key in self.__dict__.keys():
                delattr(self,key)
            elif mode == RAISE:
                raise ValueError('Unknown attribute {}'.format(key))


    def get_keys(self):
        """
        return object or class attributes

        Examples :
        >>> ClassAttr.set_default({'x':1},mode=FORCE)
        >>> obj = ClassAttr()
        >>> obj.set(x=3,y=2,mode=FORCE)
        >>> obj.get_keys()
        ['x', 'y']
        >>> obj.x
        3
        >>> obj.y
        2
        """

        classes = (self.__class__,) + self.__class__.__bases__

        class_attr = set()
        for c in classes:
            class_attr = class_attr.union(set([x for x in c.__dict__.keys() if x[:2] != '__' and not callable(c.__dict__[x]) and not isinstance(c.__dict__[x],classmethod)]))

        obj_attr = list(set(self.__dict__.keys()).union(class_attr))
        obj_attr.sort()

        return obj_attr


    def get(self,which = []):
        """
        return object or class attribute's value in a dictionary
        
        which str or str list, attributes list
        if which is empty, return all attributes and values

        Examples :
        >>> ClassAttr.set_default({'x':1},mode=FORCE)
        >>> obj = ClassAttr()
        >>> obj.set(y=2,mode=FORCE)
        >>> obj.get('y')
        2
        >>> obj.get(['x','y'])
        {'x': 1, 'y': 2}
        """

        class_attr = [x for x in self.__class__.__dict__.keys() if x[:2] != '__' and not callable(self.__class__.__dict__[x]) and not isinstance(self.__class__.__dict__[x],classmethod)]

        superclass_attr = {}
        for c in self.__class__.__bases__:
            for k in c.__dict__.keys():
                if k[:2] != '__' and not callable(c.__dict__[k]) and not isinstance(c.__dict__[k],classmethod):
                    superclass_attr[k] = c

        result = {}

        if isinstance(which,str):
            if which in self.__dict__.keys():
                return self.__dict__[which]
            elif which in class_attr:
                return self.__class__.__dict__[which]
            elif which in superclass_attr.keys():
                return superclass_attr[wich].__dict__[which]
            else:
                raise ValueError('Unknown attribute {}'.format(which))
        elif which == []:
            for key,value in superclass_attr.items():
                result[key] = value.__dict__[key]
            for item in class_attr:
                result[item] = self.__class__.__dict__[item]
            for item in self.__dict__.keys():
                result[item] = self.__dict__[item]
            return result
        else:
            for item in which:
                if item in self.__dict__.keys():
                    result[item] = self.__dict__[item]
                elif item in class_attr:
                    result[item] = self.__class__.__dict__[item]
                elif item in superclass_attr.keys():
                    return superclass_attr[item].__dict__[item]
                else:
                    raise ValueError('Unknown attribute {}'.format(which))

        return result


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    ClassAttr.clear_default()
