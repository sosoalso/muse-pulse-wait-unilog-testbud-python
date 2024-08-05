# ---------------------------------------------------------------------------- #
from mojo import context

# ---------------------------------------------------------------------------- #
from pulse import pulse
from wait import wait


# ---------------------------------------------------------------------------- #
def uni_log_info(msg):
    context.log.info(msg.encode("utf-16").decode("utf-16"))


def uni_log_warn(msg):
    context.log.warn(msg.encode("utf-16").decode("utf-16"))


# ---------------------------------------------------------------------------- #
uni_log_info("파이썬 wait, pulse 테스트 프로그램")
# ---------------------------------------------------------------------------- #
muse = context.devices.get("idevice")
tp = context.devices.get("tp")
relay = muse.relay[0]
# ---------------------------------------------------------------------------- #


def muse_online_listener(_):
    uni_log_info("뮤즈 온라인")

    def relay_on():
        uni_log_info("릴레이 켜짐")
        relay.state = True

    def relay_off():
        uni_log_info(" 릴레이 꺼짐")
        relay.state = False

    @pulse(1.0, relay_off)  # 1초 후에 relay_off를 호출
    def pulse_relay():
        uni_log_info("릴레이 펄스")
        relay_on()

    def button_watcher_pulse_relay(e):
        if e.value:
            pulse_relay()

    def relay_state_watcher(e):
        tp.port[1].channel[1].value = e.newValue

    my_waiter = wait("my_waiter", allow_multiple_execution=False)

    def wait_example(e):
        if e.newValue:
            nonlocal my_waiter
            my_waiter.wait(5, relay_on)
            my_waiter.wait(10, relay_off)
            my_waiter.run()
            # 스케줄러를 강제 종료하려면 실행 시간 내에 .stop()을 호출해야 함

    tp.port[1].button[1].watch(button_watcher_pulse_relay)
    tp.port[1].button[1].watch(wait_example)
    relay.state.watch(relay_state_watcher)
    uni_log_info("뮤즈 온라인 실행 완료")


# ---------------------------------------------------------------------------- #


# leave this as the last line in the Python script
muse.online(muse_online_listener)
uni_log_info("프로그램 로딩됨")

# ---------------------------------------------------------------------------- #
context.run(globals())
