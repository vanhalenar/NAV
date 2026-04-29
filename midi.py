import mido
import time
import subprocess

NAM_INPUT = "/run/jalv-nam-input"
IR_INPUT = "/run/jalv-ir-input"
PATTERN = "MIDI-FOOTSWITCH"

def set_nam_preset(uri):
    with open(NAM_INPUT, 'w') as f:
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


def button_4_pressed(output_port):
    msg = mido.Message('sysex', data=bytearray(b'DEF'))
    output_port.send(msg)
    print("button 4")


def button_5_pressed(output_port):
    msg = mido.Message('sysex', data=bytearray(b'EFG'))
    output_port.send(msg)
    print("button 5")


def button_6_pressed(output_port):
    msg = mido.Message('sysex', data=bytearray(b'FGH'))
    output_port.send(msg)
    print("button 6")
    
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

print("got here at least")