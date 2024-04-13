import enum


class SpecializationCode(enum.IntEnum):
    developer = 0
    tester = 1


class Level(enum.IntEnum):
    intern = 0
    junior = 1
    middle = 2
    senior = 3


class BugCategory(enum.IntEnum):
    minor = 0
    serious = 1
    showstopper = 2


class ResultInfo(enum.IntEnum):
    success = 0
    failure = 1
