import re
import string
import numpy as np
from collections import deque

# with open('Day20SampleInput.txt') as f:
# with open('Day20SampleInput2.txt') as f:
with open('Day20Input.txt') as f:
    data = f.read()

lines = data.strip('\n').split('\n')


class BeamModule:
    def __init__(self, details):  # )name, module_type, dest_modules):
        self.details = details

        source, dest = details.split(' -> ')
        if source == 'broadcaster':
            name = 'broadcaster'
            type = 'broadcaster'
            state = None
        elif source[0] == '%':
            name = source[1:]
            type = 'flip-flop'
            state = 0  # 0 for 'off', 1 for 'on'
        elif source[0] == '&':
            name = source[1:]
            type = 'conjunction'
            state = {}
        else:
            name = 'output'
            type = 'output'
            state = None

        dest_modules = dest.split(', ')

        self.name = name
        self.type = type
        self.dest_modules = dest_modules
        self.state = state
        self.beams_sent = {0: 0, 1: 0}

    def handle_pulse(self, pulse, source):
        if self.type == 'broadcaster':
            # Send the same pulse type on to all destination modules
            self.beams_sent[pulse] += 1 * len(self.dest_modules)
            return self.name, pulse, self.dest_modules

        if self.type == 'flip-flop':
            # High pulse - do nothing
            if pulse == 1:
                return

            # Low pulse - flip state and send a pulse
            if pulse == 0:
                # If previously off, turn on and send a high pulse
                # If previously on, turn off and send a low pulse
                self.state = self.state ^ 1
                # States are 0 or 1, as are low and high pulses, so can just send the state as the pulse
                self.beams_sent[self.state] += 1 * len(self.dest_modules)
                return self.name, self.state, self.dest_modules  # Assumption here that only ever has one destination module

        if self.type == 'conjunction':
            # Update memory for input
            self.state[source] = pulse
            # Check if high pulses are remembered for all inputs
            if set(self.state.values()) == {1}:
                # Send a low pulse
                self.beams_sent[0] += 1 * len(self.dest_modules)
                return self.name, 0, self.dest_modules
            # Send a high pulse
            self.beams_sent[1] += 1 * len(self.dest_modules)
            return self.name, 1, self.dest_modules

        if self.type == 'output':
            return



temp_list = []
for line in lines:
    temp_list.append(BeamModule(line))
beam_modules = {}
for beam_module in temp_list:
    beam_modules[beam_module.name] = beam_module
# Manually added
beam_modules['output'] = BeamModule('output -> output')
beam_modules['rx'] = BeamModule('output -> output')

# Need to initialise the conjuction modules?
for con_mod in beam_modules.values():
    if con_mod.type != 'conjunction':
        continue

    # Find all the connected input modules, and set hte initial memory state for them to 0 (low pulse)
    for bm in beam_modules.values():
        if con_mod.name in bm.dest_modules:
            con_mod.state[bm.name] = 0

# Get the original flip-flop and conjuction module states
orig_ff_module_states = {}
orig_con_module_states = {}
for name in beam_modules.keys():
    if beam_modules[name].type == 'flip-flop':
        orig_ff_module_states[name] = beam_modules[name].state
    elif beam_modules[name].type == 'conjunction':
        orig_con_module_states[name] = beam_modules[name].state


button_presses = 0
while button_presses < 1000:
    pulse_q = deque([('button', 0, ['broadcaster'])])
    button_presses += 1
    print(f"\nButton pressed again ({button_presses} button presses so far)")
    while pulse_q:
        # print(pulse_q)
        # Take the next beam to process from the top of the queue
        pulse_to_process = pulse_q.popleft()
        source = pulse_to_process[0]
        pulse = pulse_to_process[1]
        targets = pulse_to_process[2]
        for target in targets:
            # print(f"Sending pulse {pulse} from {source} to {target}")
            output = beam_modules[target].handle_pulse(pulse, source)
            if output:
                pulse_q.append(output)

        # Check state of flip-flop modules
        ff_module_states = {}
        con_module_states = {}
        for name in beam_modules.keys():
            if beam_modules[name].type == 'flip-flop':
                ff_module_states[name] = beam_modules[name].state
            elif beam_modules[name].type == 'conjunction':
                con_module_states[name] = beam_modules[name].state
        # print(f"Flip-flop module states: {ff_module_states}")
        # print(f"Conjunction module states: {con_module_states}")

    # Check if we're back to the original state or not
    if ff_module_states == orig_ff_module_states and con_module_states == orig_con_module_states:
        break

# print(f"Flip-flop module states: {ff_module_states}")
# print(f"Conjunction module states: {con_module_states}")

# Count number of pulses sent
total_pulses = {0: 0, 1: 0}
for bm in beam_modules.values():
    # if bm == 'TestOutputModule':
    #     continue
    total_pulses[0] += bm.beams_sent[0]
    total_pulses[1] += bm.beams_sent[1]
# Add on initial button press
total_pulses[0] += button_presses

print(f"\nTotal pulses after {button_presses} button presses:")
print(total_pulses)
total_low_pulses_1000_buttons = total_pulses[0] * (1000 / button_presses)
total_high_pulses_1000_buttons = total_pulses[1] * (1000 / button_presses)
print(f"Total low pulses after 1000 button presses: {total_low_pulses_1000_buttons}")
print(f"Total high pulses after 1000 button presses: {total_high_pulses_1000_buttons}")
print(f"Product: {total_low_pulses_1000_buttons * total_high_pulses_1000_buttons}")

print('hi')
