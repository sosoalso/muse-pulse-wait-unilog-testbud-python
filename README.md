# PULSE 동작, wait 동작, 다국어 로그 테스트

## PULSE
pulse 는 데코레이터로 클래스 호출해서 쓰레드 하나 열어서 돌리기..

```python
def relay_on():
    relay.state = True

def relay_off():
    relay.state = False

@pulse(1.0, relay_off)  # 1초 후에 relay_off를 호출
def pulse_relay():
    uni_log_info("릴레이 펄스")
    relay_on()

def button_watcher_pulse_relay(e):
    if e.value:
        pulse_relay()

tp.port[1].button[1].watch(button_watcher_pulse_relay)


```


## WAIT
실행, 중단, 중복 방지만 구현함..
wait 은 파이썬 내장 스케쥴러 라이브러리 sched 에서 heap 이랑 named tuple 사용하는 부분만
list 랑 dict 로 바꿔서 간편? 하게 사용
왜냐면 뮤즈에 heap 이랑 복잡한게 없다.. 으잉..
라이선스 정책이 어떻게 되는지 몰라서.. ㅠㅠ 써도 되나

```python
my_waiter = wait("my_waiter", allow_multiple_execution=False)

    def wait_example(e):
        if e.newValue:
            global my_waiter
            # 실행하기 전에 리스트 추가하면 됨
            my_waiter.wait(5.0, relay_on)  # 5초
            my_waiter.wait(10.0, relay_off) # 10초
            my_waiter.wait(11.0, print, "Hello!") # 인수 추가하려면 튜플이나 딕셔너리 뒤에 넣으면 됨 args=() kwargs={}
            my_waiter.run()
            # 스케줄러를 강제 종료하려면 실행 시간 내에 .stop()을 호출해야 함

tp.port[1].button[1].watch(wait_example)

```


## 다국어 로그
context.log 는 utf-16 이라 ^^ 아하하.. 

```python
def uni_log_info(msg):
    context.log.info(msg.encode("utf-16").decode("utf-16"))


def uni_log_warn(msg):
    context.log.warn(msg.encode("utf-16").decode("utf-16"))
```


