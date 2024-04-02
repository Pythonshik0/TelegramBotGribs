# TelegramBotGribs
Асинхронный телеграм бот на aiogram 2.2, sqllite 3. В боте присутствует личный кабинет админа с командами, которые представлены ниже


**Возможности админа**
## 1. Изменение заказа
Для того, чтобы войти в админскую панель, после команды ```/start``` нажмите на кнопку
"Выйти"

У вас будет доступны команды:

```/add_product - Не пишите её если не хотите добавлять товар (Команда добавляет товар в базу данных)```

```/edit_product - Это командой можно изменить данные любого товара по его названию```

```/del_product - Данной командой можно удалить любой товар из базы данных```

После того, как вы закончили работу в админской панели, нужно нажать на кнопку "Выйти" и написать команду ```/start```

## 2. Подтверждение заказа
Для того, чтобы подтвердить заказ, вам нужно перейти на самую главную страницу и нажать "Выйти"

Далее у вас должно быть уведомление о том, что какой либо человек оплатил заказ:
Пример:

Почта России
Оплатил Тинькофф
9650 Рублей
Заказ принят от пользователя 2064781562
1) Рапэ Пау перейра 5 шт
Цена: 9000💵Вес: 5 грамм⚖️
2) Шиитаке 1 шт**
Цена: 400💵Вес: 100 грамм⚖️

От клиента @IskanderMinsafinRR

Данные клиента для доставки: xxxxxxxxxxxx

Вам нужно взять его номер (он копируется легко при нажатии) 2064781562 и написать команду /checking 
Далее ввести его номер и если вы подтверждаете то Yes если не подтверждаете, то No
Пример: 2064781562 Yes
Пример: 2064781562 No

## 3. Удаление заказа

```/del_product ->> выйдите на главное меню и введите команду```
Далее введите наименование товара, который хотите удалить из базы данных


