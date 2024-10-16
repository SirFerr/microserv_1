import pika
import time
import threading

# Параметры подключения к RabbitMQ
host = '51.250.26.59'
port = 5672
login = 'guest'
password = 'guest123'

# Настройка соединения
credentials = pika.PlainCredentials(login, password)

# Объявление обменника типа fanout и очередей
def setup_channel(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', credentials))
    channel = connection.channel()
    exchange_name = 'logs_fanout'

    # Объявление обменника
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)

    # Создание очереди
    channel.queue_declare(queue=queue_name, durable=True)

    # Связывание очереди с обменником
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    return connection, channel


# Обработка сообщений с задержкой, зависящей от количества символов #
def process_message(ch, method, properties, body):
    message = body.decode()
    sleep_time = message.count('#')
    print(f"Получено сообщение: {message}. Сон на {sleep_time} секунд.")
    time.sleep(sleep_time)
    print("Задача выполнена.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Настройка обработки сообщений в отдельной очереди
def start_consuming(queue_name):
    connection, channel = setup_channel(queue_name)

    # Потребление сообщений
    channel.basic_qos(prefetch_count=1)  # Гарантирует, что только одно сообщение будет отправлено потребителю за раз
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)

    print(f"Ожидание сообщений из очереди: {queue_name}")
    channel.start_consuming()

# Запуск двух потоков для каждой очереди
if __name__ == '__main__':
    queue1 = 'IKBO-25-21_Shillo_fanout_1'
    queue2 = 'IKBO-25-21_Shillo_fanout_2'

    thread1 = threading.Thread(target=start_consuming, args=(queue1,))
    thread2 = threading.Thread(target=start_consuming, args=(queue2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
