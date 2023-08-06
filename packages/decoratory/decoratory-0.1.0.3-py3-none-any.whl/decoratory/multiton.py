#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Multiton**

    A multiton pattern is a design pattern that extends the singleton pattern.
    Whereas the singleton allows for exactly one instance per class, the
    multiton ensures one single (unique) instance per key value of a
    dictionary.

    Attributes
    ----------
        None.

    Methods
    -------
    seal(self):
        Seal multiton.

    unseal(self):
        Unseal multiton.

    issealed(self):
        Multiton sealing state

    get_instance():
        Return the singleton instantce. (if accessible=True)

    reset():
        Resets the singleton instance.  (if resettable=True)

    Example
    -------

    from decoratory.multiton import Multiton

    # --- For alternative decorations see cases below!
    @Multiton                       # Multiton(), Multiton(key=17), ...
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create instances
    a = Animal('dog', name='Bello')
    b = Animal('cat', name='Mausi')
    c = Animal('dog', name='Tessa')

    # Case 0: decoration @Multiton or @Multiton() or @Multiton(key=17) or ...
    #    ---> With no or fixed key the Multiton acts like a Singleton
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('dog', 'Bello')
    print(c)                        # Animal('dog', 'Bello')

    # Case 1: decoration @Multiton(key=lambda spec, name: name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 2: decoration @Multiton(key=lambda spec, name: 'a' in name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('cat', 'Mausi')

    # Case 3: decoration @Multiton(key="{0}".format)
    #    ---> Parameter spec is referenced as args[0] (positional)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Bello')

    # Case 4: decoration @Multiton(key="{name}".format)
    #    ---> Parameter name is referenced as kwargs['name'] (keyword)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 5: decoration @Multiton(key=lambda spec, name: (spec, name))
    #    ---> One unique instance for all init values, i.e. no duplicates
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 6: decoration @Multiton(key=F("my_key"))
    #    ---> Late binding with F(classmethod_string)
    #         One unique instance from a @staticmethod or @classmethod
    class Animal:
        ...
        @classmethod
        def my_key(cls, spec, name):
            return 'a' in name
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('cat', 'Mausi')

    # Case 7: decoration @Multiton(key=lambda spec, name: name,
    #                              accessible=True, resettable=True)
    #    ---> Seal after Bello
    Animal.reset()                  # Reset/Clear the instance dictionary
    print(Animal.get_instances())   # {}
    print(Animal.issealed())        # False
    a = Animal('dog', name='Bello') # Animal('dog', 'Bello')
    Animal.seal()                   # Seal it!
    print(Animal.issealed())        # True
    b = Animal('dog', name='Bello') # Returns primary instance
    print(a is b)                   # True
    try:
        c = Animal('dog', name='Tessa')
    except KeyError as ex:          # KeyError, Animal is sealed!
        print(f"For '{ex.args[1]}' {ex.args[0]}")
    print(Animal.get_instances())   # {'Bello': Animal('dog', 'Bello')}
    Animal.unseal()                 # Unseal it!
    c = Animal('dog', name='Tessa') # Animal('dog', 'Bello') now it's ok!
    print(Animal.get_instances())   # {'Bello': Animal('dog', 'Bello'),
                                    #  'Tessa': Animal('dog', 'Tessa')}
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Multiton"
__module__ = "multiton.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.0.5"
__date__ = "2023-06-15"
__time__ = "18:24:13"
__state__ = "Beta"
__license__ = "PSF"

__all__ = ["Multiton"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Classes
class Multiton:
    """**Multiton**

    A multiton pattern is a design pattern that extends the singleton pattern.
    Whereas the singleton allows for exactly one instance per class, the
    multiton ensures one single (unique) instance per key value of a
    dictionary.

    Attributes
    ----------
        None.

    Methods
    -------
    seal(self):
        Seal multiton.

    unseal(self):
        Unseal multiton.

    issealed(self):
        Multiton sealing state

    get_instance():
        Return the singleton instantce. (if accessible=True)

    reset():
        Resets the singleton instance.  (if resettable=True)

    Example
    -------

    from decoratory.multiton import Multiton

    # --- For alternative decorations see cases below!
    @Multiton                       # Multiton(), Multiton(key=17), ...
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create instances
    a = Animal('dog', name='Bello')
    b = Animal('cat', name='Mausi')
    c = Animal('dog', name='Tessa')

    # Case 0: decoration @Multiton or @Multiton() or @Multiton(key=17) or ...
    #    ---> With no or fixed key the Multiton acts like a Singleton
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('dog', 'Bello')
    print(c)                        # Animal('dog', 'Bello')

    # Case 1: decoration @Multiton(key=lambda spec, name: name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 2: decoration @Multiton(key=lambda spec, name: 'a' in name)
    #    ---> key is a function evaluating the attribute name from __init__(..)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('cat', 'Mausi')

    # Case 3: decoration @Multiton(key="{0}".format)
    #    ---> Parameter spec is referenced as args[0] (positional)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Bello')

    # Case 4: decoration @Multiton(key="{name}".format)
    #    ---> Parameter name is referenced as kwargs['name'] (keyword)
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 5: decoration @Multiton(key=lambda spec, name: (spec, name))
    #    ---> One unique instance for all init values, i.e. no duplicates
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('dog', 'Tessa')

    # Case 6: decoration @Multiton(key=F("my_key"))
    #    ---> Late binding with F(classmethod_string)
    #         One unique instance from a @staticmethod or @classmethod
    class Animal:
        ...
        @classmethod
        def my_key(cls, spec, name):
            return 'a' in name
    print(a)                        # Animal('dog', 'Bello')
    print(b)                        # Animal('cat', 'Mausi')
    print(c)                        # Animal('cat', 'Mausi')

    # Case 7: decoration @Multiton(key=lambda spec, name: name,
    #                              accessible=True, resettable=True)
    #    ---> Seal after Bello
    Animal.reset()                  # Reset/Clear the instance dictionary
    print(Animal.get_instances())   # {}
    print(Animal.issealed())        # False
    a = Animal('dog', name='Bello') # Animal('dog', 'Bello')
    Animal.seal()                   # Seal it!
    print(Animal.issealed())        # True
    b = Animal('dog', name='Bello') # Returns primary instance
    print(a is b)                   # True
    try:
        c = Animal('dog', name='Tessa')
    except KeyError as ex:          # KeyError, Animal is sealed!
        print(f"For '{ex.args[1]}' {ex.args[0]}")
    print(Animal.get_instances())   # {'Bello': Animal('dog', 'Bello')}
    Animal.unseal()                 # Unseal it!
    c = Animal('dog', name='Tessa') # Animal('dog', 'Bello') now it's ok!
    print(Animal.get_instances())   # {'Bello': Animal('dog', 'Bello'),
                                    #  'Tessa': Animal('dog', 'Tessa')}
    """

    def __init__(self,
                 substitute: type = None,
                 *args: object,
                 key: Union[F, callable, object, None] = None,
                 accessible: bool = False,
                 resettable: bool = False,
                 **kwargs: object) -> None:
        """Set up a multiton.

        Parameters:
            substitute (object): A type to be made a multiton
            key: (F|callable|object|None): Instance key.
            accessible (bool): If True exposes a get_instance() method
            resettable (bool): If True exposes a reset() method

        Returns:
            self (object): Multiton decorator instance
        """
        self.__set__substitute(substitute)
        self.__key = key

        # Dictionary for unique key instances
        self.__instances = dict()

        # Sealing state
        self.__sealed = False

        # If accessible == True exposes a get_instances() method
        if bool(accessible):
            def get_instances(s: object = self):
                """Return dictionary of all instance representations."""
                return s.__instances

            # Add the instances method
            setattr(self, 'get_instances', get_instances)

        # If resettable == True exposes a reset() method
        if bool(resettable):
            def reset(s: object = self):
                """Define reset method"""
                s.__instances.clear()

            # Add the reset method
            setattr(self, 'reset', reset)

        # --- Decorator Arguments Pattern (1/2)
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

    def __call__(self, *args, **kwargs):
        """Apply the decorator"""
        # --- Decorator Arguments Pattern (2/2)
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())
            return self
        else:  # *** Wrapper ***
            # If no current values, take defaults
            if args or kwargs:
                subst = F(self.__get__substitute().callee, *args, **kwargs)
            else:
                subst = self.__get__substitute()

            # Calculate key from callable or read key from arguments
            try:
                if isinstance(self.__key, F):  # classmethod or staticmethod
                    d_key = F(
                        getattr(self.substitute.callee, self.__key.callee),
                        *subst.callee_args, **subst.callee_kwargs).eval()
                elif callable(self.__key):  # function
                    d_key = F(self.__key, *subst.callee_args,
                              **subst.callee_kwargs).eval()
                else:  # Value
                    d_key = self.__key
                instance = self.__instances.get(d_key, None)
            except (TypeError, Exception):  # Default is None
                d_key = None
                instance = self.__instances.get(d_key, None)

            # Create and store new or return existing instance (by key)
            if instance is None:
                if self.__sealed:
                    raise KeyError(f"{self.__name__} is sealed.", d_key)
                instance = self.__instances.setdefault(d_key, subst.eval())

            return instance

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    # Methods
    def seal(self):
        """Seal multiton.

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = True

    def unseal(self):
        """Unseal multiton .

        Parameters:
            None.

        Returns:
            None.
        """
        self.__sealed = False

    def issealed(self):
        """Multiton sealing state

        Parameters:
            None.

        Returns:
            True/False (bool): Sealing state.
        """
        return self.__sealed


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(Multiton,),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
