import pika
import sys

# Параметры подключения к RabbitMQ
host = '51.250.26.59'
port = 5672
login = 'guest'
password = 'guest123'

# Настройка соединения
credentials = pika.PlainCredentials(login, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', credentials))
channel = connection.channel()

# Объявление обменника типа fanout
exchange_name = 'logs_fanout'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)

# Сообщение и количество символов #, передаваемое в виде аргумента
message = sys.argv[1] if len(sys.argv) > 1 else '###'
channel.basic_publish(
    exchange=exchange_name,
    routing_key='',  # Для fanout routing_key не используется
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2  # Делает сообщение устойчивым (persistent)
    )
)
print(f"Отправлено сообщение: {message}")

# Закрытие соединения
connection.close()
