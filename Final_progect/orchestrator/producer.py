from kafka import KafkaProducer

producer = KafkaProducer(
        bootstrap_servers=['rc1d-055jdnvv92da9uun.mdb.yandexcloud.net:9091'],
        security_protocol="SASL_SSL",
        sasl_mechanism="SCRAM-SHA-512",
        sasl_plain_username='kafka_user361',
        sasl_plain_password='AT5APRfviHxsUF8',
        ssl_cafile=r"C:\Users\zarocool\.kafka\YandexInternalRootCA.crt")

try:
    message = 'hello world'.encode('utf-8')
    producer.send("tg_send", message)
    producer.flush()
    print("Message sent to Kafka successfully.")
except Exception as e:
    print("Error while sending message to Kafka:", e)
finally:
    producer.close()

# from confluent_kafka import Producer
#
# def error_callback(err):
#     print('Something went wrong: {}'.format(err))
#
# params = {
#     'bootstrap.servers': 'rc1d-055jdnvv92da9uun.mdb.yandexcloud.net:9091',
#     'security.protocol': 'SASL_SSL',
#     'ssl.ca.location': r"C:\Users\zarocool\.kafka\YandexInternalRootCA.crt",
#     'sasl.mechanism': 'SCRAM-SHA-512',
#     'sasl.username': 'kafka_user361',
#     'sasl.password': 'AT5APRfviHxsUF8',
#     'error_cb': error_callback,
# }
#
# p = Producer(params)
# p.produce('tg_send', 'hello 4')
# p.flush(10)