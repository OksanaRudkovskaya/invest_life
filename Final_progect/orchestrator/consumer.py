from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'tg_send',
    bootstrap_servers='rc1d-055jdnvv92da9uun.mdb.yandexcloud.net:9091',
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username='kafka_consumer361',
    sasl_plain_password='2ZZ6RPH8nNvNDFj',
    ssl_cafile=r"C:\Users\zarocool\.kafka\YandexInternalRootCA.crt")

print("ready")

for msg in consumer:
    print(msg.key, msg.value)

# from confluent_kafka import Consumer
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
#     'group.id': 'ajel0683okcsvnrjbp5f',
#     'auto.offset.reset': 'earliest',
#     'enable.auto.commit': False,
#     'error_cb': error_callback,
#     'debug': 'all',
# }
# c = Consumer(params)
# c.subscribe(['tg_send'])
# while True:
#     msg = c.poll(timeout=3.0)
#     if msg:
#         val = msg.value().decode()
#         print(val)
