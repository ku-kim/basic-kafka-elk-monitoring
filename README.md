- [소개](#소개)
- [아키텍처](#아키텍처)
  - [기본 형태](#기본-형태)
  - [Kafka + ELK Stack](#kafka--elk-stack)
- [1. Requirements](#1-requirements)
  - [1.1 install docker & docker compose](#11-install-docker--docker-compose)
  - [1.2 install python3 & packages(kafka-python, json, faker)](#12-install-python3--packageskafka-python-json-faker)
- [2. Usage](#2-usage)
  - [2.1 docker compose up](#21-docker-compose-up)
  - [2.2 run producer](#22-run-producer)
  - [2.3 kibana index pattern 추가 & elasticsearch life cycle 수정](#23-kibana-index-pattern-추가--elasticsearch-life-cycle-수정)
  - [2.4 kafka manager에서 토픽 리스트 확인](#24-kafka-manager에서-토픽-리스트-확인)
  - [2.5 clean up](#25-clean-up)
- [3. 결과](#3-결과)
  - [3.1 kibana 전체 데이터 조회](#31-kibana-전체-데이터-조회)
  - [3.2 특정 검색](#32-특정-검색)



# 소개
이 저장소는 Kafka에 저장된 이벤트를 ELK Stack를 활용하여 실시간 모니터링 예제 입니다. 

- docker-compose를 활용하여 kafka, elk stack를 구축합니다.
- kafka에 dummy event를 생성하는 producer는 python 스크립트로 대체합니다. ([event는 총 6개](https://github.com/ku-kim/basic-kafka-elk-monitoring/pull/8))

# 아키텍처

## 기본 형태

<img width="1100" alt="image" src="https://user-images.githubusercontent.com/57086195/201714941-c7dea6d7-9815-4e02-b56f-bade9127ead3.png">

## Kafka + ELK Stack
<img width="1175" alt="image" src="https://user-images.githubusercontent.com/57086195/201715864-6e73488a-f000-47b8-be2b-589dfc61a30c.png">


# 1. Requirements

## 1.1 install docker & docker compose
- 도커, 도커 컴포즈 설치는 생략합니다.
- 🔥 도커 메모리가 부족하여 137 error가 발생한 경우 메모리를 올려주세요.

기본으로 사용되는 포트는 아래와 같습니다.
- elasticsearch : 9200
- kibana : 5601
- logstash : 9600 / 7777
- zookeeper : 2181
- kafka : 9092
- kafka_manager : 9000

## 1.2 install python3 & packages(kafka-python, json, faker)

- python3 설치는 생략합니다.

```bash
# install python packages
pip3 install json
pip3 install kafka-python
pip3 install Faker
```

# 2. Usage

## 2.1 docker compose up
- router ip 수정
```bash
# docker-compose의 kafaka 이미지 환경 변수를 본인의 router ip로 변경합니다.
  kafka:
    image: wurstmeister/kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: 10.44.8.36 #[Personal IP] 

vim /container-kafka-elk/kafka-elk.yml
```


- 도커 컴포즈 실행

```bash
docker-compose -f ./container-kafka-elk/kafka-elk.yml up
```

[![docker-compose-up](https://asciinema.org/a/537482.svg)](https://asciinema.org/a/537482)

위 녹화는 중간에 멈췄지만 1분 정도 기다리면 모든 컨테이너가 정상적으로 실행되고 kafaka_manager가 아래의 log를 출력합니다.

![결과](https://i.imgur.com/FNatAJN.png)


## 2.2 run producer
- dummy event 생성할 프로듀서 실행
```bash
python3 ./producer/producer.py
```

[![producer_py](https://asciinema.org/a/537485.svg)](https://asciinema.org/a/537485)

## 2.3 kibana index pattern 추가 & elasticsearch life cycle 수정
- [setup kibana](https://github.com/ku-kim/basic-kafka-elk-monitoring/issues/10#issuecomment-1313377947)

## 2.4 kafka manager에서 토픽 리스트 확인

- [setup kafka manager](https://github.com/ku-kim/basic-kafka-elk-monitoring/issues/10#issuecomment-1313382496)


## 2.5 clean up

```bash
docker kill $(docker ps -q) # 실행된 모든 도커 프로세스 종료
docker volume ls # 도커 볼륨 조회
docker volume rm <volume name> 
```

[![docker volume rm](https://asciinema.org/a/537490.svg)](https://asciinema.org/a/537490)

# 3. 결과

## 3.1 kibana 전체 데이터 조회
<img width="1536" alt="image" src="https://user-images.githubusercontent.com/57086195/201626172-1efd9c6b-42b1-4d9d-ab2a-febf243a4bc6.png">

## 3.2 특정 검색
- 실시간 모니터링 : 최근 10분간 회원 등급이 3이면서 상품 번호 1~30번 을 주문한 사람 수

![order](https://user-images.githubusercontent.com/57086195/201631598-e5250c94-92d9-4c6c-9d8f-676668606264.png)

---

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fku-kim%2Fbasic-kafka-elk-monitoring&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)