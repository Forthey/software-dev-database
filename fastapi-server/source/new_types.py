import enum


class SpecializationCode(enum.IntEnum):
    developer = 0
    tester = 1


spec_code_str = {
    SpecializationCode.developer: "Разработчик",
    SpecializationCode.tester: "Тестировщик"
}


class Level(enum.IntEnum):
    intern = 0
    junior = 1
    middle = 2
    senior = 3


level_str = {
    Level.intern: "Стажер",
    Level.junior: "Junior",
    Level.middle: "Middle",
    Level.senior: "Senior"
}


class BlockStatus(enum.IntEnum):
    in_progress = 0
    on_testing = 1
    completed = 3


block_status_str = {
    BlockStatus.in_progress: "В разработке",
    BlockStatus.on_testing: "На тестировании",
    BlockStatus.completed: "Завершен"
}


class BugCategory(enum.IntEnum):
    minor = 0
    serious = 1
    showstopper = 2


bug_category_str = {
    BugCategory.minor: "Незначительный",
    BugCategory.serious: "Серьезный",
    BugCategory.showstopper: "ShowStopper"
}
