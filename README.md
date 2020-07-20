# AUth Service for Linux Machines Backend
Это репозиторий с кодом бекенд сервиса, который предоставляет механизм управления авторизациями пользователей на удалённых машинах.
В его задачи входит:

*   Хранить публичные ключи пользователей
*   Предоставять API для автоматизации процесса выдачи доступов
*   Непосредственно ходить на виртуальные машины, создавать там пользователей и разностить ключи


Вся информация о проекте доступна на gh-pages по [ссылке](https://auslm.github.io/)


## ToDo:
- [ ] Сделать взятие имени и фамилии из AD
- [ ] Логика по бану/разбану пользователей, самоудалению и удалению пользователей
- [ ] Для всей логики на получение списком и словарей прикрутить возможность забирать данные порциями
- [ ] Добавить логи в консоль и логи в бд
- [ ] Перенести логику веб-терминала
- [ ] Кодстайл поправить
- [ ] Ручка подтверждения
- [ ] Логика множественной выдачи и отбора доступов
- [ ] JS на кнопки удаления, отзывов и т.д. в таблицах
- [ ] измененный JS на формы доабвлений и удалений на страницах с таблицами для обновления таблиц (и собственно ручки для рендера таблиц на сервере)
- [ ] переработать названия
- [ ] добить переработку JS и допеределать сабмит кнопки
