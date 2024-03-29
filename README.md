## Компания по разработке ПО
Требуется создать схему реляционной БД согласно требованиями, реализовать эту схему в одной из известных СУБД и организовать взаимодействие с БД с помощью выбранного интерфейса с поддержкой требуемых действий

## Требования к работе и структуре БД
Список текущих разработок компании. \
Список разработчиков, список тестеров (тестеры находят ошибки, разработчики, допустившие ошибки, их исправляют) – каждый может участвовать не более, чем в двух проектах. \
У проекта есть план – набор блоков кода, приписанные к блокам разработчики, время старта каждого блока, дедлайн сдачи готового (протестированного и исправленного) блока. \
Разработчики передают тестерам блоки (есть дата передачи и имя тестера). Время на тестирование – не более 10% от времени написания блока. Время на исправление ошибки – 1 день. Время написания блока + время тестирования + время исправления должно вписаться до дедлайна сдачи блока. Багов в блоке может не быть. \
По каждому проекту – список багов (обязательные поля: категория, кто заметил, когда, кто будет исправлять, срок для исправления, фактическое исправление). \
\
Требуется поддержка:
- Приема на работу;
-	Перевода в новый проект;
-	Завершения проекта;
-	Планирования и старта нового проекта;
-	Отслеживания текущего состояния проекта (по всем блокам проекта);
-	Увольнения разработчика или тестера за N просрочек (по его вине) дедлайнов блоков в рамках проекта с генерацией письма «товарищу» об этом 
-	Отчеты: 
    - Список текущих разработок компании с указанием занятых в проекте; 
    - Список персонала, с указанием истории каждого (в каких проектах участвовал, упоряд. по времени старта проектов); 
    - Качество разработки – диаграмма по завершенным проектам со следующим показателем – (общее количество багов)/(продолжительность проекта в человеко-днях)
