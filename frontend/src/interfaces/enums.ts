export enum SpecializationCode {
    developer = 0,
    tester = 1
}
export const specCodeToStr = ["Разработчик", "Тестировщик"]


export enum Level {
    intern = 0,
    junior = 1,
    middle = 2,
    senior = 3
}
export const levelToStr = ["Стажер", "Junior", "Middle", "Senior"]


export enum BlockStatus {
    in_progress = 0,
    on_testing = 1,
    completed = 3
}
export const blockStatusToStr = ["У разработчика", "На тестировании", "", "Закрыт/Завершен"]


export enum BugCategory {
    minor = 0,
    serious = 1,
    showstopper = 2
}
export const bugCategoryToStr = ["Незначительный", "Серьезный", "ShowStopper"]
