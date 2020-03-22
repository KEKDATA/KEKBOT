BOT

Структура файлов:

1. bonus.7z - содержит документы с концептом анализа сети
2. bot.py - исполняемый файл
3. bot_answer.py - отправляет SPARQL запросы и по их результатам формирует ответы для бота
4. bot_answer_templates.py - содержит шаблоны ответов
5. config.py - содержит параметры бота
6. queries.py - содержит SPARQL запросы
7. validator.py - сщдержит валидаторы для ИНН и ОГРН

Оставьные файлы на данный момент не задействованы.



Функционал бота:

1. Найти ЮЛ по ОГРН
2. Найти ЮЛ по ИНН
3. Найти ЮЛ по названию
4. Найти ЮЛ по учередителю

В первых трех случаях возвращает инфу о ЮЛ (название, сокращенное название, ИНН, ОГРН, адрес) + список учередителей + список лиц, имеющих право без доверенности действовать от имени ЮЛ.

В четвертом случае возвращает инфу о человеке(имя, ИНН) +
список компаний, в которых он является учередителем

Команда:
	
	Сошкин Андрей 
		github.com/s-andrew
		vk.com/id138238035

	Калита Андрей 
		github.com/2la

	Страхов Марк 
		github.com/xevolesi
		vk.com/id233593984
		
	Слинкин Петр
		github.com/sinptr
		vk.com/s.p_13
		
	Крохмаль Даниил 
		github.com/TchernyavskyDaniil
		vk.com/id40371882
