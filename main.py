import telnetlib as tl
import time
from time import sleep
import paramiko

# при ошибки ModuleNotFoundError: No module named 'paramiko'
# надо установаить модуль paramiko
#  pip install paramiko
# в терменале

HOST_ROUTER = '192.168.1.1'
HOST_EQ = '10.7.190.234'
USER = 'Admin'
SECRET = 'Admin'
SSH_AND_TELNET = ''
PORT = 22

###############################################
# сколько всего портов
PORTS = 20
# с какого порта начать
PORTS_START = 1
# todo
# пароль и логин для железок сапротские не то.#
LOGIN_MAIN_EQ = ''
PASS_MAIN_EQ = ''
###############################################


router_warning_again_main = []
router_warning_again = []


def _sleep(sec=0.6):
    sleep(sec)


def login_(eq, ports):
    global PASS_MAIN_EQ, LOGIN_MAIN_EQ
    _sleep()
    eq.write(f"{LOGIN_MAIN_EQ}\r".encode())
    _sleep()
    eq.write(f"{PASS_MAIN_EQ}\r".encode())
    _sleep()
    eq.write(b"terminal monitor\r")
    _sleep()
    eq.write(b"conf t\r")
    _sleep()
    eq.write(f"interface range fa0/1 - {ports}\r".encode())
    _sleep()
    eq.write("shutdown\r".encode())
    _sleep(5)


def switching_port_up(eq, current_port):
    eq.write(f"interface fa0/{current_port}\r".encode())
    _sleep()
    eq.write(b"no shutdown\r")
    eq.read_until(b'changed state to up\r')
    sleep(.1)


def switching_port_down(eq):
    eq.write(b"shutdown\r")
    _sleep()


def router_setup(eq_):
    _sleep()
    eq_.read_until(b'login')
    sleep(.1)
    eq_.write(b"Admin\r")
    _sleep()
    eq_.write(b"Admin\r")
    eq_.read_until(b'#')
    _sleep()
    eq_.write(b"nvram_set Password 5555911\r")
    _sleep()
    eq_.write(b"nvram_set AckPolicy 0\r")
    _sleep()
    eq_.write(b"nvram_set BssidIfName all\r")
    _sleep()
    eq_.write(b"nvram_set Language ru\r")
    _sleep()
    eq_.write(b"nvram_set NoForwarding 0\r")
    _sleep()
    eq_.write(b"nvram_set NoForwardingMBCast 0\r")
    _sleep()
    eq_.write(b"nvram_set RemoteManagement 2\r")
    _sleep()
    eq_.write(b"nvram_set SSID1 BISV\r")
    _sleep()
    eq_.write(b"nvram_set MaxStaNum 56\r")
    _sleep()
    eq_.write(b"nvram_set StationKeepAlive 60\r")
    _sleep()
    eq_.write(b"nvram_set SSID1INIC BISV-5GHZ\r")
    _sleep()
    eq_.write(b"nvram_set RADIUS_Key wive-ng-mt\r")
    _sleep()
    eq_.write(b"nvram_set RADIUS_Server 127.0.0.1\r")
    _sleep()
    eq_.write(b"nvram_set WNMEnable 0\r")
    _sleep()
    eq_.write(b"nvram_set FirstInstall 0\r")
    _sleep()
    eq_.write(b"nvram_set ACSCheckTimeINIC 0\r")
    _sleep()
    eq_.write(b"reboot\r")
    _sleep()
    eq_.close()
    _sleep()


def router_setup_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST_ROUTER, username=USER, password=SECRET, port=PORT)
    _sleep()
    client.exec_command("nvram_set Password 5555911")
    _sleep()
    client.exec_command("nvram_set AckPolicy 0")
    _sleep()
    client.exec_command("nvram_set BssidIfName all")
    _sleep()
    client.exec_command("nvram_set Language ru")
    _sleep()
    client.exec_command("nvram_set NoForwarding 0")
    _sleep()
    client.exec_command("nvram_set NoForwardingMBCast 0")
    _sleep()
    client.exec_command("nvram_set RemoteManagement 2")
    _sleep()
    client.exec_command("nvram_set SSID1 BISV")
    _sleep()
    client.exec_command("nvram_set MaxStaNum 56")
    _sleep()
    client.exec_command("nvram_set StationKeepAlive 60")
    _sleep()
    client.exec_command("nvram_set SSID1INIC BISV-5GHZ")
    _sleep()
    client.exec_command("nvram_set RADIUS_Key wive-ng-mt")
    _sleep()
    client.exec_command("nvram_set RADIUS_Server 127.0.0.1")
    _sleep()
    client.exec_command("nvram_set WNMEnable 0")
    _sleep()
    client.exec_command("nvram_set FirstInstall 0")
    _sleep()
    client.exec_command("nvram_set ACSCheckTimeINIC 0")
    _sleep()
    client.exec_command("reboot")
    client.close()


def initial_information():
    global HOST_ROUTER, HOST_EQ, PORTS, PORTS_START
    settings_rout()
    HOST_ROUTER = input('ip адрес роутера - ')
    HOST_EQ = input('ip адрес оборудования - ')
    PORTS = int(input('Количество портов - '))
    PORTS_START = int(input('С какого порта начинаем - '))


def settings_rout():
    print(f'''Текущие настройки:\n
    ip адрес роутера - {HOST_ROUTER}
    ip адрес оборудования - {HOST_EQ}
    Количество портов - {PORTS}
    С какого порта начинаем - {PORTS_START}'''
    )

    def main_setup():
        global router_warning_again
        connect_eq = tl.Telnet(HOST_EQ)
        login_(eq=connect_eq, ports=PORTS)
        router_warning_again = []
        for port in range(PORTS_START, PORTS + 1):
            logic_setup(port=port, connect_eq=connect_eq, list_router=router_warning_again)
        end_setup(connect_eq, router_warning_again)

    def main_setup_again():
        global router_warning_again_main, router_warning_again
        connect_eq = tl.Telnet(HOST_EQ)
        login_(eq=connect_eq, ports=PORTS)
        router_warning_again = []
        for port in router_warning_again_main:
            logic_setup(port=port, connect_eq=connect_eq, list_router=router_warning_again)
        end_setup(connect_eq, router_warning_again)

    def logic_setup(*, port, connect_eq, list_router):
        start = time.time()
        if SSH_AND_TELNET == '1':
            try:
                print(f'Поднимаем порт -{port}')
                switching_port_up(eq=connect_eq, current_port=port)
                print(f'Подключаемся к роутеру -{port}')
                # connect_router = tl.Telnet(HOST_ROUTER)
                print(f'Настраивает роутер -{port}')
                # router_setup(eq_=connect_router)
                router_setup_ssh()
                print(f'Готов роутер - {port}')
                switching_port_down(eq=connect_eq)
                print(f'Port down - {port}')
            except Exception:
                # connect_eq.close()
                switching_port_down(eq=connect_eq)
                list_router.append(port)
                print(f'Какая-то проблема с {port} роутером, Пропускаю его и перехожу к следующему')
            end = time.time()
            print('Время настройки - ', end - start)
        elif SSH_AND_TELNET == '2':
            try:
                print(f'Поднимаем порт -{port}')
                switching_port_up(eq=connect_eq, current_port=port)
                print(f'Подключаемся к роутеру -{port}')
                connect_router = tl.Telnet(HOST_ROUTER)
                print(f'Настраивает роутер -{port}')
                router_setup(eq_=connect_router)
                print(f'Готов роутер - {port}')
                switching_port_down(eq=connect_eq)
                print(f'Port down - {port}')
            except Exception:
                # connect_eq.close()
                switching_port_down(eq=connect_eq)
                list_router.append(port)
                print(f'Какая-то проблема с {port} роутером, Пропускаю его и перехожу к следующему')
            end = time.time()
            print('Время настройки - ', end - start)

    def end_setup(connect_eq, list_router):
        global router_warning_again_main
        if len(list_router) != 0:
            print(f'Проблемы с роутерами {list_router}'
                  f'\nповторная настройка проблемных роутеров')
            connect_eq.close()
            router_warning_again_main = list_router
            main_setup_again()
        else:
            print(f'Настроено {PORTS} роутеров')
            connect_eq.close()

    while True:
        user_input = input('''
        O - для изменения настроек
        P - для просмотра настроек
        SSH - 1
        Telnet - 2
        Для продолжения нажми 1 или 2:''')
        print('ПОЕХАЛИ')
        if user_input == 'o' or user_input == 'O':
            initial_information()
        elif user_input == 'i' or user_input == 'I':
            main_setup_again()
        elif user_input == 'p' or user_input == 'P':
            settings_rout()
        elif user_input == '1' or user_input == '2':
            SSH_AND_TELNET = user_input
            main_setup()