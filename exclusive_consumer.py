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

# Создание эксклюзивной очереди
queue_name = 'IKBO-25-21_Shillo_exclusive'
channel.queue_declare(queue=queue_name, exclusive=True)

# Обработка сообщений
def callback(ch, method, properties, body):
    print(f"Получено сообщение: {body.decode()}")

# Подписка на очередь и ожидание сообщений
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(f"Ожидание сообщений из очереди: {queue_name}")
channel.start_consuming()
