#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Singleton**

    A singleton pattern is a design pattern that limits the instantiation of a
    class to a single (unique) instance. This is useful when exactly one
    unique object is needed i.e. to manage an expensive resource or coordinate
    actions across modules.

    Attributes
    ----------
        None.

    Methods
    -------
    get_instance():
        Return the singleton instantce. (if accessible=True)

    reset():
        Resets the singleton instance.  (if resettable=True)

    Example
    -------

    from decoratory.singleton import Singleton

    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Create Instances
    a = Animal(name='Bello')        # Creates Bello
    b = Animal(name='Tessa')        # Returns Bello

    # Case 1: Static decoration using @Singleton or @Singleton()
    #    ---> One single object instance fits all.
    print(f"a = {a}")               # a = Animal('Bello')
    print(f"b = {b}")               # b = Animal('Bello')
    print(f"a is b: {a is b}")      # a is b: True
    print(f"a == b: {a == b}")      # a == b: True

    # Case 2: Dynamic decoration providing extra initial default values
    #    ---> Initial default values provided via the decorator
    Animal = Singleton(Animal, 'Bello')
    Animal()                        # Using the decorator's default 'Bello'
    a = Animal(name='Tessa')        # Returns Bello
    print(a)                        # Animal('Bello')

    # Case 3: Decoration using @Singleton(resettable=True)
    print(Animal(name='Bello'))     # Animal('Bello')
    print(Animal(name='Tessa'))     # Animal('Bello')   (=primary instance)
    Animal.reset()                  # Reset the singleton
    print(Animal(name='Tessa'))     # Animal('Tessa')
    print(Animal(name='Bello'))     # Animal('Tessa')   (=primary instance)

    # Case 4: Decoration using @Singleton(accessible=True)
    a = Animal(name='Bello')        # Animal('Bello')
    b = Animal.get_instance()       # Animal('Bello')   (=primary instance)
    print(a)                        # Animal('Bello')
    print(b)                        # Animal('Bello')
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Singleton"
__module__ = "singleton.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.0.4"
__date__ = "2023-06-15"
__time__ = "18:24:13"
__state__ = "Beta"
__license__ = "PSF"

__all__ = ["Singleton"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from decoratory.basic import F


# -----------------------------------------------------------------------------
# Classes
class Singleton:
    """**Singleton**

    A singleton pattern is a design pattern that limits the instantiation of a
    class to a single (unique) instance. This is useful when exactly one
    unique object is needed i.e. to manage an expensive resource or coordinate
    actions across modules.

    Attributes
    ----------
        None.

    Methods
    -------
        get_instance(): Return the singleton instantce, (if accessible=True)
        reset(): Resets the singleton instance.         (if resettable=True)

    Example
    -------

    from decoratory.singleton import Singleton

    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Create Instances
    a = Animal(name='Bello')        # Creates Bello
    b = Animal(name='Tessa')        # Returns Bello

    # Case 1: Static decoration using @Singleton or @Singleton()
    #    ---> One single object instance fits all.
    print(f"a = {a}")               # a = Animal('Bello')
    print(f"b = {b}")               # b = Animal('Bello')
    print(f"a is b: {a is b}")      # a is b: True
    print(f"a == b: {a == b}")      # a == b: True

    # Case 2: Dynamic decoration providing extra initial default values
    #    ---> Initial default values provided via the decorator
    Animal = Singleton(Animal, 'Bello')
    Animal()                        # Using the decorator's default 'Bello'
    a = Animal(name='Tessa')        # Returns Bello
    print(a)                        # Animal('Bello')

    # Case 3: Decoration using @Singleton(resettable=True)
    print(Animal(name='Bello'))     # Animal('Bello')
    print(Animal(name='Tessa'))     # Animal('Bello')   (=primary instance)
    Animal.reset()                  # Reset the singleton
    print(Animal(name='Tessa'))     # Animal('Tessa')
    print(Animal(name='Bello'))     # Animal('Tessa')   (=primary instance)

    # Case 4: Decoration using @Singleton(accessible=True)
    a = Animal(name='Bello')        # Animal('Bello')
    b = Animal.get_instance()       # Animal('Bello')   (=primary instance)
    print(a)                        # Animal('Bello')
    print(b)                        # Animal('Bello')
    """

    def __init__(self,
                 substitute: object = None,
                 *args: object,
                 accessible: bool = False,
                 resettable: bool = False,
                 **kwargs: object) -> None:
        """Set up a singleton.

        Parameters:
            substitute (object): A type to be made a singleton
            accessible (bool): If True exposes a get_instance() method
            resettable (bool): If True exposes a reset() method

        Returns:
            self (object): Singleton decorator instance
        """
        self.__set__substitute(substitute)

        # The unique instance
        self.__instance = None

        # If accessible == True exposes a get_instance() method
        if bool(accessible):
            def get_instance(s: object = self):
                """Define get_instance method"""
                return s.__instance

            # Add the get_instance method
            setattr(self, 'get_instance', get_instance)

        # If resettable == True exposes a reset() method
        if bool(resettable):
            def reset(s: object = self):
                """Define reset method"""
                s.__instance = None

            # Add the reset method
            setattr(self, 'reset', reset)

        # --- Decorator Arguments Pattern (1/2)
        if self.__substitute is not None:
            # Decoration without parameter(s)
            self.__set__substitute(F(self.__substitute, *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

    def __call__(self, *args, **kwargs):
        """Apply the decorator."""

        # --- Decorator Arguments Pattern (2/2)
        if self.__substitute is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())
            return self
        else:  # *** Wrapper ***
            # Create and store new or return existing instance
            if self.__instance is None:
                if args or kwargs:
                    self.__instance = F(self.__get__substitute().callee,
                                        *args, **kwargs).eval()
                else:
                    self.__instance = self.__get__substitute().eval()
            return self.__instance

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)


# -----------------------------------------------------------------------------
# Entry Point
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(Singleton,),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)
