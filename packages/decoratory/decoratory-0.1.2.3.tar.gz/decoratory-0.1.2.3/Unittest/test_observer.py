#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# vim: fileencoding=UTF-8 tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -----------------------------------------------------------------------------
# Document Description
"""**Test Observer**"""

# -----------------------------------------------------------------------------
# Module Level Dunders
__title__ = "Test Observer"
__module__ = "test_observer.py"
__author__ = "Martin Abel"
__maintainer__ = "Martin Abel"
__credits__ = ["Martin Abel"]
__company__ = "eVation"
__email__ = "python@evation.eu"
__url__ = "http://evation.eu"
__copyright__ = f"(c) copyright 2020-2023, {__company__}"
__created__ = "2020-01-01"
__version__ = "0.1.2.2"
__date__ = "2023-06-18"
__time__ = "10:46:02"
__state__ = "Beta"
__license__ = "PSF"

# -----------------------------------------------------------------------------
# Libraries & Modules
import unittest

from decoratory.observer import (BaseObservable, BaseObserver,
                                         Observable, Observer,
                                         Activation, F, X)


# -----------------------------------------------------------------------------
# Test Class
# noinspection PyPep8Naming
# noinspection PyUnresolvedReferences
# noinspection PyArgumentEqualDefault
# noinspection PyPropertyAccess
class TestObserver(unittest.TestCase):

    def setUp(self):
        """Preparation"""
        pass

    def tearDown(self):
        """Wrap-up"""
        pass

    def test_basics_nodecos_noparams_without_brackets(self):
        """Unittest: Observable & Observer - nodecos, noparams, nobrackets"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Dog = Observable(dog)
        Person = Observer(person)

        # Basic checks for Dog
        self.assertTrue(isinstance(Dog, Observable))
        self.assertIs(Dog.BaseClass, BaseObservable)
        self.assertTrue(isinstance(Dog.observable, Dog.BaseClass))
        self.assertTrue(hasattr(Dog.observable, 'register'))
        self.assertTrue(hasattr(Dog.observable, 'unregister'))
        self.assertTrue(hasattr(Dog.observable, 'dispatch'))
        self.assertTrue(hasattr(Dog.observable, 'observers'))
        self.assertTupleEqual(Dog.observable.args, ())
        self.assertDictEqual(Dog.observable.kwargs, {})
        self.assertIs(Dog.activate, Activation.AFTER)
        self.assertFalse(hasattr(Dog, 'decorator_args'))
        self.assertFalse(hasattr(Dog, 'decorator_kwargs'))
        self.assertListEqual(Dog.methods, [])
        self.assertIs(Dog.substitute.callee, dog)
        self.assertTupleEqual(Dog.substitute.callee_args, ())
        self.assertDictEqual(Dog.substitute.callee_kwargs, {})
        self.assertIs(Dog.__annotations__, dog.__annotations__)
        self.assertIs(Dog.__doc__, dog.__doc__)
        self.assertIs(Dog.__name__, dog.__name__)

        # Basic checks for Person
        self.assertTrue(isinstance(Person, Observer))
        self.assertIs(Person.BaseClass, BaseObserver)
        self.assertTrue(isinstance(Person.observer, Person.BaseClass))
        self.assertTupleEqual(Person.observer.args, ())
        self.assertDictEqual(Person.observer.kwargs, {})
        self.assertFalse(hasattr(Person, 'decorator_args'))
        self.assertFalse(hasattr(Person, 'decorator_kwargs'))
        self.assertListEqual(Person.methods, [])
        self.assertListEqual(Person.observables, [])
        self.assertIs(Person.substitute.callee, person)
        self.assertTupleEqual(Person.substitute.callee_args, ())
        self.assertDictEqual(Person.substitute.callee_kwargs, {})
        self.assertIs(Person.__annotations__, person.__annotations__)
        self.assertIs(Person.__doc__, person.__doc__)
        self.assertIs(Person.__name__, person.__name__)

        # Basic calls deliver function defaults
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_basics_nodecos_noparams_with_empty_brackets(self):
        """Unittest: Observable & Observer - nodecos, noparams, brackets"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Dog = Observable()(dog)
        Person = Observer()(person)

        # Basic checks for Dog
        self.assertTrue(isinstance(Dog, Observable))
        self.assertIs(Dog.BaseClass, BaseObservable)
        self.assertTrue(isinstance(Dog.observable, Dog.BaseClass))
        self.assertTrue(hasattr(Dog.observable, 'register'))
        self.assertTrue(hasattr(Dog.observable, 'unregister'))
        self.assertTrue(hasattr(Dog.observable, 'dispatch'))
        self.assertTrue(hasattr(Dog.observable, 'observers'))
        self.assertTupleEqual(Dog.observable.args, ())
        self.assertDictEqual(Dog.observable.kwargs, {})
        self.assertIs(Dog.activate, Activation.AFTER)
        self.assertTupleEqual(Dog.observable.args, ())
        self.assertDictEqual(Dog.observable.kwargs, {})
        self.assertListEqual(Dog.methods, [])
        self.assertIs(Dog.substitute.callee, dog)
        self.assertTupleEqual(Dog.substitute.callee_args, ())
        self.assertDictEqual(Dog.substitute.callee_kwargs, {})
        self.assertIs(Dog.__annotations__, dog.__annotations__)
        self.assertIs(Dog.__doc__, dog.__doc__)
        self.assertIs(Dog.__name__, dog.__name__)

        # Basic checks for Person
        self.assertTrue(isinstance(Person, Observer))
        self.assertIs(Person.BaseClass, BaseObserver)
        self.assertTrue(isinstance(Person.observer, Person.BaseClass))
        self.assertTupleEqual(Person.observer.args, ())
        self.assertDictEqual(Person.observer.kwargs, {})
        self.assertTupleEqual(Person.observer.args, ())
        self.assertDictEqual(Person.observer.kwargs, {})
        self.assertListEqual(Person.methods, [])
        self.assertListEqual(Person.observables, [])
        self.assertIs(Person.substitute.callee, person)
        self.assertTupleEqual(Person.substitute.callee_args, ())
        self.assertDictEqual(Person.substitute.callee_kwargs, {})
        self.assertIs(Person.__annotations__, person.__annotations__)
        self.assertIs(Person.__doc__, person.__doc__)
        self.assertIs(Person.__name__, person.__name__)

        # Basic calls deliver function defaults
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_basics_nodecos_params(self):
        """Unittest: Observable & Observer - nodecos, params"""

        # Result list
        res = list()

        # Observable
        def dog(act1: str = "Brrr", act2: str = "!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act1}{act2}'")

        # Observer
        def person(say1: str = "Hello", say2: str = "?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say1}{say2}'")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Dog = Observable(dog, 'Woof,', act2='Woof!')
        Person = Observer(person, 'Ooops', say2='!')

        # Basic checks for Dog
        self.assertTrue(isinstance(Dog, Observable))
        self.assertIs(Dog.BaseClass, BaseObservable)
        self.assertTrue(isinstance(Dog.observable, Dog.BaseClass))
        self.assertTrue(hasattr(Dog.observable, 'register'))
        self.assertTrue(hasattr(Dog.observable, 'unregister'))
        self.assertTrue(hasattr(Dog.observable, 'dispatch'))
        self.assertTrue(hasattr(Dog.observable, 'observers'))
        self.assertTupleEqual(Dog.observable.args, ())
        self.assertDictEqual(Dog.observable.kwargs, {})
        self.assertIs(Dog.activate, Activation.AFTER)
        self.assertFalse(hasattr(Dog, 'decorator_args'))
        self.assertFalse(hasattr(Dog, 'decorator_kwargs'))
        self.assertListEqual(Dog.methods, [])
        self.assertIs(Dog.substitute.callee, dog)
        self.assertTupleEqual(Dog.substitute.callee_args, ('Woof,',))
        self.assertDictEqual(Dog.substitute.callee_kwargs, {'act2': 'Woof!'})
        self.assertIs(Dog.__annotations__, dog.__annotations__)
        self.assertIs(Dog.__doc__, dog.__doc__)
        self.assertIs(Dog.__name__, dog.__name__)

        # Basic checks for Person
        self.assertTrue(isinstance(Person, Observer))
        self.assertIs(Person.BaseClass, BaseObserver)
        self.assertTrue(isinstance(Person.observer, Person.BaseClass))
        self.assertTupleEqual(Person.observer.args, ())
        self.assertDictEqual(Person.observer.kwargs, {})
        self.assertFalse(hasattr(Person, 'decorator_args'))
        self.assertFalse(hasattr(Person, 'decorator_kwargs'))
        self.assertListEqual(Person.methods, [])
        self.assertListEqual(Person.observables, [])
        self.assertIs(Person.substitute.callee, person)
        self.assertTupleEqual(Person.substitute.callee_args, ('Ooops',))
        self.assertDictEqual(Person.substitute.callee_kwargs, {'say2': '!'})
        self.assertIs(Person.__annotations__, person.__annotations__)
        self.assertIs(Person.__doc__, person.__doc__)
        self.assertIs(Person.__name__, person.__name__)

        # Basic calls deliver decorator defaults
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Ooops!'"])
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Woof,Woof!'"])

    def test_basics_decos_noparams(self):
        """Unittest: Observable & Observer - decos, noparams"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Dog = Observable(None, 'deco_arg', kw='deco_kwarg')(dog)
        Person = Observer(None, 'deco_arg', kw='deco_kwarg')(person)

        # Basic checks for Dog
        self.assertTrue(isinstance(Dog, Observable))
        self.assertIs(Dog.BaseClass, BaseObservable)
        self.assertTrue(isinstance(Dog.observable, Dog.BaseClass))
        self.assertTrue(hasattr(Dog.observable, 'register'))
        self.assertTrue(hasattr(Dog.observable, 'unregister'))
        self.assertTrue(hasattr(Dog.observable, 'dispatch'))
        self.assertTrue(hasattr(Dog.observable, 'observers'))
        self.assertTupleEqual(Dog.observable.args, ('deco_arg',))
        self.assertDictEqual(Dog.observable.kwargs, {'kw': 'deco_kwarg'})
        self.assertIs(Dog.activate, Activation.AFTER)
        self.assertTupleEqual(Dog.decorator_args, ('deco_arg',))
        self.assertDictEqual(Dog.decorator_kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(Dog.methods, [])
        self.assertIs(Dog.substitute.callee, dog)
        self.assertTupleEqual(Dog.substitute.callee_args, ())
        self.assertDictEqual(Dog.substitute.callee_kwargs, {})
        self.assertIs(Dog.__annotations__, dog.__annotations__)
        self.assertIs(Dog.__doc__, dog.__doc__)
        self.assertIs(Dog.__name__, dog.__name__)

        # Basic checks for Person
        self.assertTrue(isinstance(Person, Observer))
        self.assertIs(Person.BaseClass, BaseObserver)
        self.assertTrue(isinstance(Person.observer, Person.BaseClass))
        self.assertTupleEqual(Person.observer.args, ('deco_arg',))
        self.assertDictEqual(Person.observer.kwargs, {'kw': 'deco_kwarg'})
        self.assertTupleEqual(Person.decorator_args, ('deco_arg',))
        self.assertDictEqual(Person.decorator_kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(Person.methods, [])
        self.assertListEqual(Person.observables, [])
        self.assertIs(Person.substitute.callee, person)
        self.assertTupleEqual(Person.substitute.callee_args, ())
        self.assertDictEqual(Person.substitute.callee_kwargs, {})
        self.assertIs(Person.__annotations__, person.__annotations__)
        self.assertIs(Person.__doc__, person.__doc__)
        self.assertIs(Person.__name__, person.__name__)

        # Basic calls deliver function defaults
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Hello?'"])
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

    def test_basics_decos_params(self):
        """Unittest: Observable & Observer - decos, params"""

        # Result list
        res = list()

        # Observable
        def dog(act1: str = "Brrr", act2: str = "!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act1}{act2}'")

        # Observer
        def person(say1: str = "Hello", say2: str = "?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say1}{say2}'")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Dog = Observable(None, 'deco_arg', kw='deco_kwarg')(
            dog, 'Woof,', act2='Woof!')
        Person = Observer(None, 'deco_arg', kw='deco_kwarg')(
            person, 'Ooops', say2='!')

        # Basic checks for Dog
        self.assertTrue(isinstance(Dog, Observable))
        self.assertIs(Dog.BaseClass, BaseObservable)
        self.assertTrue(isinstance(Dog.observable, Dog.BaseClass))
        self.assertTrue(hasattr(Dog.observable, 'register'))
        self.assertTrue(hasattr(Dog.observable, 'unregister'))
        self.assertTrue(hasattr(Dog.observable, 'dispatch'))
        self.assertTrue(hasattr(Dog.observable, 'observers'))
        self.assertTupleEqual(Dog.observable.args, ('deco_arg',))
        self.assertDictEqual(Dog.observable.kwargs, {'kw': 'deco_kwarg'})
        self.assertIs(Dog.activate, Activation.AFTER)
        self.assertTupleEqual(Dog.decorator_args, ('deco_arg',))
        self.assertDictEqual(Dog.decorator_kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(Dog.methods, [])
        self.assertIs(Dog.substitute.callee, dog)
        self.assertTupleEqual(Dog.substitute.callee_args, ('Woof,',))
        self.assertDictEqual(Dog.substitute.callee_kwargs, {'act2': 'Woof!'})
        self.assertIs(Dog.__annotations__, dog.__annotations__)
        self.assertIs(Dog.__doc__, dog.__doc__)
        self.assertIs(Dog.__name__, dog.__name__)

        # Basic checks for Person
        self.assertTrue(isinstance(Person, Observer))
        self.assertIs(Person.BaseClass, BaseObserver)
        self.assertTrue(isinstance(Person.observer, Person.BaseClass))
        self.assertTupleEqual(Person.observer.args, ('deco_arg',))
        self.assertDictEqual(Person.observer.kwargs, {'kw': 'deco_kwarg'})
        self.assertTupleEqual(Person.decorator_args, ('deco_arg',))
        self.assertDictEqual(Person.decorator_kwargs, {'kw': 'deco_kwarg'})
        self.assertListEqual(Person.methods, [])
        self.assertListEqual(Person.observables, [])
        self.assertIs(Person.substitute.callee, person)
        self.assertTupleEqual(Person.substitute.callee_args, ('Ooops',))
        self.assertDictEqual(Person.substitute.callee_kwargs, {'say2': '!'})
        self.assertIs(Person.__annotations__, person.__annotations__)
        self.assertIs(Person.__doc__, person.__doc__)
        self.assertIs(Person.__name__, person.__name__)

        # Basic calls deliver decorator defaults
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Ooops!'"])

        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Woof,Woof!'"])

    def test_basics_observable_activation(self):
        """Unittest: Observable & Observer - Activation"""

        # Result list
        res = list()

        # Observable
        def dog(act: str = "Brrr!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test
        self.assertEqual(len(Activation), 4)

        self.assertNotEqual(Activation.NONE, Activation.BEFORE)
        self.assertNotEqual(Activation.NONE, Activation.AFTER)
        self.assertNotEqual(Activation.NONE, Activation.BEFORE_AND_AFTER)
        self.assertNotEqual(Activation.BEFORE, Activation.AFTER)
        self.assertNotEqual(Activation.BEFORE, Activation.BEFORE_AND_AFTER)
        self.assertNotEqual(Activation.AFTER, Activation.BEFORE_AND_AFTER)

        self.assertEqual(Activation.BEFORE_AND_AFTER,
                         Activation.BEFORE | Activation.AFTER)

        # ---------------------------------------------------------------------
        # Decoration
        Dog = Observable(dog)
        Person = Observer(observables=Dog)(person)

        # Person says default
        res.clear()
        Person()
        self.assertListEqual(res, ["person says 'Hello?'"])

        # ---------------------------------------------------------------------

        # Default activation is AFTER
        self.assertIs(Dog.activate, Activation.AFTER)

        # Activation: NONE
        Dog.activate = Activation.NONE
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Brrr!'"])

        # Activation: BEFORE
        Dog.activate = Activation.BEFORE
        res.clear()
        Dog()
        self.assertListEqual(res, ["person says 'Hello?'",
                                   "dog acts 'Brrr!'"])

        # Activation: AFTER
        Dog.activate = Activation.AFTER
        res.clear()
        Dog()
        self.assertListEqual(res, ["dog acts 'Brrr!'",
                                   "person says 'Hello?'"])

        # Activation: BEFORE & AFTER
        Dog.activate = Activation.BEFORE_AND_AFTER
        res.clear()
        Dog()
        self.assertListEqual(res, ["person says 'Hello?'",
                                   "dog acts 'Brrr!'",
                                   "person says 'Hello?'"])

    def test_observable_functions(self):
        """Unittest: Observable & Observer - Functions"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        def dog(act: str = "Woof!") -> None:
            """A dog function"""
            res.append(f"{dog.__name__} acts '{act}'")

        # Observer
        def person(say: str = "Hello?") -> None:
            """A person function"""
            res.append(f"{person.__name__} says '{say}'")

        # ---------------------------------------------------------------------
        # Test scenario
        def test(Person, Dog):
            # Person registered as an observer of dog by decorations above
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Repeated registration override current registration
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Unregister person as an observer of dog
            Dog.observable.unregister(Person)
            self.assertDictEqual(Dog.observable.observers(classbased=True), {})
            self.assertDictEqual(Dog.observable.observers(), dict())

            # Re-register person as an observer of dog
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Unregister *all* observers of dog
            Dog.observable.unregister()
            self.assertDictEqual(Dog.observable.observers(classbased=True), {})
            self.assertDictEqual(Dog.observable.observers(), dict())

            # Re-register person as an observer of dog
            Dog.observable.register(Person)
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person)}))
            Dog.observable.register(Person, say="What's up?")
            self.assertTrue(cmp(Dog.observable.observers().values(),
                                {F(Person, say="What's up?")}))

            # Person say default
            res.clear()
            Person()
            self.assertListEqual(res, ["person says 'Hello?'"])

            # Person say customized text using positional parameter
            res.clear()
            Person("Where is my dog?")
            self.assertListEqual(res, ["person says 'Where is my dog?'"])

            # Person say customized text using keyword parameter
            res.clear()
            Person(say="Where is my dog?")
            self.assertListEqual(res, ["person says 'Where is my dog?'"])

            # Dog act default triggers person say decoration default
            res.clear()
            Dog()
            self.assertListEqual(res, ["dog acts 'Woof!'",
                                       "person says 'What's up?'"])

            # Dog act customized text triggers person say decoration default
            res.clear()
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            # Initiate additional customized dispatch
            res.clear()
            Dog("Brrr!")
            Dog.observable.dispatch(observer=Person, say="Quiet, please!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'",
                                       "person says 'Quiet, please!'"])

            # Switch notification off/on
            res.clear()
            Dog.activate = Activation.NONE
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'"])

            res.clear()
            Dog.activate = Activation.BEFORE
            Dog("Brrr!")
            self.assertListEqual(res, ["person says 'What's up?'",
                                       "dog acts 'Brrr!'"])

            res.clear()
            Dog.activate = Activation.AFTER
            Dog("Brrr!")
            self.assertListEqual(res, ["dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            res.clear()
            Dog.activate = Activation.BEFORE_AND_AFTER
            Dog("Brrr!")
            self.assertListEqual(res, ["person says 'What's up?'",
                                       "dog acts 'Brrr!'",
                                       "person says 'What's up?'"])

            Dog.activate = Activation.AFTER

        # ---------------------------------------------------------------------
        # Test: Decoration via Observer
        Dog = Observable(dog)
        Person = Observer(observables=X(Dog, say="What's up?"))(person)
        test(Person, Dog)

        # ---------------------------------------------------------------------
        # Test: Decoration via Observable
        Person = Observer(person)
        Dog = Observable(observers=F(Person, say="What's up?"))(dog)
        test(Person, Dog)

    def test_observable_class_init(self):
        """Unittest: Observable & Observer - class init"""

        # Result list
        res = list()

        # Observable
        class dog:
            """A Dog Type"""

            def __init__(self, name: str = "DOG"):
                self.name = name
                res.append(f"{self.name} acts 'INIT'")

            def untouched(self):
                """Untouched by decoration"""
                res.append(f"{self.name} is untouched")

        # Observer
        class person:
            """A Person Type"""

            def __init__(self, name: str = "PERSON"):
                self.name = name
                res.append(f"{self.name} says 'INIT'")

            def untouched(self):
                """Untouched by decoration"""
                res.append(f"{self.name} is untouched")

        # ---------------------------------------------------------------------
        # Test setup: Decoration
        Person = Observer(person)
        Dog = Observable(observers=Person)(dog)

        # Person registered as an observer of dog by decorations above
        self.assertDictEqual(Dog.observable.observers(),
                             {F(Person): F(Person)})

        # Init a Person
        res.clear()
        p = Person()
        self.assertListEqual(res, ["PERSON says 'INIT'"])

        # Init a Dog with Person as an observer
        res.clear()
        d = Dog()
        self.assertListEqual(res, ["DOG acts 'INIT'", "PERSON says 'INIT'"])

        # The untouchables
        res.clear()
        p.untouched()
        self.assertEqual(res, ['PERSON is untouched'])
        res.clear()
        d.untouched()
        self.assertEqual(res, ['DOG is untouched'])

    def test_observable_class_staticmethod01(self):
        """Unittest: Observable & Observer - static methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            @staticmethod
            def static_method(act: str = 'Woof!'):
                """To be decorated"""
                res.append(f"dog act '{act}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"dog is untouched")

        # Observer
        class person:
            """A Person Type"""

            @staticmethod
            def static_method(say: str = 'Hello?'):
                """To be decorated"""
                res.append(f"person say '{say}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"person is untouched")

        # ---------------------------------------------------------------------
        # Test: function decoration
        person.static_method = Observer(person.static_method)
        dog.static_method = Observable(
            observers=F(person.static_method, say="What's up?"))(
            dog.static_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(dog.static_method.observable.observers().values(),
                            {F(person.static_method, say="What's up?")}))

        # Person
        res.clear()
        person.static_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        dog.static_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])

        # The untouchables
        res.clear()
        person.static_untouched()
        self.assertEqual(res, ['person is untouched'])
        res.clear()
        dog.static_untouched()
        self.assertEqual(res, ['dog is untouched'])

    def test_observable_class_staticmethod02(self):
        """Unittest: Observable & Observer - static methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            @staticmethod
            def static_method(act: str = 'Woof!'):
                """To be decorated"""
                res.append(f"dog act '{act}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"dog is untouched")

        # Observer
        class person:
            """A Person Type"""

            @staticmethod
            def static_method(say: str = 'Hello?'):
                """To be decorated"""
                res.append(f"person say '{say}'")

            @staticmethod
            def static_untouched():
                """Untouched by decoration"""
                res.append(f"person is untouched")

        # ---------------------------------------------------------------------
        # Test: class decoration
        Person = Observer(methods=person.static_method)(person)
        Dog = Observable(observers=F(Person.static_method, say="What's up?"),
                         methods=dog.static_method)(dog)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.static_method.observable.observers().values(),
                            {F(Person.static_method, say="What's up?")}))

        # Person
        res.clear()
        Person.static_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.static_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])

        # The untouchables
        res.clear()
        person.static_untouched()
        self.assertEqual(res, ['person is untouched'])
        res.clear()
        dog.static_untouched()
        self.assertEqual(res, ['dog is untouched'])

    def test_observable_class_classmethod01(self):
        """Unittest: Observable & Observer - class methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            @classmethod
            def class_method(cls, act: str = 'Woof!'):
                """A classmethod"""
                res.append(f"{cls.__name__} act '{act}'")

        # Observer
        class person:
            """A Person Type"""

            @classmethod
            def class_method(cls, say: str = 'Hello?'):
                """A classmethod"""
                res.append(f"{cls.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: function decoration
        person.class_method = Observer(person.class_method)
        dog.class_method = Observable(
            observers=F(person.class_method, say="What's up?"))(
            dog.class_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(dog.class_method.observable.observers().values(),
                            {F(person.class_method, say="What's up?")}))

        # Person
        res.clear()
        person.class_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        dog.class_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])

    def test_observable_class_classmethod02(self):
        """Unittest: Observable & Observer - class methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            @classmethod
            def class_method(cls, act: str = 'Woof!'):
                """A classmethod"""
                res.append(f"{cls.__name__} act '{act}'")

        # Observer
        class person:
            """A Person Type"""

            @classmethod
            def class_method(cls, say: str = 'Hello?'):
                """A classmethod"""
                res.append(f"{cls.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: class decoration
        Person = Observer(methods=person.class_method)(person)
        Dog = Observable(observers=F(Person.class_method, say="What's up?"),
                         methods=dog.class_method)(dog)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.class_method.observable.observers().values(),
                            {F(Person.class_method, say="What's up?")}))

        # Person
        res.clear()
        Person.class_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.class_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])

    def test_observable_class_objectmethod01(self):
        """Unittest: Observable & Observer - object methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            def object_method(self, act: str = 'Woof!'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} act '{act}'")

        # Observer
        class person:
            """A Person Type"""

            def object_method(self, say: str = 'Hello?'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: function decoration
        Person = person()
        Dog = dog()

        Person.object_method = Observer(Person.object_method)
        Dog.object_method = Observable(
            observers=F(Person.object_method, say="What's up?"))(
            Dog.object_method)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.object_method.observable.observers().values(),
                            {F(Person.object_method, say="What's up?")}))

        # Person
        res.clear()
        Person.object_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.object_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])

    def test_observable_class_objectmethod02(self):
        """Unittest: Observable & Observer - object methods"""

        # Result list
        res = list()

        # Helper
        def cmp(iter1, iter2):
            """Compare *all* elements of F with a tuple"""
            if len(iter1) != len(iter2):
                return False
            else:
                iter1 = list(iter1)
                iter2 = list(iter2)
                iter1.sort()
                iter2.sort()
                for left, right in zip(iter1, iter2):
                    if left.callee != right.callee or \
                            left.callee_args != right.callee_args or \
                            left.callee_kwargs != right.callee_kwargs:
                        return False
                return True

        # Observable
        class dog:
            """A Dog Type"""

            def object_method(self, act: str = 'Woof!'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} act '{act}'")

        # Observer
        class person:
            """A Person Type"""

            def object_method(self, say: str = 'Hello?'):
                """An objectmethod"""
                res.append(f"{self.__class__.__name__} say '{say}'")

        # ---------------------------------------------------------------------
        # Test: object decoration
        Person = person()
        Dog = dog()

        Person = Observer(methods=X('object_method'))(Person)
        Dog = Observable(observers=F(Person.object_method, say="What's up?"),
                         methods=F('object_method'))(Dog)

        # Person registered as an observer of dog by decorations above
        self.assertTrue(cmp(Dog.object_method.observable.observers().values(),
                            {F(Person.object_method, say="What's up?")}))

        # Person
        res.clear()
        Person.object_method()
        self.assertListEqual(res, ["person say 'Hello?'"])

        # Dog with Person as an observer
        res.clear()
        Dog.object_method()
        self.assertListEqual(res, ["dog act 'Woof!'",
                                   "person say 'What's up?'"])


# -----------------------------------------------------------------------------
# Execution
if __name__ == "__main__":
    unittest.main()
