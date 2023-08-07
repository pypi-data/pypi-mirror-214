#  Zenlayer.com Inc.
#  Copyright (c) 2014-2023 All Rights Reserved.
import unittest

from zenlayercloud.common.abstract_model import AbstractModel


class MyTestCase(unittest.TestCase):

    def test_something(self):
        p2 = Person("hell", age=None, hobbies=["hobby"])
        print(p2._serialize(allow_none=True))


if __name__ == '__main__':
    unittest.main()


class Person(AbstractModel):

    def __init__(self, name: str, age: int, hobbies: list):
        self.name = name
        self.age = age
        self.hobbies = hobbies


class Person2(object):

    def __init__(self, name: str, age: int, hobbies: list):
        self.name = name
        self.age = age
        self.hobbies = hobbies
