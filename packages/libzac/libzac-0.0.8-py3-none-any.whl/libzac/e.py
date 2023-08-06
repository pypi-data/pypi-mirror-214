from __future__ import annotations
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from .math import byte2int,i3u1_to_i4
from subprocess import STDOUT, check_output, CalledProcessError

from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from .bitfield import bitfield

def einput(num, output_int=False):
    """convert all kind of input to hex string(default) or integer"""
    if isinstance(num, str):
        return int(num,16) if output_int else num 
    elif isinstance(num, (int, np.integer)):
        return num if output_int else f"{num:x}"
    elif isinstance(num, (float, np.float_)):
        num = int(np.around(num))
        return num if output_int else f"{num:x}"
    else:
        raise TypeError(f"Input type [{type(num)}] of [{num}] not supported")

def eread(addr, length=1, dtype="u1", ch=0, timeout=3):
    addr = einput(addr)
    length = einput(length)
    try:
        raw = check_output(f"e {addr}l{length}", stderr=STDOUT, timeout=timeout,  env={"ch":f"{ch}"}).decode("utf8")
    except CalledProcessError as e:
        print(e.output.decode("utf8"))
        raise e
    return e2int(raw, dtype=dtype)[0]

def ewrite(addr, value, ch=0, timeout=3):
    addr = einput(addr)
    value = einput(value)
    try:
        check_output(f"e {addr} {value}", stderr=STDOUT, timeout=timeout,  env={"ch":f"{ch}"})
    except CalledProcessError as e:
        print(e.output.decode("utf8"))
        raise e

def ewrite_block(addr, u1_data):
    addr = einput(addr)
    data_length = len(u1_data)
    addr = addr if isinstance(addr, int) else int(addr,16)
    
    for i in range(0,data_length,8):
        block = u1_data[i:min(i+8,data_length)]
        data = "".join([f"{b:02x}" if isinstance(b,(int,np.integer)) else b for b in block][::-1])
        start_address = f"{addr + i:x}"
        ewrite(start_address, data)

def e2byte(input, skip_row=1):
    if os.path.isfile(input):
        with open(input,"r") as f:
            raw = f.read()
    else:
        raw = input
    raw = raw.split("\n")[skip_row:]
    data = []
    addr = []
    start_addr = int(re.search(r"[0-9a-f]+(?= : )", raw[0]).group(), 16)
    start_addr += (re.search(r" [0-9a-f]{2} ", raw[0]).span()[0] - 8)//3
    for r in raw:
        row = re.split(r"(\W*[0-9a-f]+ : )", r)
        if len(row) > 2:
            for d in row[2].split(" "):
                if (len(d)==2):
                    data.append(int(d, 16))
                    addr.append(start_addr)
                    start_addr += 1
    byte = np.asarray(data, dtype=np.uint8).tobytes()
    addr = np.asarray(addr)
    return byte, addr

def e2int(input, dtype="<i4", skip_row=1):
    byte, addr = e2byte(input, skip_row=skip_row)
    itemsize = 1
    if isinstance(dtype, str):
        itemsize = int(dtype[-1])
    else:
        itemsize = np.dtype(dtype).itemsize
    return byte2int(byte, dtype), addr[::itemsize]

def e2plt(input, dtype="<i4", skip_row=1, x_hex=True, y_int=True):
    data, addr = e2int(input, dtype=dtype, skip_row=skip_row)
    fig, ax = plt.subplots()
    ax.plot(addr,data)
    if x_hex:
        ax.get_xaxis().set_major_formatter(lambda x, pos: hex(int(x)))
    if y_int:
        ax.get_yaxis().set_major_formatter(lambda x, pos: int(x))
    fig.show()

def e2write(input, skip_row=1):
    u1_data, addr = e2int(input, "u1", skip_row=skip_row)
    ewrite_block(addr[0], u1_data)

HREAD = HREAD2 = HREAD3 = HREAD_INLINE =        lambda reg: eread(reg)[0]
HREADW =                                        lambda reg: eread(reg, length=2, dtype="u2")[0]
HREAD24BIT = HREADADDR3 =                       lambda reg: i3u1_to_i4(eread(reg, length=3))[0]
HREAD4 = HREADL = HREADRV =                     lambda reg: eread(reg, length=4, dtype="i4")[0]

HWRITE = HWRITE2 = HWRITE3 = HWRITE_INLINE =    lambda reg, value: ewrite(reg, einput(value,output_int=True) & 0xff)
HWRITEW = HWRITEW_INLINE =                      lambda reg, value: ewrite(reg, einput(value,output_int=True) & 0xffff)
HWRITE24BIT =                                   lambda reg, value: ewrite(reg, einput(value,output_int=True) & 0xffffff) 
HWRITEL = HWRITERV = HWRITE4 =                  lambda reg, value: ewrite(reg, einput(value,output_int=True) & 0xffffffff)

def HREAD_STRUCT(reg, stc:bitfield):
    if einput(reg) == einput(stc.addr):
        stc.read()
    else:
        raise ValueError(f"reg '{reg}' is different from bitfield '{stc.__class__.__name__} @ {stc.addr}'")

def HWRITE_STRUCT(reg, stc:bitfield):
    if einput(reg) == einput(stc.addr):
        stc.write()
    else:
        raise ValueError(f"reg '{reg}' is different from bitfield '{stc.__class__.__name__} @ {stc.addr}'")
    
HREADW_STRUCT = HREAD24BIT_STRUCT = HREADL_STRUCT = HREAD_STRUCT
HWRITEW_STRUCT = HWRITE24BIT_STRUCT = HWRITEL_STRUCT = HWRITE_STRUCT