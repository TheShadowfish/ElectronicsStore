**Задание**

В данном задании вам предлагается разработать онлайн платформу-торговой сети электроники

**Общая информация**

Тестовое задание состоит из нескольких задач. Мы примем вашу кандидатуру к рассмотрению только в том случае, если работа выполнена целиком. Попытайтесь продемонстрировать ваш уровень опыта и навыков в каждой задаче, чтобы мы смогли в полной мере оценить вашу кандидатуру.
Вы должны отправить ваше готовое приложение в виде ссылки на GitHub- или GitLab-репозиторий. **(+)**

Если вы пришлете приложение в любом другом виде (в виде ссылки на zip-архив, прикрепите zip-архив к письму и др.), ваша кандидатура не будет нами рассмотрена!
Если вы сделали не все пункты тестового задания — пожалуйста, укажите причину, по которой вы их не выполнили (не хватило времени, не хватило опыта/знаний, что-то еще).

**Технические требования** **(+)**
- Python 3.8+ (+)
- Django 3+ (+)
- DRF 3.10+ (+)
- PostgreSQL 10+ (+)
При выполнении тестового задания вы можете дополнительно использовать любые сторонние Python-библиотеки без всяких ограничений.

**Задание**

Создайте веб-приложение с API-интерфейсом и админ-панелью.

Создайте базу данных, используя миграции Django.


**Требования к реализации:**

Необходимо реализовать модель сети по продаже электроники.
Сеть должна представлять собой иерархическую структуру из трех уровней:

- завод;
- розничная сеть;
- индивидуальный предприниматель.

Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии). Важно отметить, что уровень иерархии определяется не названием звена, а отношением к остальным элементам сети, т. е. завод всегда находится на уровне 0, а если розничная сеть относится напрямую к заводу, минуя остальные звенья, ее уровень — 1.

**Вытекающие из этого условия**

- завод ни на кого не ссылается, сам всё производит.
- не позволить никому ссылаться на себя, это тупо и любой тестировщик полезет такое проверять
- уровень определяется количеством посредников (извращения с бесконечной перепродажей продукта допускаются (ИРЛ же есть такое)), следовательно, может быть выше трех. Но в целом рассчитываем на 3 уровня.


**Каждое звено сети должно обладать следующими элементами:** (реализовано, +)
- Название.
- Контакты:
- email,
- страна,
- город,
- улица,
- номер дома.
- Продукты:
- название,
- модель,
- дата выхода продукта на рынок.
- Поставщик (предыдущий по иерархии объект сети). (реализовано, +)
- Задолженность перед поставщиком в денежном выражении с точностью до копеек. (реализовано, +)
- Время создания (заполняется автоматически при создании). (реализовано, +)

**Сделать вывод в админ-панели созданных объектов.**

На странице объекта сети добавить:
- ссылку на «Поставщика»;
- фильтр по названию города; (реализовано, +)
- admin action, очищающий задолженность перед поставщиком у выбранных объектов. (реализовано, +)


**Используя DRF, создать набор представлений:**

- CRUD для модели поставщика (запретить обновление через API поля «Задолженность перед поставщиком»).
- Добавить возможность фильтрации объектов по определенной стране.
- Настроить права доступа к API так, чтобы только активные сотрудники имели доступ к API.