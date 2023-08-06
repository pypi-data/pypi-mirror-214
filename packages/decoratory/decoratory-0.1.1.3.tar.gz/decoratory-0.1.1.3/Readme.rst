
.. _top:

==============================================================================
Decoratory
==============================================================================


**Introduction**

The *decoratory package* is based on the `Decorator Arguments Pattern`_, an
integrated concept for Python decorators with and without parameters. In
addition, all decorators created with it support complex arguments, e.g.
lists of values and functions, without unnecessarily complicating the
decoration of simple cases by these extensions. All implementation details
are described on the `project homepage`_.


**Installation** ::

    pip install --upgrade decoratory

After installation, basic information about the package, the individual
modules and their methods is also available from the command line. ::

    python -m decoratory --help

.. _toc:

**Package Contents**

The *decoratory package* available here includes some classic decorators
implemented and functionally extended with this concept, e.g.

* `Singleton`_
* `Multiton`_
* `Wrapper`_
* `Observer`_ 

This is an open list that possibly will grow over time.


**Description**

To illustrate the functionality of each module, a simple as well as a
more complex example is presented. Even if only one particular module
is needed, it is recommended to view the preceding examples as well. For even
more examples of the full range of possibilities, please refer to the
`project homepage`_.


******************************************************************************
Singleton
******************************************************************************

A `singleton pattern`_ is a design pattern that limits the instantiation of
a class to a single (unique) instance. This is useful when exactly one unique
object is needed i.e. to manage an expensive resource or coordinate actions
across modules.

As a simple example serves the decoration of the class  ``Animal`` as
singleton. In the context of the `Decorator Arguments Pattern`_, this can be
done both without brackets (decorator class) and with brackets (decorator
instance), meaning both notations describe the same functional situation.

.. code-block:: python

    # *** example_singleton.py - class Animal with Singleton decoration

    from decoratory.singleton import Singleton

    @Singleton                      # or @Singleton()
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Create Instances
    a = Animal(name='Teddy')        # Creates Teddy
    b = Animal(name='Roxie')        # Returns Teddy

If instances of the class ``Animal`` are now created, this is only done for the
very first instantiation, and for all further instantiations always this
*primary instance* is given back.

.. code-block:: python

    # *** example_singleton.py - verfication of the unique instance

    # Case 1: Static decoration using @Singleton or @Singleton()
    print(f"a = {a}")               # a = Animal('Teddy')
    print(f"b = {b}")               # b = Animal('Teddy')
    print(f"a is b: {a is b}")      # a is b: True
    print(f"a == b: {a == b}")      # a == b: True

If instead of the above *static decoration* using pie-notation, i.e. with
@-notation at the class declaration, the *dynamic decoration* within Python
code is used, additional parameters can be passed to the decorator for
passing to the class constructor.

.. code-block:: python

    # *** example_singleton.py - dynamic decoration with extra parameters

    # Case 2: Dynamic decoration providing extra initial default values
    Animal = Singleton(Animal, 'Teddy')
    Animal()                        # Using the decorator's default 'Teddy'
    a = Animal(name='Roxie')        # Returns Teddy
    print(a)                        # Animal('Teddy')

Quite generally, for all the following decorators based on this
`Decorator Arguments Pattern`_, these two properties are always fulfilled:

#. Decoration as a class (without parentheses) and Decoration as an instance
   (with empty parentheses) are equivalent
#. For dynamic decoration, extra parameters can be passed, e.g. for the
   class constructor

So far, this singleton implementation follows the concept of *once and
forever*, i.e. whenever a new instance of a class is created, one always
gets the *primary instance* back - without any possibility of ever changing
it again.

Although this behavior is consistent with the basic concept of a singleton,
there are situations where it might be useful to reset a *singleton*. Such
a *resettable singleton* could be useful to express in code that an instance
is often retrieved but rarely changed.

.. code-block:: python

    # *** example_singleton.py - decoration as 'resettable singleton'

    from decoratory.singleton import Singleton

    @Singleton(resettable=True)     # Exposes an additional reset method
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Case 3: Decoration using @Singleton(resettable=True)
    print(Animal(name='Teddy'))     # Animal('Teddy')
    print(Animal(name='Roxie'))     # Animal('Teddy')   (=primary instance)
    Animal.reset()                  # Reset the singleton
    print(Animal(name='Roxie'))     # Animal('Roxie')
    print(Animal(name='Teddy'))     # Animal('Roxie')   (=primary instance)

Without ``resettable=True`` decoration ``Animal`` has no ``reset`` method and
the call ``Animal.reset()`` will fail raising an ``AttributeError``.

With the same intention, the retrieval of the *primary instance* is also
locked by default, but can be unlocked during decoration with the
``accessible=True`` parameter, which allows ``Animal`` to expose the
``get_instance()`` method.

.. code-block:: python

    # *** example_singleton.py - decoration as 'accessible singleton'

    from decoratory.singleton import Singleton

    @Singleton(accessible=True)     # Exposes a get_instance method
    class Animal:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.name}')"

    # Case 4: Decoration using @Singleton(accessible=True)
    a = Animal(name='Teddy')        # Animal('Teddy')
    b = Animal.get_instance()       # Animal('Teddy')   (=primary instance)
    print(a)                        # Animal('Teddy')
    print(b)                        # Animal('Teddy')


******************************************************************************
Multiton
******************************************************************************

A `multiton pattern`_ is a design pattern that extends the singleton pattern.
Whereas the singleton allows for exactly one instance per class, the multiton
ensures one single (unique) *instance per key value of a dictionary*.

In this implementation the key parameter can be either any immutable type
or a callable returning such an immutable type which can be used as a key
of a dictionary. In case of an invalid key, key is set ``None`` and with only
one key value the multiton simply collapses to a singleton, therefore the
decoration ``@Multiton`` resp. ``@Multiton()`` or even ``@Multiton(key=17)``
or  ``@Multiton(key='some constant value')`` and so on always creates a
singleton.

Normally, the key is part of or is composed from the initial values of the
classified object, as in the following example, where the key function matches
the signature of the constructor and uses the initial value of the ``name``
parameter to construct a key value for the instances of ``Animal``.

.. code-block:: python

    # *** example_multitonton.py - class Animal with Multiton decoration

    from decoratory.multiton import Multiton

    @Multiton(key=lambda spec, name: name)
    class Animal:
        def __init__(self, spec, name):
            self.spec = spec
            self.name = name

        def __repr__(self):
            return f"{self.__class__.__name__}('{self.spec}', '{self.name}')"

    # Create Instances
    a = Animal('dog', name='Teddy')
    b = Animal('cat', name='Molly')
    c = Animal('dog', name='Roxie')

When instances of the class ``Animal`` are now created, this only happens for
the *first instantiation per key value*, the initial name of the animal. For
all subsequent instantiations, this *primary instance per key value* is
returned. But for each new key value, a new ``Animal`` instance is created
and stored in the internal directory.

.. code-block:: python

    # *** example_multitonton.py - One unique instance per name

    # Case 1: decoration @Multiton(key=lambda spec, name: name)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('dog', 'Roxie')

With three different names, a separate instance is created in each case.
In contrast, the following variant distinguishes only two types (equivalence
classes): animals with a character 'a' in their name and those without and
thus the key values can only be ``True`` or ``False``.

.. code-block:: python

    # *** example_multitonton.py - One unique instance per equivalence class

    # Case 2: decoration @Multiton(key=lambda spec, name: 'a' in name)
    print(a)                        # Animal('dog', 'Teddy')
    print(b)                        # Animal('cat', 'Molly')
    print(c)                        # Animal('cat', 'Molly')

The initial parameter values of the constructor can also be accessed by their
``args``-index or ``kwargs``-name. So the following decorations are also
possible:

.. code-block:: python

    # *** example_multitonton.py - Alternative decoration examples

    # Case 3: One unique instance per specie
    @Multiton(key="{0}".format)     # spec is args[0]
    class Animal:
        ...

    # Case 4: One unique instance per name
    @Multiton(key="{name}".format)  # name is kwargs['name']
    class Animal:
        ...

    # Case 5: One unique instance for all init values, i.e. no duplicates
    @Multiton(key=lambda spec, name: (spec, name))
    class Animal:
        ...

    # Case 6: One unique instance from a @staticmethod or @classmethod
    @Multiton(key=F("my_key"))      # Late binding with F(classmethod_string)
    class Animal:
        ...

        @classmethod
        def my_key(cls, spec, name):
            return 'a' in name

To actively control access to new equivalence classes, ``Multiton`` provides
the ``seal()``, ``unseal()``, and ``issealed()`` methods for sealing, unsealing,
and checking the sealing state of the ``Multiton``. By default, the sealing
state is set ``False``, so for every new key a new (unique) object is
instantiated. When sealed (e.g. later in the process) is set ``True`` the
dictionary has completed, i.e. restricted to the current object set and
any new key raises a ``KeyError``.

For deeper, special requirements on the equivalence classes of a multiton
by setting the decorator parameter ``accessible=True``, the method
``get_instances()`` is enabled, which grants direct access to the internal
directory of the instances. This can be actively manipulated in this way,
which of course should be done with care and is generally not recommended.

.. code-block:: python

    # *** example_multitonton.py - Accessibility to the internal directory

    # Case 7: with decoration @Multiton(key=lambda spec, name: 'a' in name,
    #                                   accessible=True)
    print(Animal.get_instances())   # {}
    a = Animal('dog', name='Teddy') #
    print(Animal.get_instances())   # {False: Animal('dog', 'Teddy')}
    b = Animal('cat', name='Molly') #
    c = Animal('dog', name='Roxie') #
    print(Animal.get_instances())   # {False: Animal('dog', 'Teddy'),
                                    #  True:  Animal('cat', 'Molly')}

In situations where it might be useful to reset the multiton to express in
code that instances are often retrieved but rarely modified, setting the
decorator parameter ``resettable=True`` will expose the ``reset()`` method,
by means of which the internal directory of instances can be completely cleared.

.. warning::

    Classifications into the multiton directory are done only once on
    initial key data. Subsequent changes affecting a key value are not
    reflected in the multiton directory, i.e. the directory may then be
    corrupted by such modifications.

    Therefore, **never change key related values of classified objects**!


******************************************************************************
Wrapper
******************************************************************************

As the name implies, a wrapper encloses the original function with an

* (optional) ``before`` call functionality

and/or

* (optional) ``after`` call functionality.

This implementation additionally supports an

* (optional) ``replace`` call functionality.

This generic Wrapper is all the more broadly applicable, the more flexibly
these three activities can be formulated. All three decorator parameters,
``before``, ``after`` and ``replace``, can be combined with each other and
support both single callables and (nested) lists of ``F``-types
(imported from module decoratory.basic, see below for details).
In addition, ``replace`` supports passing results from successive
replacement calls through an optional keyword argument named ``result``
(defaut value is ``None``).

Even without any of these arguments, such a *do nothing wrapper* can be used
to *overwrite* default values, for example.

.. code-block:: python

    # *** example_wrapper.py - overwrite default parameter values

    from decoratory.wrapper import Wrapper

    # Case 1: Dynamic decoration with decorator arguments, only
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    # Function call with default parameters
    some_function()                 # value = 'original'
    some_function = Wrapper(some_function, value="changed")
    some_function()                 # value = 'changed'

The functionality of ``some_function()`` itself remains unchanged. A typical
scenario for a wrapper is, of course, the execution of additional functionality
before and/or after a given functionality, which itself remains unchanged,
such as ``enter/leave`` markers, call data caches, runtime measurements, etc.
Here is a typical example:

.. code-block:: python

    # *** example_wrapper.py - enclose original function

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 2: Decoration with before and after functionalities
    def print_message(message: str = "ENTER"):
        print(message)

    @Wrapper(before=print_message, after=F(print_message, "LEAVE"))
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    some_function()                 # ENTER
                                    # value = 'original'
                                    # LEAVE

While ``before`` calls ``print_message`` with its default parameters the
``after`` parameter uses the ``F``-function from ``decoratory.basic``.
It has a signature ``F(callable, *args, **kwargs)`` and encapsulates the
passing of any function with optional positional and keyword parameters.
Accordingly, the keyword variant ``after=F(print_message, message="LEAVE")``
would also be possible.

A rather more complex example illustrates the replacement of the original
functionality with a sequence of replacement functionalities, passing a
``result`` object of type ``int`` between successive calls.

.. code-block:: python

    # *** example_wrapper.py - enclose and replacing original function

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 3: Decoration with before, after and multiple replacements
    def print_message(message: str = "UNDEFINED"):
        print(message)

    def replacement_printer(add: int = 1, *, result=None):
        result += add if isinstance(result, int) else 0
        print(f"result = {result}")
        return result

    @Wrapper(before=F(print, "ENTER"), # Python's print()
             replace=[F(replacement_printer, 1, result=0),
                      F(replacement_printer, 3),
                      F(replacement_printer, 5)],
             after=F(print_message, "LEAVE"))
    def result_printer(message: str = "UNKNOWN"):
        print(message)

    result_printer()                # ENTER         (before)
                                    # result = 1    (replacement_printer, 1)
                                    # result = 4    (replacement_printer, 3)
                                    # result = 9    (replacement_printer, 5)
                                    # LEAVE         (after)
                                    # 9             (output default_printer)

The absence of the outputs of ``UNDEFINED`` and ``UNKNOWN`` reflects the
correct replacements by the decoration, and the order of execution is exactly
as expected: ``before`` then ``replace`` then ``after`` and in each of these
variables the lists are processed in ascending order.

The *decoration of a class* always refers to the constructor of the class, e.g.

.. code-block:: python

    # *** example_wrapper.py - class decoration

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    @Wrapper(before=F(print, "BEFORE init"), after=F(print, "AFTER init"))
    class Animal:
        def __init__(self, name):
            self.name = name
            print("RUNNING init")

    # Case 4: Decoration of a class always refers to __init__
    a = Animal(name='Teddy')        # BEFORE init
                                    # RUNNING init
                                    # AFTER init


For all other methods applies:

.. note::

    Decorations to ``@staticmethod`` or ``@classmethod`` can be done
    analogously to the function decorations above, since they already exist
    at compile time. Instance methods, on the other hand, do not exist until
    an object instance is created and must be handled differently.

With ``Wrapper`` and custom service functions, a *private wrapper library*
can be built and reused.

.. code-block:: python

    # *** example_wrapper.py - private wrapper library

    from decoratory.wrapper import Wrapper
    from decoratory.basic import F

    # Case 5: Define a private wrapper library
    before_wrapper = Wrapper(before=F(print, "BEFORE"))
    after_wrapper = Wrapper(after=F(print, "AFTER"))

    # Multiple decorations for specialized functionality encapsulation
    @before_wrapper
    @after_wrapper
    def some_function(value: str = "original"):
        print(f"value = '{value}'")

    some_function()                 # BEFORE
                                    # value = 'original'
                                    # AFTER


******************************************************************************
Observer
******************************************************************************

The `observer pattern`_ is generally used to inform one or more registered
objects (observers, subscribers, objects) about selected actions of an
observed object (observable, publisher, subject).

This implementation provides several ways to decorate a function or class
as an observable or observer.

* `Observable Decoration`_
* `Observer Decoration`_
* `Static Class Decoration`_
* `Dynamic Class Decoration`_ 


Observable Decoration
---------------------

The simplest and at the same time the most Pythonic variant of decoration
is to decorate only the *observed* entities.

.. code-block:: python

    # *** example_observer.py - observable decoration

    from decoratory.observer import Observable
    from decoratory.basic import F
        
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")
    
    @Observable(observers=F(person, 'Hey, dog!'))
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")
    
    # Case 1: Observable decoration
    #    ---> Person as an observer to dog
    person()                        # person says 'Hello?'
    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # person says 'Hey, dog!' (observer to dog)

Obviously, the addressed observer, the person, must be declared before
the observed dog. With the simpler decoration 
``@Observable(observers=person)`` the person would always respond with their 
default action and say ``'Hello?'``. The usage of ``F`` enables the transfer 
of individual parameters to the observer.

To make the observers more visible in the code, an (optional) observer 
decoration is supported, i.e.

.. code-block:: python

    # *** example_observer.py - observable decoration

    from decoratory.observer import Observer

    @Observer                       # Just for the clarity of the code!
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

This makes person an ``Observer``, but here with the same result as in 
``Case 1`` above.

Due to hierarchies in stacked observer patterns, a more detailed management
of the observed objects may be necessary.

.. code-block:: python

    # *** example_observer.py - observable decoration

    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    @Observable(observers=F(person, 'Hey, cat!'))
    def cat(act: str = "Meow!"):
        print(f"{cat.__name__} acts '{act}'")

    @Observable(observers=[F(cat, 'Roar!'), F(person, 'Hey, dog!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

    # Case 2: Stacked observable decoration
    #    ---> Cat observes dog, person observes cat and dog
    person()                        # person says 'Hello?'    (person acting)

    cat()                           # cat acts 'Meow!'        (cat acting)
                                    # person says 'Hey, cat!' (observer to cat)

    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, cat!' (observer to cat)
                                    # person says 'Hey, dog!' (observer to dog)

The order of reactions is determined by the order in the list in which
the cat observes the dog prior to the person. If this order is reversed:

.. code-block:: python

    # *** example_observer.py - observable decoration

    @Observable(observers=[F(person, 'Hey, dog!'), F(cat, 'Roar!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")
        
    # Case 3: Stacked observable decoration
    #    ---> Cat observes dog, person observes dog and cat
    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # person says 'Hey, dog!' (observer to dog)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, cat!' (observer to cat)

Calling ``dog()`` results in three activities at the observers, because 
``dog()`` observes the *observed cat*, which informs the person about its own 
action. If this behavior is not desired, ``dog()`` can instead address the
*original cat* using the cat substitute callee, i.e.

.. code-block:: python

    # *** example_observer.py - observable decoration

    @Observable(observers=[F(cat.substitute.callee, 'Roar!'),
                           F(person, 'Hey, dog!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

    # Case 4: Stacked observable decoration
    #    ---> Original cat observes dog, person observes dog and cat
    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, dog!' (observer to dog)

And again, cat acts before person because of the order of the observer
list.


Observer Decoration 
-------------------

In this reverse decoration, the observer decorator collects its observables.
Because an observer decoration uses observable methods, all observable(s)
must always be declared before their observer(s).

    **1. Rule:** Declare *Observables before Observers*

Thus, the initial example ``Case 1`` from above is as follows:

.. code-block:: python

    # *** example_observer.py - observer decoration

    from decoratory.observer import Observer, Observable
    from decoratory.basic import X

    @Observable                     
    def dog(act: str = "Woof!"):    # 1. Rule: declare dog before person!
        print(f"{dog.__name__} acts '{act}'")

    @Observer(observables=X(dog, 'Hey, dog!'))
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    # Case 1: Observer decoration
    #    ---> Person as an observer to dog
    person()                        # person says 'Hello?'
    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # person says 'Hey, dog!' (observer to dog)
    
The use of the semantic ``X`` instead of ``F`` indicates that ``dog`` is the 
observable, but the ``X`` arguments are for ``person``.

For multiple decorations, the *order of decoration* is relevant. Each
observable must be decorated before it is used by the observer.

    **2. Rule:** Decorate *@Observer before @Observable*

The above situation with person, dog and cat would then look like this:

.. code-block:: python

    # *** example_observer.py - observer decoration

    @Observable                     # 2. Rule: dog before cat, person
    def dog(act: str = "Woof!"):    # 1. Rule: dog before cat, person
        print(f"{dog.__name__} acts '{act}'")

    @Observer(observables=X(dog, 'Roar!'))
    @Observable                     # 2. Rule: cat before person
    def cat(act: str = "Meow!"):    # 1. Rule: cat before person
        print(f"{cat.__name__} acts '{act}'")

    @Observer(observables=[X(dog, 'Hey, dog!'),
                           X(cat.substitute.callee, say='Hey, cat!')])
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    # Case 2: Stacked observer decoration
    #    ---> Cat observes dog, person observes cat and dog
    person()                        # person says 'Hello?'    (person acting)

    cat()                           # cat acts 'Meow!'        (cat acting)
                                    # person says 'Hey, cat!' (observer to cat)

    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, cat!' (observer to cat)
                                    # person says 'Hey, dog!' (observer to dog)

Here, the *observed cat* observes the dog, reacts and triggers the person 
observing the *orignal cat*. This situation reflects the ``Case 2`` from above.

To reproduce ``Case 3`` above, simply swap the order of the decorations at the 
cat and the person then looks at the *observed cat*.

.. code-block:: python

    # *** example_observer.py - observer decoration

    @Observable                     # 2. Rule: dog before cat, person
    def dog(act: str = "Woof!"):    # 1. Rule: dog before cat, person
        print(f"{dog.__name__} acts '{act}'")

    @Observable                     # 2. Rule: cat before person
    @Observer(observables=X(dog, 'Roar!'))
    def cat(act: str = "Meow!"):    # 1. Rule: cat before person
        print(f"{cat.__name__} acts '{act}'")

    @Observer(observables=[X(dog, 'Hey, dog!'), X(cat, say='Hey, cat!')])
    def person(say: str = "Hello?"):        # 1) Rule: dog, cat before person
        print(f"{person.__name__} says '{say}'")

    # Case 3: Stacked observer decoration
    #    ---> Cat observes dog, person observes cat and dog
    person()                        # person says 'Hello?'    (person acting)

    cat()                           # cat acts 'Meow!'        (cat acting)
                                    # person says 'Hey, cat!' (observer to cat)

    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, dog!' (observer to dog)

Note the difference: in ``Case 2``, the cat ends up as an ``Observer``, not as 
an ``Observable``. So the person observes the *original cat*. Whereas in 
``case 3``, the cat actually ends up as an ``Observable`` and person can observe 
the *observed cat*.


Static Class Decoration 
-----------------------

Both techniques, observable and observer decoration, are static, in the sense, 
decorations are done in @-notation evaluated at compile time. They are applied 
to *static functions*.

*Decoration of a class* by default addresses decoration of the 
*class constructor*, this means

.. code-block:: python

    @Observable
    class Dog:
        def __init__(self):
            pass                    # Some code ...

should be understood as

.. code-block:: python

    class Dog:
        @Observable
        def __init__(self):
            pass                    # Some code ...

But this behavior is insidious.

.. warning::

    Calling **__init__()** results in a new instance! This means calling 
    the observable induces instantiation of a new observer object, surely
    in not any case this is the desired action...

These previous two techniques can be used to decorate ``@staticmethod`` and 
``@classmethod`` that are declared and available at compile time. Things are 
different for instance methods, because instances are not available at 
compile time. They are not available until class instantiation. Therefore, 
instance methods are best decorated dynamically in the class constructor.

.. code-block:: python

    # *** example_observer.py - static class decoration

    class Agent:
        @classmethod
        def inform(cls, value):
            print(f"Informed value is: {value}")

        def report(self, value):
            print(f"Reported value is: {value}")

    class Actor:
        def __init__(self):
            self.a = 1              # Dynamic decoration, static data
            print(f"Initialization: a = {self.a}")
            self.modify = Observable(observers=[
                F(Agent.inform, 'unknown'),
                F(Agent().report, 'undefined')])(self.modify)

        def modify(self, value=1):
            self.a += value
            print(f"Modification  : a = {self.a}")

Each ``Actor`` instance defines its ``modify`` method as an observable, which 
informs about each change of ``self.a`` both the class method ``Agent.inform`` 
and the ``Agent().report`` instance method. But at the time of execution of 
``__init__()`` no (current) values or data are available yet, so only static 
reporting is possible in this way.

.. code-block:: python

    # *** example_observer.py - static class decoration

    # Case 1: Dynamic decoration, static data
    a = Actor()                     # Initialization: a = 1
    a.modify(13)                    # Modification  : a = 14
                                    # Informed value is: unknown
                                    # Reported value is: undefined

However, the problem can be tackled i.e. adding the attribute
``activate=Activation.NONE`` to the ``Observable`` definition in 
``__init__()`` to switch off default ``Activation.AFTER`` and add an 
individualized dispatch within the ``modify`` method

.. code-block:: python

    # *** example_observer.py - static class decoration

    class Actor:
        def __init__(self):
            self.a = 1              
            print(f"Initialization: a = {self.a}")
            self.modify = Observable(observers=[
                F(Agent.inform, 'unknown'),
                F(Agent().report, 'undefined')],
            # (1) Switch off default activation
                activate=Activation.NONE)(self.modify)

        def modify(self, value=1):
            self.a += value
            print(f"Modification  : a = {self.a}")
            # (2) Add individual dispatch
            self.modify.observable.dispatch(value=self.a)
    
    # Case 2: Dynamic decoration, dynamic data
    a = Actor()                     # Initialization: a = 1
    a.modify(13)                    # Modification  : a = 14
                                    # Informed value is: 14
                                    # Reported value is: 14
    

Dynamic Class Decoration 
------------------------

The classic way to exchange information between objects with the observer 
pattern is through the active use of the ``register``, ``dispatch``, and 
``unregister`` methods that an observable exports. This way, information can 
be given to the right recipients at the right places in the code. For this, 
the classes are not decorated. The dynamic decoration comes into play. 

For this, the classes remain undecorated. Dynamic decoration is used, often 
also in connection with getter/setter/property constructions, since data 
changes take place meaningfully over these methods.

Let's start with the simple classes:

.. code-block:: python

    # *** example_observer.py - daynamic class decoration
    class Note:                             # Observer without decoration!
        def info(self, thing):
            print(f"Note.info: val = {thing.a}")

    class Thing:                            # Observable without decoration!
        def __init__(self, a=0):
            self._a = a
        def inc(self):
            self._a += 1
        def get_a(self):
            return self._a
        def set_a(self, value):
            self._a = value
        a = property(get_a, set_a)

Well, some typical actions might be:

.. code-block:: python

    # *** example_observer.py - daynamic class decoration

    # (1) Setup instances
    nti = Note()                    # Note instance
    thg = Thing()                   # Thing instance

    # (2) Dynamic decoration of some methods: Late binding
    thg.inc = Observable(thg.inc)           # Late method decoration   
    Thing.set_a = Observable(Thing.set_a)   # Late property decoration 
    Thing.a = property(Thing.get_a, Thing.set_a)

    # (3) Register the observer (Note) with the observable (Thing)
    thg.inc.observable.register(F(nti.info, thg))
    thg.set_a.observable.register(F(nti.info, thing=thg))

    # Case 1: Change self.a = 0 using inc()
    thg.inc()                       # Note.info: val = 1

    # Case 2: Change self.a = 1 using setter via property
    thg.a = 2                       # Note.info: val = 2

    # Case 3: Notification from inc() to nti.info() about Thing(3)
    thg.inc.observable.dispatch(nti.info, Thing(3))
                                    # Note.info: val = 3

    # Case 4: Notification from set_a() to nti.info() about Thing(4)
    thg.set_a.observable.dispatch(nti.info, Thing(4))
                                    # Note.info: val = 4

    # Case 5: Print the current value of thg.a
    print(f"a = {thg.a}")           # a = 2     (no changes by notifications)



******************************************************************************
Version History
******************************************************************************

**Version: 0.1.1.*, Build: 2023-06-16**

- Initial version of the observer, incl. documentation

**Version: 0.1.0.3, Build: 2023-06-15**

- accessible parameter for singleton and multiton, incl. documentation
- resettable parameter for singleton and multiton, incl. documentation

**Version: 0.1.0.2, Build: 2023-06-13**

- Documentation enhancements for for singleton, multiton and wrapper

**Version: 0.1.0.1, Build: 2023-06-12**

- Initial version with singleton, multiton and wrapper


.. ===========================================================================
.. _project homepage: http://evation.eu
.. _singleton pattern: https://en.wikipedia.org/wiki/Singleton_pattern
.. _multiton pattern: https://en.wikipedia.org/wiki/Multiton_pattern
.. _observer pattern: https://en.wikipedia.org/wiki/Observer_pattern
.. _Decorator Arguments Pattern: http://evation.eu

