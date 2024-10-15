import pika
import time

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

# Создание очереди с названием KBO-25-21_Shillo_fanout
queue_name = 'IKBO-25-21_Shillo_fanout'
channel.queue_declare(queue=queue_name, durable=True)

# Связывание очереди с обменником
channel.queue_bind(exchange=exchange_name, queue=queue_name)

# Обработка сообщений с задержкой, зависящей от количества символов #
def process_message(ch, method, properties, body):
    message = body.decode()
    sleep_time = message.count('#')
    print(f"Получено сообщение: {message}. Сон на {sleep_time} секунд.")
    time.sleep(sleep_time)
    print("Задача выполнена.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Потребление сообщений
channel.basic_qos(prefetch_count=1)  # Гарантирует, что только одно сообщение будет отправлено потребителю за раз
channel.basic_consume(queue=queue_name, on_message_callback=process_message)

print(f"Ожидание сообщений из очереди: {queue_name}")
channel.start_consuming()
