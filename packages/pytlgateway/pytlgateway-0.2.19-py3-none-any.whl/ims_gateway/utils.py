from datetime import datetime
import sys
import os

from constants import ORDER_SIDE, Side



#没有融券
def encode_ims_side(side):
    rtn_trade_side = 0
    if side == 1:
        rtn_trade_side = 1
    elif side == 2:
        rtn_trade_side = 2
    elif side == 5:
        rtn_trade_side = 3
    return rtn_trade_side

def decode_ims_side(side):
    order_side = ""
    if side == 0:
        order_side = "Long Buy"
    elif side == 1:
        order_side = "Long Sell"
    elif side == 2:
        order_side = "Short Sell"
    elif side == 3:
        order_side = "Buy To Cover"
    return order_side

def decode_atx_target_type(side):
    f_side = 0
    if side in [1,5]:
        return 1
    elif side == 2:
        return 2

def decode_ims_contract_type(contract_type):
    str_type = ""
    if contract_type == 0:
        str_type = "TRS"
    elif contract_type == 1:
        str_type = "RISKY"
    return str_type

def decode_ims_status(status):
    new_status = ""
    if status == 'P_FILLED':
        new_status = 'active'
    elif status == 'F_FILLED':
        new_status = 'filled'
    elif status == 'CANCELED':
        new_status = 'canceled'
    return new_status

def side_to_target_type(side):
    target_type = ""
    if side in [1,5]:
        target_type = "buy"
    elif side == 2:
        target_type = "sell"
    return target_type

def decode_exchange_id(exchange):
    exchange = 0
    if exchange == 'SH':
        exchange = 101        #EXCHANGE_SSE 
    elif exchange == 'SZ':
        exchange = 102        #EXCHANGE_SZE 
    
    return exchange
    
def get_log_default_path():
    # python2: linux2, python3: linux
    if sys.platform.startswith("linux") or sys.platform == "darwin":
        dirs = "/shared/log"
    elif sys.platform == "win32":
        dirs = os.path.join(get_windows_first_disk() + "/tmp/linker/log")
    else:
        dirs = '.'

    return dirs

def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

def get_digit_from_env(env_name, default_num):
    num = str(os.environ.get(env_name))
    return int(num) if num.isdigit() else default_num

def get_log_given_path(path):
    dirs = os.path.join(path)
    return path

def decode_ordtype(order_type:str):
    ord_type = -1
    mapping = {
        'TWAP': 0,
        'VWAP': 1,
        'VOLINLINE': 2,
        'ICEBERG': 3
    }
    ord_type = mapping.get(order_type, -1)
    return ord_type
