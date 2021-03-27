import pandas as pd
import json
import asyncio
import websockets
import time
import MySQL_Request
import sys
import unittest
#   Блок с функциями которые пригодятся для мелких задач


def get_value_from_json(string, found_string):
    """
    Помогает перевести сырой ответ после запроса в нужный атрибут
    :param string: Сюда вкидываем site-answer
    :param found_string: Тот ответ что мы хотим найти, как пример found_string = 'access_token'
    :return: Возвращает значение атрибута что мы указали в found_string
    """

    if found_string == 'estimated_delivery_price':
        new_str = string[string.find(found_string):string.find(found_string) + len(string) - string.find(found_string)]
        new_str = new_str[(new_str.find(':')+1):(new_str.find(',')-1)]
        return new_str
    if found_string == 'access_token':
        new_str = string[string.find(found_string):string.find(found_string) + len(string) - string.find(found_string)]
        arrow = (new_str.find(':') + 2)
        new_str = new_str[arrow:new_str.find('"', arrow)]
        return new_str
    if found_string == 'refresh_token':
        new_str = string[string.find(found_string):string.find(found_string) + len(string) - string.find(found_string)]
        arrow = (new_str.find(':') + 2)
        new_str = new_str[arrow:new_str.find('"', arrow)]
        return new_str
    if found_string == 'order_id':
        new_str = string[string.find(found_string):len(string)]
        new_str = new_str[(new_str.find(':') + 2):(new_str.find('"', new_str.find(':') + 2))]
        return new_str
    if found_string == 'mark_price':
        new_str = string[string.find(found_string):string.find(found_string) + len(string) - string.find(found_string)]
        new_str = new_str[(new_str.find(':')+1):(new_str.find(','))]
        return new_str
    if found_string == 'order_state':
        new_str = string[string.find(found_string):len(string)]
        new_str = new_str[(new_str.find(':') + 2):(new_str.find('"', new_str.find(':') + 2))]
        return new_str
    if found_string == 'filled_amount':
        new_str = string[string.find(found_string):len(string)]
        new_str = new_str[(new_str.find(':')+1):(new_str.find(',', new_str.find(':') + 1))]
        return new_str
    if (found_string != 'estimated_delivery_price') and \
            (found_string != 'access_token') and (found_string != 'order_id') and \
            (found_string != 'mark_price') and (found_string != 'order_state'):
        print('Робот говорит:')
        print('Я не уверен что аттрибут json строки будет найден корректно')
        new_str = string[string.find(found_string):string.find(found_string) + len(string) - string.find(found_string)]
        new_str = new_str[(new_str.find(':')+1):(new_str.find(','))]
        return new_str


#   Конец блока функций мелких задач


#   Функционал робота
class ImRobot():

    def __init__(self, name, config_file_way):
        self.name = name
        config = pd.read_csv(str(config_file_way), header=0, sep=' ')
        self.gap = float(config.iloc[list(config.index).index('gap:'), 0])
        self.gap_ignore = float(config.iloc[list(config.index).index('gap_ignore:'), 0])
        self.client_id = str(config.iloc[list(config.index).index('client_id:'), 0])
        self.client_secret = str(config.iloc[list(config.index).index('client_secret:'), 0])
        self.operation_volume = float(config.iloc[list(config.index).index('operation_volume:'), 0])
        self.iterations_numbers = int(config.iloc[list(config.index).index('numbers_of_iterations:'), 0])
        self.time_interval = float(config.iloc[list(config.index).index('time_interval:'), 0])

    #       Новые настройки вписывать сюда

    def amount_setup(self, amount):
        self.operation_volume = float(amount)

    def orders_params(self, current_price, method):
        """
        Функция считает цены ордера
        :param current_price: Актуальная цена на инструмент
        :param method: 'BUY' - ордер на покупку, 'SELL' - ордер на продажу
        :return: Возвращает цену для установки ордера
        """
        if method == 'BUY':
            buy_price = current_price - (self.gap/2)
            return buy_price
        if method == 'SELL':
            sell_price = current_price + self.gap
            return sell_price

    def close_params(self, order_price, method):
        """
        Функция считает параметры при которых ордер будет отклонен
        :param order_price: Цена по которой ордер был открыт
        :param method: 'BUY' - ордер был куплен, 'SELL' - орден был продан
        :return: STOP_ORDER_PRICE
        """
        if method == 'BUY':
            close_buying = order_price + self.gap + self.gap_ignore
            return close_buying
        if method == 'SELL':
            close_selling = order_price - self.gap - self.gap_ignore
            return close_selling

    def add_access_token(self, key):
        self.access_token = key

    def add_refresh_token(self, key):
        self.refresh_token = key


#   Описание робота законченно


def close_order(robot_name, order_id):
    """
    Функция принудительно закрывает ордер
    :param robot_name: Имя робота
    :param order_id: id ордера который необходимо принудительно закрыть
    :return: NONE
    """
    import asyncio
    import websockets
    import json

    msg = \
        {
            "jsonrpc": "2.0",
            "id": 4214,
            "method": "private/cancel",
            "params": {
                "order_id": order_id,
                "access_token": str(robot_name.access_token),
            }
        }

    async def call_api(message):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(message)
            while websocket.open:
                response = await websocket.recv()
                return response
    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'close_order')
        sys.exit()


def authenticator(robot_name):
    """
    Аутентификация на бирже
    :param robot_name: Имя робота
    :return: access_token
    """
    msg = \
    {
        "jsonrpc": "2.0",
        "id": 9929,
        "method": "public/auth",
        "params": {
            "grant_type": "client_credentials",
            "client_id": str(robot_name.client_id),
            "client_secret": str(robot_name.client_secret),
            "scope": "session:testnet, expires:60000"
        }
    }

    async def call_api(message):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(message)
            while websocket.open:
                response = await websocket.recv()
                access_token = get_value_from_json(response, 'access_token')
                refresh_token = get_value_from_json(response, 'refresh_token')
                robot_name.add_refresh_token(refresh_token)
                robot_name.add_access_token(access_token)
                return access_token

    try:
        asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'authenticator')
        sys.exit()


def get_market_price():
    """
    Функция находит рыночную цену инструмента
    :return: возвращает актуальную рыночную цену
    """
#   Разные цены содержатся в ответе от вызова /get_order_book
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 8772,
            "method": "public/get_order_book",
            "params": {
                "instrument_name": "BTC-PERPETUAL",
                "depth": 5
            }
        }

    async def call_api(message):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(message)
            while websocket.open:
                response = await websocket.recv()
                return float(get_value_from_json(response, 'mark_price'))
    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'get_market_price')
        sys.exit()


def order_placement(robot_name, price, method):
    """
    Функция выполняет выставление ордера
    :param robot_name: имя ордера
    :param price: цена по которой следует выставить ордер
    :param method: метод выставления ордера 'BUY' or 'SELL'
    :return:
    """
    robot_volume = robot_name.operation_volume
    if float(robot_volume) < 10:
        robot_name.operation_volume = 10

    if method == 'BUY':
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 5275,
                "method": "private/buy",
                "params": {
                    "instrument_name": "BTC-PERPETUAL",
                    "amount": int(robot_name.operation_volume),
                    "type": "limit",
                    "price": float(price),
                    "label": "market0000234",
                    "access_token": str(robot_name.access_token),
                }
            }

    if method == 'SELL':
         msg = \
            {
                "jsonrpc": "2.0",
                "id": 5275,
                "method": "private/sell",
                "params": {
                    "instrument_name": "BTC-PERPETUAL",
                    "amount": int(robot_name.operation_volume),
                    "type": "limit",
                    "price": float(price),
                    "label": "market0000234",
                    "access_token": str(robot_name.access_token),
                }
            }

    async def call_api(message):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(message)
            while websocket.open:
                response = await websocket.recv()
                return response
    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'order_placement')
        sys.exit()



def order_status(robot_name, order_id):
    """
    Функция проверяет статус выполнение ордера
    :param robot_name: имя робота
    :param order_id: id ордера который необходимо проверить
    :return: строку запрос
    """
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 4316,
            "method": "private/get_order_state",
            "params": {
                "order_id": str(order_id),
                "access_token": str(robot_name.access_token),
            }
        }

    async def call_api(message):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(message)
            while websocket.open:
                response = await websocket.recv()
                return response

    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'order_status')
        sys.exit()


def connection_test():
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 8212,
            "method": "public/test",
            "params": {

            }
        }

    async def call_api(msg):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                return response

    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'connection_test')
        sys.exit()


def re_login(robot_name):
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 9929,
            "method": "public/auth",
            "params": {
                "grant_type": "refresh_token",
                "refresh_token": robot_name.refresh_token
            }
        }

    async def call_api(msg):
        async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                access_token = get_value_from_json(response, 'access_token')
                refresh_token = get_value_from_json(response, 'refresh_token')
                robot_name.add_refresh_token(refresh_token)
                robot_name.add_access_token(access_token)
                return response

    try:
        return asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
    except Exception:
        print('Connection to deribit failed...')
        print('MODULE:', 'order_status')
        sys.exit()



def BUYING_ORDER(robot_name):
    try:
        connection_test()
    except Exception:
        print('Connection to deribit failed...')
        print('*Starter module failed')
        sys.exit()
    time_interval = robot_name.time_interval
    status_of_success = 1
    current_price = get_market_price()
    buy_price = robot_name.orders_params(current_price, 'BUY')
    stop_buy_price = robot_name.close_params(buy_price, 'BUY')
    order_information = order_placement(robot_name, buy_price, 'BUY')
    order_id = get_value_from_json(str(order_information), 'order_id')
    order_current = get_value_from_json(order_status(robot_name, order_id), 'order_state')
    time_counter = 0
    timer = 0
    MySQL_Request.base_placement('BUY', 'ORDER_PLACED', current_price, robot_name.operation_volume)
    while order_current != 'filled':
        try:
            connection_test()
        except Exception:
            print('Connection to deribit failed...')
            print('*Starter module failed')
            sys.exit()
        time.sleep(time_interval)
        time_counter += 1
        timer = time_interval*time_counter
        order_current = get_value_from_json(order_status(robot_name, order_id), 'order_state')
        current_price = get_market_price()
        if float(stop_buy_price) < float(current_price):
            if '"Invalid params"' != get_value_from_json(order_status(robot_name, order_id), 'message'):
                order_less = get_value_from_json(order_status(robot_name, order_id), 'filled_amount')
                close_order(robot_name, order_id)
            else:
                order_less = 0
            MySQL_Request.base_placement('BUY', 'ORDER_CANCELED', current_price, robot_name.operation_volume)
            status_of_success = 0
            break

    if status_of_success == 0:
        return 'FALSE', timer, current_price, order_less

    if status_of_success == 1:
        order_less = 0.666
        MySQL_Request.base_placement('BUY', 'ORDER_COMPLETE', current_price, robot_name.operation_volume)
        return 'TRUE', timer, current_price, order_less


def SELLING_ORDER(robot_name):
    try:
        connection_test()
    except Exception:
        print('Connection to deribit failed...')
        print('*Starter module failed')
        sys.exit()
    time_interval = robot_name.time_interval
    status_of_success = 1
    current_price = get_market_price()
    sell_price = robot_name.orders_params(current_price, 'SELL')
    stop_sell_price = robot_name.close_params(current_price, 'SELL')
    order_information = order_placement(robot_name, sell_price, 'SELL')
    order_information = str(order_information)
    order_id = get_value_from_json(order_information, 'order_id')
    order_current = get_value_from_json(order_status(robot_name, order_id), 'order_state')
    time_counter = 0
    timer = 0
    MySQL_Request.base_placement('SELL', 'ORDER_PLACED', current_price, robot_name.operation_volume)
    while order_current != 'filled':
        try:
            connection_test()
        except Exception:
            print('Connection to deribit failed...')
            print('*Starter module failed')
            sys.exit()
        time.sleep(time_interval)
        time_counter += 1
        timer = time_interval*time_counter
        order_current = get_value_from_json(order_status(robot_name, order_id), 'order_state')
        current_price = get_market_price()
        if float(stop_sell_price) > float(current_price):
            if '"Invalid params"' != get_value_from_json(order_status(robot_name, order_id), 'message'):
                order_less = get_value_from_json(order_status(robot_name, order_id), 'filled_amount')
                close_order(robot_name, order_id)
            else:
                order_less = 0
            MySQL_Request.base_placement('SELL', 'ORDER_CANCELED', current_price, robot_name.operation_volume)
            status_of_success = 0
            break

    if status_of_success == 0:
        return 'FALSE', timer, current_price, order_less
    if status_of_success == 1:
        order_less = 0.666
        MySQL_Request.base_placement('SELL', 'ORDER_COMPLETE', current_price, robot_name.operation_volume)
        return 'TRUE', timer, current_price, order_less


def body():

    index = 0
    v_2 = ImRobot('v_2', 'Config.txt')
    authenticator(v_2)
    standard = v_2.operation_volume
    time_count = 0
    iteration = 0
    auth_timer = 0
    try:
        connection_test()
    except Exception:
        print('Connection to deribit failed...')
        print('*Starter module failed')
        sys.exit()

    while iteration < v_2.iterations_numbers:
        auth_timer = time_count
        if auth_timer > 20000:
            re_login(v_2)
            auth_timer = 0
        iteration += 1
        status = 'FALSE'
        v_2.operation_volume = standard
        while status == 'FALSE':
            index += 1
            status, timer, order_price, order_remain = BUYING_ORDER(v_2)
            time_count += float(timer)
            if order_remain != '':
                v_2.operation_volume = v_2.operation_volume - float(order_remain)
                print('V-2 VOLUME', v_2.operation_volume)

        status = 'FALSE'
        v_2.operation_volume = standard
        while status == 'FALSE':
            index += 1
            status, timer, order_price, order_remain = SELLING_ORDER(v_2)
            time_count += float(timer)
            if order_remain != '':
                v_2.operation_volume = v_2.operation_volume - float(order_remain)

    print('ALL TIME:', time_count, 'SECS')


body()
