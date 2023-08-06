#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Observer Pattern**

    The observer pattern is generally used to inform one or more registered
    objects (observers, subscribers, objects) about selected actions of an
    observed object (observable, publisher, subject).

    This implementation provides several ways to decorate a function or class
    as an Observable or Observer.

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
        Return the singleton instance.  (if accessible=True)

    reset():
        Resets the singleton instance.  (if resettable=True)

    Example
    -------

    A) Observable Decoration

    The simplest and at the same time the most Pythonic variant of decoration
    is to decorate only the *observed* entities. This is possible because all
    observer pattern functionalities are concentrated in the BaseClass
    (=BaseObservable) of the observable decorator, while the BaseClass
    (=BaseObserver) of the observer decorator remains empty here. If
    necessary, it is possible to inherit from both BaseClasses to extend
    their functionalities.

    from decoratory.observer import Observable

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

    Obviously, the addressed observer, the person, must be specified before
    the observed, the dog. To make the observers more visible in the code, an
    (optional) observer decoration is supported, i.e.

    @Observer                       # Just for the clarity of the code!
    def person(say: str = "Hello?"):
        print(f"{person.__name__} says '{say}'")

    This makes person an observer, but here with the same result as above.

    Due to hierarchies in stacked observer patterns, a more detailed management
    of the observed objects may be necessary.

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

    @Observable(observers=[F(person, 'Hey, dog!'), F(cat, 'Roar!')])
    def dog(act: str = "Woof!"):
        print(f"{dog.__name__} acts '{act}'")

    # Case 3: Stacked observable decoration
    #    ---> Cat observes dog, person observes dog and cat
    dog()                           # dog acts 'Woof!'        (dog acting)
                                    # person says 'Hey, dog!' (observer to dog)
                                    # cat acts 'Roar!'        (observer to dog)
                                    # person says 'Hey, cat!' (observer to cat)

    Calling dog() results in three activities at the observers, because dog()
    observes the 'observed cat', which informs the person about its own action.
    If this behavior is not desired, dog() can instead address the
    'original cat' using the cat substitute, i.e.

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


    B) Observer Decoration

    In this reverse decoration, the observer decorator defines its observables.
    Because an observer decoration uses observable methods, all observable(s)
    must always be declared before their observer(s).

    1. Rule: Declare Observables before Observers

    Thus, the initial example Case 1 from above is as follows:

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

    The use of the semantic X instead of F indicates that dog is the
    observable, but the X arguments are for person.

    For multiple decorations, the order of decoration is relevant. Each
    observable must be decorated before it is used by the observer.

    2. Rule: Decorate @Observer before @Observable

    The above situation with person, dog and cat would then look like this:

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

    Here, the observed cat observes the dog, reacts and triggers the person
    observing the orignal cat. This situation reflects the Case 2 from above.

    To reproduce Case 3 above, simply swap the order of the decorations at the
    cat and the person then looks at the observed cat.

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

    Note the difference: in Case 2, the cat ends up as an Observer, not as an
    Observable. So the person observes the original cat. Whereas in case 3,
    the cat actually ends up as an Observable and person can observe the
    observed cat.


    C) Static Class Decoration

    Both techniques, observable and observer decoration, are static, in the
    sense, decorations are done in @-notation evaluated at compile time. They
    are applied to *static functions*.

    Decoration of a class by default addresses decoration of the class
    constructor, this means

    @Observable
    class Dog:
        def __init__(self):
            pass                    # Some code ...

    should be understood as

    class Dog:
        @Observable
        def __init__(self):
            pass                    # Some code ...

    But this behavior is insidious.

    WARNING: Calling __init__() results in a new instance! This means calling
             the observable induces instantiation of a new observer object,
             surely in not any case this is the desired action...

    These previous two techniques can be used to decorate @staticmethod and
    @classmethod that are declared and available at compile time. Things are
    different for instance methods, because instances are not available at
    compile time. They are not available until class instantiation. Therefore,
    instance methods are best decorated dynamically in the class constructor.

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

    Each Actor instance defines its modify method as an observable, which
    informs about each change of self.a both the class method Agent.inform
    and the Agent().report instance method. But at the time of execution of
    __init__ no (current) values or data are available yet, so only static
    reporting is possible in this way.

    # Case 1: Dynamic decoration, static data
    a = Actor()                     # Initialization: a = 1
    a.modify(13)                    # Modification  : a = 14
                                    # Informed value is: unknown
                                    # Reported value is: undefined

    However, the problem can be tackled i.e. adding the attribute
    activate=Activation.NONE to the Observable definition in __init__ to
    switch off default Activation.AFTER and add an individualized dispatch
    within the modify method

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


    D) Dynamic Class Decoration

    The classic way to exchange information between objects with the observer
    pattern is through the active use of the register, dispatch, and unregister
    methods that an observable exports. This way, information can be given to
    the right recipients at the right places in the code. For this, the
    classes are not decorated. The dynamic decoration comes into play.

    For this, the classes remain undecorated. Dynamic decoration is used,
    often also in connection with getter/setter/property constructions, since
    data changes take place meaningfully over these methods.

    Let’s start with the simple classes:

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
"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Observer"
__module__ = "observer.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.1.2"
__date__ = "2023-06-16"
__time__ = "19:56:14"
__state__ = "Beta"
__license__ = "PSF"

__all__ = ["Observer", "BaseObserver", "Observable", "BaseObservable"]

# -----------------------------------------------------------------------------
# Libraries & Modules
from functools import update_wrapper
from typing import Union
from decoratory.basic import Activation, F, Parser, X


# -----------------------------------------------------------------------------
# Classes
class BaseObservable:
    """**Observable Base Class**

    A base implementation of the (abstract) observable base class. It manages
    (abstract) observers (of F-type) within a private dictionary using the
    methods:

    register  : Register an observer for callback
    unregister: Unregister an observer
    dispatch  : Dispatch a given observer or even all observers
    observers : Dictionary of all registered observers (of F-type)

    While the methods register, unregister and observers only handles given
    data into F objects and/or collects them, the dispatch method applies F's
    eval method (without arguments!) to them. It's in the user's responsibility
    to make sure that these calls succeed, i.e. for a class or instance/object
    method of class A or an instance a = A():
     - Registration call:   F(a.method, *args, **kwargs).eval()         or
                            F('method', a, *args, **kwargs).eval()      but not
     - Dynamic call:        F('method', *args, **kwargs).eval(obj=a)
    """

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

        self.__observers = dict()  # dict of F-type observers: callee is key!

    # Methods of the Observer Pattern
    def register(self,
                 observer: Union[F, callable, str],
                 *observer_args,
                 **observer_kwargs) -> None:
        """Register a function (callable) or method (str) for callback.

        Parameters:
            observer (F|callable|str): Callback function|method of the observer
            observer_args (object): Callback (default) positional arguments
            observer_kwargs (object): Callback (default) keyword arguments

        Returns:
            None.
        """
        if isinstance(observer, F):
            if observer_args or observer_kwargs:
                observer.callee_args = observer_args
                observer.callee_kwargs = observer_kwargs
            self.__observers[observer.callee] = observer  # Override mode
        elif callable(observer) or isinstance(observer, str):
            obs = F(observer, *observer_args, **observer_kwargs)
            self.__observers[observer] = obs
        else:
            raise TypeError(f"'{observer}' cannot be registered.")

    def unregister(self,
                   observer: Union[F, callable, str, None] = None) -> None:
        """Unregister an observer.

        If the observer parameter is omitted (None), all registered observers
        will be unregistered.

        Parameters:
            observer (F|callable|str|None): Callback to be unregistered

        Returns:
            None.
        """
        if observer is None:
            self.__observers.clear()
        elif isinstance(observer, F):
            self.__observers.pop(observer.callee, None)  # Quiet mode
        elif callable(observer) or isinstance(observer, str):
            self.__observers.pop(observer, None)  # Quiet mode
        else:
            raise TypeError(f"'{observer}' cannot be unregistered.")

    def dispatch(self,
                 observer: Union[F, callable, str, None] = None,
                 *observer_args,
                 **observer_kwargs) -> None:
        """Dispatch an observer.

        If the observer parameter is omitted (None), all registered observers
        will be dispatched.

        Parameters:
            observer (F|callable|str|None): Callback to be dispatched
            observer_args (object): Callback (default) positional arguments
            observer_kwargs (object): Callback (default) keyword arguments

        Returns:
            None.
        """
        if observer is None:
            # Registration call using default arguments, no extra eval obj!
            if observer_args or observer_kwargs:
                for obs in self.__observers.values():
                    F(obs.callee, *observer_args, **observer_kwargs).eval()
            else:
                for obs in self.__observers.values():
                    obs.eval()
        elif isinstance(observer, F):
            # Dynamic call using current/default arguments, no extra eval obj!
            if observer_args or observer_kwargs:
                F(observer.callee, *observer_args, **observer_kwargs).eval()
            else:
                observer.eval()
        elif callable(observer):
            # Dynamic call using current arguments, no extra eval obj!
            F(observer, *observer_args, **observer_kwargs).eval()
        elif isinstance(observer, str):
            pass  # todo: str???
        else:
            raise TypeError(f"'{observer}' cannot be dispatched.")

    def observers(self, classbased=False) -> dict:
        """Listing of all observers.

        Observers are collected in a dict, which is returned by default with
        classbased=False. Calling with classbased=True returns a dictionary
        with key-value-pair syntax {classname: list(methods)}.

        Parameters:
            classbased (bool): A boolean switch for returned data structure

        Returns:
            observers (dict): Dictionary of all observers
        """
        if bool(classbased):
            result = dict()
            for obs in self.__observers.values():
                *skip, cls, mtd = obs.callee.__qualname__.split(".")
                result.setdefault(cls, []).append(obs)
            return result
        else:
            return self.__observers  # Has to be the default (without params)!


class Observable:
    """**Observable** (Publisher, Subject)

    Creating an observable instantiates a callable object which exposes the
    four basic observable pattern methods register, unregister, dispatch and
    observers via an observable attribute for an instance of BaseClass
    (default = BaseObservable) as well as the original decorator arguments,
    if present, like the callable to be substituted, observers, methods and
    activation point in time.
    """

    BaseClass = BaseObservable

    def __init__(self,
                 substitute: Union[callable, type] = None,
                 *args: object,
                 observers: Union[list, F, callable, str] = None,
                 methods: Union[list, F, callable, str] = None,
                 activate: Activation = Activation.AFTER,
                 **kwargs: object) -> None:
        """Observable (Publisher, Subject).

        Parameters:
            substitute (callable|type: Callable|Type to be made an observable
            observers (list|F|callable|str): (List of) callable(s) of observers
            methods (list|F|callable|str): (List of) callable(s) of as strings
            activate (Activation): Dispatch activation point in time

        Returns:
            None.
        """
        self.__set__substitute(substitute)
        self.__set__observers(observers)
        self.__set__methods(methods)
        self.__set__activate(activate)

        # --- Decorator Arguments Pattern (1/2)
        if self.__get__substitute() is not None:
            # Decoration without parameter(s)
            self.__set__substitute(
                F(self.__get__substitute(), *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Instance of BaseObservable
            self.__set__observable(Observable.BaseClass())
        else:
            # Decoration with parameter(s)
            self.__set__decorator_args(args)
            self.__set__decorator_kwargs(kwargs)

            # Instance of BaseObservable
            self.__set__observable(Observable.BaseClass(
                *self.__get__decorator_args(),
                **self.__get__decorator_kwargs()))

    def __call__(self, *args, **kwargs):
        # --- Decorator Arguments Pattern (2/2)
        if self.__get__substitute() is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))

            # Decoration of a type means decoration of *all* submitted methods
            if self.__get__methods():
                # Resolve list of methods:
                subst = self.__get__substitute().callee
                for mtd, mtd_args, mtd_kwargs in self.__get__methods():
                    if isinstance(mtd, str) and hasattr(subst, mtd):
                        mtds = mtd
                        mtd0 = getattr(subst, mtds)
                    elif callable(mtd):
                        mtds = mtd.__name__
                        mtd0 = mtd
                    else:
                        raise TypeError(f"{mtd} is nor a string nor callable.")
                    # noinspection PyArgumentEqualDefault
                    mtd1 = Observable(
                        None,  # Call with deco arguments (substitute is None)
                        *self.__get__decorator_args(),
                        observers=self.__get__observers(),
                        methods=None,  # Resolved, call to else part below!
                        activate=self.__get__activate(),
                        **self.__get__decorator_kwargs())(
                        mtd0, *mtd_args, **mtd_kwargs)
                    setattr(subst, mtds, mtd1)

                # Return the undecorated original class
                return subst
            else:
                # Setup observers
                if self.__get__observers():
                    for observer in self.__get__observers():
                        self.__get__observable().register(observer)

                # Complete wrapper and return observable
                update_wrapper(self, self.__get__substitute().callee,
                               updated=())
                return self
        else:  # *** Wrapper ***
            # Dispatch BEFORE
            if self.__get__activate() & Activation.BEFORE:
                self.__get__observable().dispatch()

            # Delegation: apply the substitute, current before default values
            if args or kwargs:
                result = F(self.__get__substitute().callee, *args,
                           **kwargs).eval()
            else:
                result = self.__get__substitute().eval()

            # Dispatch AFTER
            if self.__get__activate() & Activation.AFTER:
                self.__get__observable().dispatch()

            return result

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__decorator_args(self):
        return self.__decorator_args

    def __set__decorator_args(self, value):
        self.__decorator_args = value

    decorator_args = property(__get__decorator_args)

    def __get__decorator_kwargs(self):
        return self.__decorator_kwargs

    def __set__decorator_kwargs(self, value):
        self.__decorator_kwargs = value

    decorator_kwargs = property(__get__decorator_kwargs)

    def __get__observers(self):
        return self.__observers

    def __set__observers(self, value):
        self.__observers: list = Parser.eval(value)

    observers = property(__get__observers)

    def __get__methods(self):
        return self.__methods

    def __set__methods(self, value):
        self.__methods: list = Parser.eval(value)

    methods = property(__get__methods)

    def __get__observable(self):
        return self.__observable

    def __set__observable(self, value):
        self.__observable = value

    observable = property(__get__observable)

    def __get__activate(self):
        return self.__activate

    def __set__activate(self, activate):
        self.__activate = activate if isinstance(
            activate, Activation) else Activation.NONE

    activate = property(__get__activate, __set__activate)


class BaseObserver:
    """**Observer Base Class**

    A base implementation of the (abstract) observer base class.

    As long as this class, just like here, is an empty dummy, decoration of a
    callable as an observer is optional. If BaseObserver is overwritten and
    assigned to the observers BaseClass attribute all non captured decorator
    args & kwargs will be submitted to be used in customized class
    functionalities.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Observer:
    """**Observer** (Subscriber, Object)

    Creating an observer instantiates a callable object which exposes the
    original decorator arguments, if present, like the callable to be
    substituted, observables and methods.
   """

    BaseClass = BaseObserver

    def __init__(self,
                 substitute: Union[callable, type] = None,
                 *args: object,
                 observables: Union[list, X, callable, str] = None,
                 methods: Union[list, X, callable, str] = None,
                 **kwargs: object) -> None:
        """**Observer** (Subscriber, Object)

        @param substitute: The callable or type to be made an observable
        @param observables: (List of) callable(s) of observables
        @param methods: (List of) callable(s) of method strings
        @rtype: NoneType
            """
        self.__set__substitute(substitute)
        self.__set__observables(observables)
        self.__set__methods(methods)

        # --- Decorator Arguments Pattern (1/2)
        if self.__get__substitute() is not None:
            # Decoration without parameter(s)
            self.__set__substitute(
                F(self.__get__substitute(), *args, **kwargs))
            update_wrapper(self, self.__get__substitute().callee, updated=())

            # Instance of BaseObserver
            self.__set__observer(Observer.BaseClass())
        else:
            # Decoration with parameter(s)
            self.__set__decorator_args(args)
            self.__set__decorator_kwargs(kwargs)

            # Instance of BaseObserver
            self.__set__observer(Observer.BaseClass(
                *self.__get__decorator_args(),
                **self.__get__decorator_kwargs()))

    def __call__(self, *args, **kwargs):
        # --- Decorator Arguments Pattern (2/2)
        if self.__get__substitute() is None:
            # Decoration with parameter(s)
            self.__set__substitute(F(args[0], *args[1:], **kwargs))

            # Decoration of a type means decoration of *all* submitted methods
            if self.__get__methods():
                # Resolve list of methods:
                subst = self.__get__substitute().callee
                for mtd, mtd_args, mtd_kwargs in self.__get__methods():
                    if isinstance(mtd, str) and hasattr(subst, mtd):
                        mtds = mtd
                        mtd0 = getattr(subst, mtds)
                    elif callable(mtd):
                        mtds = mtd.__name__
                        mtd0 = mtd
                    else:
                        raise TypeError(f"{mtd} is nor a string nor callable.")
                    # noinspection PyArgumentEqualDefault
                    mtd1 = Observer(
                        None,  # Call with deco arguments (substitute is None)
                        *self.__get__decorator_args(),
                        observables=self.__get__observables(),
                        methods=None,  # Resolved, call to else part below!
                        **self.__get__decorator_kwargs())(
                        mtd0, *mtd_args, **mtd_kwargs)
                    setattr(subst, mtds, mtd1)

                # Return the undecorated original class
                return subst
            else:
                # Register self as a callable object for callback
                # CAUTION: observables is a list of X-objects with semantics
                #     obs = X(observABLE, observER_args, observER_kwargs)
                # The arguments belong to the observer (self) but not to the
                # observable from the observables list!
                if self.__get__observables():
                    for observable in self.__get__observables():
                        if isinstance(observable.callee, Observable):
                            observable.callee.observable.register(
                                self, *observable.callee_args,
                                **observable.callee_kwargs)
                        else:
                            raise TypeError(
                                f"{observable.callee} is not an observable.")

                # Complete wrapper and return observer
                update_wrapper(self, self.__get__substitute().callee,
                               updated=())
                return self
        else:  # *** Wrapper ***
            # Delegation: apply the substitute, current before default values
            if args or kwargs:
                return F(self.__get__substitute().callee, *args,
                         **kwargs).eval()
            else:
                return self.__get__substitute().eval()

    # Getter, Setter, Properties
    def __get__substitute(self):
        return self.__substitute

    def __set__substitute(self, value):
        self.__substitute = value

    substitute = property(__get__substitute)

    def __get__decorator_args(self):
        return self.__decorator_args

    def __set__decorator_args(self, value):
        self.__decorator_args = value

    decorator_args = property(__get__decorator_args)

    def __get__decorator_kwargs(self):
        return self.__decorator_kwargs

    def __set__decorator_kwargs(self, value):
        self.__decorator_kwargs = value

    decorator_kwargs = property(__get__decorator_kwargs)

    def __get__observables(self):
        return self.__observables

    def __set__observables(self, value):
        self.__observables: list = Parser.eval(value)

    observables = property(__get__observables)

    def __get__methods(self):
        return self.__methods

    def __set__methods(self, value):
        self.__methods: list = Parser.eval(value)

    methods = property(__get__methods)

    def __get__observer(self):
        return self.__observer

    def __set__observer(self, value):
        self.__observer = value

    observer = property(__get__observer)


# -----------------------------------------------------------------------------
# Simple example
if __name__ == '__main__':
    from decoratory.banner import __banner as banner

    banner(title=__title__,
           version=__version__,
           date=__date__,
           time=__time__,
           docs=(BaseObserver, Observer, BaseObservable, Observable),
           author=__author__,
           maintainer=__maintainer__,
           company=__company__,
           email=__email__,
           url=__url__,
           copyright=__copyright__,
           state=__state__,
           license=__license__)


    #
    # def __test03():
    #     # ---------------------------------------------------------------------
    #     # Class decoration (dynamic)
    #     class DftFormatter:
    #         """Default Formatter"""
    #
    #         def __init__(self, name):
    #             self.name = name
    #             self._data = 0
    #             print(f"{self.__class__.__name__}: "
    #                   f"{self.name} has data {self._data}")
    #
    #         def __str__(self):
    #             return f"{self.__class__.__name__}({self.name}, {self._data})"
    #
    #         def get_data(self):
    #             """Getter"""
    #             return self._data
    #
    #         def set_data(self, value):
    #             self._data = value
    #
    #         data = property(get_data, set_data)
    #
    #     class HexFormatter(DftFormatter):
    #         """Hex Formatter"""
    #
    #         def notify(self, resource):
    #             """Notifier"""
    #             value = hex(resource.data)
    #             print(f"{self.__class__.__name__}: "
    #                   f"{resource.name} has data {value}")
    #
    #     class BinFormatter(DftFormatter):
    #         """Binary Formatter"""
    #
    #         def notify(self, resource):
    #             """Notifier"""
    #             value = bin(resource.data)
    #             print(f"{self.__class__.__name__}: "
    #                   f"{resource.name} has data {value}")
    #
    #     # Instances
    #     print("Instantiation:")
    #     df = DftFormatter('Dfter')
    #     hf = HexFormatter('Hexer')
    #     bf = BinFormatter('Biner')
    #
    #     # Setup Observable for a property
    #     DftFormatter.set_data = Observable(DftFormatter.set_data)
    #     DftFormatter.data = property(DftFormatter.get_data,
    #                                  DftFormatter.set_data)
    #
    #     hf.notify = Observer(hf.notify)  # Optional
    #     bf.notify = Observer(bf.notify)  # Optional
    #
    #     # noinspection PyTypeHints
    #     df.set_data: Observable
    #
    #     # Register Observer with default resource argument
    #     df.set_data.observable.register(F(hf.notify, df))
    #     df.set_data.observable.register(F(bf.notify, resource=df))
    #
    #     # Change data using the property
    #     print("\nChange data: 2")
    #     df.data = 2
    #
    #     # Some additional dispatches
    #     print("\nAdditional dispatches: df, bf, all(2)")
    #     df.set_data.observable.dispatch(hf.notify, df)
    #     df.set_data.observable.dispatch(BinFormatter.notify, bf, df)
    #     print()
    #     df.set_data.observable.dispatch(resource=df)
    #
    #     # List all observers
    #     print("\nList all observers:")
    #     print(df.set_data.observable.observers())
    #     print(df.set_data.observable.observers(classbased=True))
    #
    #     # Unregister bf
    #     print("\nUnregister bf:")
    #     df.set_data.observable.unregister(bf.notify)
    #     print(df.set_data.observable.observers())
    #
    #     # Unregister all
    #     print("\nUnregister all:")
    #     df.set_data.observable.unregister()
    #     print(df.set_data.observable.observers())
    #
    #
    # # -------------------------------------------------------------------------
    # # Apply tests
    # print("----------")
    # __test01()

    # print("----------")
    # __test02()
    # print("----------")
    # __test03()
    # print("----------")

