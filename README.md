# Прототип генератора инстраструктуры распределенных приложений
Прототип позволяет автоматически создавать dockerfile и контейнеры docker для ваших микросервисов. Также прототип реализует автоматическое описание инфраструктуры для вашего приложения, а именно: конфигурацию брокера сообщений Apache Kafka, окружения для каждого из микросервисов, создание узлов с базами данных, связи с микросервисов с вашими базами. Описание реализуется для запуска в Docker Compose, соответсвенно, выходным является файл docker-compose.yml. На вход подается файл в формате json с описанием предметной области. Более подробные требования к нему в разделе "Требования к файлу с семантическими данными".

Прототип поддерживает работу в двух режимах:
1. локальный режим;
2. серверный режим.

### Локальный режим
Локальный режим позволяет как просто генерировать dockerfile для каждого Node и docker-compose.yml с предварительной
проверкой входных данных (файла с семантическими данными предметной области и директорией, содержащей исходный код), так и генерировать
docker образы или же полностью запускать приложение в полученной инфраструктуре.
Для запуска в локальном режиме необходимо запустить инструкцию:

*python app.py -sc <путь> -sd <путь> -ci [optional] -run [optional]*

для запуска передаются следующие параметры:
- *-sc <путь>* - директория с исходным кодом проекта, для которого генерируется инфраструктура;
- *-ci <путь>* - директория, содержащая файл с семантическими данными semantic_data.json, либо путь к этому файлу;
- *-ci* - необязательный параметр - флаг генерации docker-images для каждого Node;
- *-run* - необязательный параметр - флаг запуска сгенерированного docker-compose.yml. Автоматически генерирует также docker-images.

### Серверный режим
Серверный режим позволяет с использованием REST API отправлять семантические данные о предметной области и получать в ответ 
dockerfile для каждого Node или же docker-compose.yml файл для всей системы.
Для запуска в серверном режиме необходимо собрать образ командой из корня проекта: 

*docker build --tag <имя образа> .*

После сборки образа необходимо запустить командой:

*docker run <имя образа> -p <порт вашей машины>:5001*

Далее можно обратиться к полученному сервису по двум эндпоинтам:

- **POST http://<адрес_хоста>:<порт_хоста>/dockerfiles**

В теле запроса необходимо прислать семантические данные предметной области в формате json. 
В ответ сервер вернет json файл со списком Nodes в формате:

```
[
    {
        'name': 'имя узла 1',
        'dockerfile': 'строка, содержащая значение dockerfile узла 1'
    }, 
    ...
]
```

- **POST http://<адрес_хоста>:<порт_хоста>/docker-compose**

В теле запроса необходимо прислать семантические данные предметной области в формате json. 
В ответ сервер вернет json файл с docker-compose файлом в формате:
```
[
    {
        'docker-compose': 'строка, содержащая значение docker-compose файла'
    }
]
```

### Требования к файлу с семантическими данными 

Файл с семантическими данными (описанием предметной области) должен иметь название semantic_data и иметь расширение .json. Таким образом, ограничения, принятые для формата json, являются ограничениями для файла с семантическими данными. 

Корневая структура json должна содержать в себе ключи для 4х списков сущностей (если указанный тип сущностей имеется в системе): 
- «clients» - содержит список клиентских сервисов; 
- «gateways» - содержит список шлюзов;
- «services» - содержит список микросервисов;
- «databases» - содержит список баз данных.

Clients содержит в себе 3 поля:
- «name» - string – наименование клиентского сервиса;
- «language» - string – наименование языка программирования, на котором реализован клиентский сервис;
- «connects» - string – наименование шлюза, к которому подключен клиентский сервис. Важно, что указываются только один шлюз из списка «gateways». Наименование базы данных, другого клиентского сервиса или микросервиса не могут быть указаны в данном списке.

Gateways содержит в себе 3 поля:
- «name» - string – наименование шлюза;
- «language» - string – наименование языка программирования, на котором реализован шлюз;
- «connects» - list<string> – список наименований микросервисов, с которыми обменивается данными шлюз. Важно, что указываются только микросервисы из списка «services». Базы данных и клиентские сервисы не могут быть указаны в данном списке.

Services содержит в себе 3 поля:
- «name» - string – наименование микросервиса;
- «language» - string – наименование языка программирования, на котором реализован микросервис;
- «connects» - list<string> – список наименований шлюзов, с которыми обменивается данными микросервис. Важно, что указываются только шлюзы из списка «gateways». Базы данных и клиентские сервисы не могут быть указаны в данном списке.

Databases содержит в себе 3 поля:
- «name» - string – наименование базы данных;
- «dbtype» - string – наименование типа СУБД;
- «connects» - list<string> – список наименований микросервисов, которые подключены к базе данных. Важно, что указываются только сервисы из списка «services». Клиентские сервисы, шлюзы и другие базы данных не могут быть указаны в данном списке.

Пример файла semantic_data.json представлен в листинге ниже:
```
{
  "clients": [
    {
      "name": "frontend",
      "language": "js_react",
      "connects": "apigateway"
    }
  ],
  "gateways": [
    {
      "name": "apigateway",
      "language": "python",
      "connects":[]
    }
  ],
  "services": [
    {
      "name": "backend_microservice",
      "language": "python",
      "connects":["apigateway"]
    }
  ],
  "databases": [
    {
      "name": "database1",
      "dbtype": "mongodb",
      "connects": ["backend_microservice"]
    }
  ]
```
В случае, если у Вас возникнут вопросы по разработке, буду рад ответить на них в телеграм https://t.me/yala_by 📱
