import mido
import time
import subprocess
import re
import sys
import os

NAM_INPUT = "/run/jalv-nam-input"
IR_INPUT = "/run/jalv-ir-input"
PATTERN = "MIDI-FOOTSWITCH"

NAM_PRESETS_BANK = ["urn:nam:orange-clean", "urn:nam:orange-hi-gain", "urn:nam:marshall-clean"]

CURRENT_NAM_PRESET_INDEX = 0

NAM_PRESET_IR_MAP = {
    "urn:nam:orange-clean": "urn:brummer:impulseloader-state-orange",
    "urn:nam:orange-hi-gain": "urn:brummer:impulseloader-state-orange",
    "urn:nam:marshall-clean": "urn:brummer:impulseloader-state-marshall"
}

NAM_PRESET_OUTPUT_LEVEL_MAP = {
    "urn:nam:orange-clean": 0,
    "urn:nam:orange-hi-gain": -2,
    "urn:nam:marshall-clean": 0,
}

# urn:nam:orange-clean => orange-clean
def strip_uri(uri):
    return re.split(':', uri)[2]

def set_nam_output_level(level):
    with open(NAM_INPUT, 'w') as f:
        f.write(f'set output_level {level}\n')

def set_nam_preset(uri):
    ir_preset = NAM_PRESET_IR_MAP[uri]
    with open(NAM_INPUT, 'w') as f:
        f.write(f'preset {uri}\n')

def set_ir_preset(uri):
    with open(IR_INPUT, 'w') as f:
        f.write(f'preset {uri}\n')

def find_matching_port(ports):
    for p in ports:
        if PATTERN in p:
            return(p)

def get_input_port_name():
    inputs = mido.get_input_names()
    return(find_matching_port(inputs))


def get_output_port_name():
    outputs = mido.get_output_names()
    return(find_matching_port(outputs))

def set_preset_by_index(index):
    nam_preset_uri = NAM_PRESETS_BANK[index]
    ir_preset_uri = NAM_PRESET_IR_MAP[nam_preset_uri]
    nam_preset_output_level = NAM_PRESET_OUTPUT_LEVEL_MAP[nam_preset_uri]
    nam_preset_name = strip_uri(nam_preset_uri)

    set_nam_preset(nam_preset_uri)
    set_ir_preset(ir_preset_uri)
    set_nam_output_level(nam_preset_output_level)
    msg = mido.Message('sysex', data=bytearray(nam_preset_name.encode('utf-8')))
    output_port.send(msg)

def button_1_pressed(output_port):
    set_nam_preset("urn:nam:default-state")
    msg = mido.Message('sysex', data=bytearray(b'Fender'))
    output_port.send(msg)
    print("button 1")


def button_2_pressed(output_port):
    set_nam_preset("urn:nam:mesa")
    msg = mido.Message('sysex', data=bytearray(b'Mesa'))
    output_port.send(msg)
    print("button 2")


def button_3_pressed(output_port):
    msg = mido.Message('sysex', data=bytearray(b'CDE'))
    output_port.send(msg)
    print("button 3")

# previous preset
def button_4_pressed(output_port):
    global CURRENT_NAM_PRESET_INDEX
    CURRENT_NAM_PRESET_INDEX = (CURRENT_NAM_PRESET_INDEX - 1) % len(NAM_PRESETS_BANK)
    set_preset_by_index(CURRENT_NAM_PRESET_INDEX)


def button_5_pressed(output_port):
    msg = mido.Message('sysex', data=bytearray(b'EFG'))
    output_port.send(msg)
    print("button 5")

# next preset
def button_6_pressed(output_port):
    global CURRENT_NAM_PRESET_INDEX
    CURRENT_NAM_PRESET_INDEX = (CURRENT_NAM_PRESET_INDEX + 1) % len(NAM_PRESETS_BANK)
    set_preset_by_index(CURRENT_NAM_PRESET_INDEX) 
    
input_port_name = get_input_port_name()
output_port_name = get_output_port_name()

with mido.open_input(input_port_name) as input_port, mido.open_output(output_port_name) as output_port:
    print("port opened")
    for msg in input_port:
        if msg.type == 'control_change' and msg.value == 127:
            match msg.control:
                case 1: button_1_pressed(output_port)
                case 2: button_2_pressed(output_port)
                case 3: button_3_pressed(output_port)
                case 4: button_4_pressed(output_port)
                case 5: button_5_pressed(output_port)
                case 6: button_6_pressed(output_port)

