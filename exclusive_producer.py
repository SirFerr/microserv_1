import pika

# Параметры подключения к RabbitMQ
host = '51.250.26.59'
port = 5672
login = 'guest'
password = 'guest123'

# Настройка соединения
credentials = pika.PlainCredentials(login, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', credentials))
channel = connection.channel()

# Название очереди (но не создаём её здесь)
queue_name = 'IKBO-25-21_Shillo_exclusive'

# Отправка сообщения в очередь
channel.basic_publish(exchange='', routing_key=queue_name, body='Привет, это тестовое сообщение!')
print(f"Сообщение отправлено в очередь: {queue_name}")

# Закрытие соединения
connection.close()
