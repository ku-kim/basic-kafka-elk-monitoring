import random
from faker import Faker
from kafka import KafkaProducer
import json
import time

fake = Faker()


def get_fake_registered_data():
  return {
    'event_type': '회원가입',
    'user_uuid': fake.uuid4(),
    'user_id': fake.random_int(min=1, max=1000, step=1),
    'grade': fake.random_int(min=0, max=5),
    'first_name': fake.first_name(),
    'last_name': fake.last_name(),
    'email': fake.email(),
    'country': fake.country(),
  }


def get_fake_read_product_data():
  return {
    'event_type': '상품 조회',
    'user_id': fake.random_int(min=1, max=100),
    'product_id': fake.random_int(min=0, max=100),
  }


def get_fake_order_data():
  return {
    'event_type': '주문 성공',
    'user_id': fake.random_int(min=1, max=100),
    'grade': fake.random_int(min=0, max=5),
    'order_id': fake.random_int(min=1, max=10000),
    'product_id': fake.random_int(min=1, max=100),
    'count': fake.random_int(min=1, max=100),
    'price': fake.random_int(min=1000, max=500000, step=1000),
  }


def get_fake_cancel_order_data():
  return {
    'event_type': '주문 취소',
    'user_id': fake.random_int(min=1, max=100),
    'order_id': fake.random_int(min=1, max=10000),
  }


def get_fake_basket_data():
  return {
    'event_type': '장바구니 담기 성공',
    'user_id': fake.random_int(min=1, max=100),
    'product_id': fake.random_int(min=1, max=100),
  }


def get_fake_failed_basket_data():
  return {
    'event_type': '장바구니 담기 실패',
    'user_id': fake.random_int(min=1, max=100),
    'product_id': fake.random_int(min=1, max=100),
  }


def json_serializer(data):
  return json.dumps(data).encode("utf-8")


producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],
                         value_serializer=json_serializer)

if __name__ == "__main__":
  while 1 == 1:
    if (random.choice([True, False])): # 50%
      print("회원가입 이벤트 발생")
      fake_registered = get_fake_registered_data()
      print(fake_registered)
      producer.send('registered_event', fake_registered)

    if (random.random() >= 0.1): # 90%
      print("상품 조회 이벤트 발생")
      fake_read_product = get_fake_read_product_data()
      print(fake_read_product)
      producer.send('read_product_event', fake_read_product)

    if (random.random() >= 0.2): # 80%
      print("주문 성공 이벤트 발생")
      fake_order = get_fake_order_data()
      print(fake_order)
      producer.send('order_event', fake_order)

    if (random.random() >= 0.3): # 70%
      print("주문 취소 이벤트 발생")
      fake_cancel_order = get_fake_cancel_order_data()
      print(fake_cancel_order)
      producer.send('cancel_order', fake_cancel_order)

    if (random.random() >= 0.1): # 90%
      print("장바구니 담기 성공 이벤트 발생")
      fake_basket = get_fake_basket_data()
      print(fake_basket)
      producer.send('basket_event', fake_basket)

    if (random.random() >= 0.7): # 30%
      print("장바구니 담기 실패 이벤트 발생")
      fake_failed_basket = get_fake_failed_basket_data()
      print(fake_failed_basket)
      producer.send('failed_basket_event', fake_failed_basket)

    print("=============================\n")
    time.sleep(1)
