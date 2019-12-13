#!/usr/bin/env python3

# Resistor divider calculator for LDO feedback resistors with 2 selectable output voltages
# R1 is the resistor between the output and the feedback pin
# R2 and R3 are in series between the feedback pin and ground with R3 being connected to ground
# R2 + R3 is also named R23
# A n-channel MOSFET is connected parallel to R3, so R3 can be shorted
# This script assumes that R_DS_on of the MOSFET is << R3
# If this generates too many or no possibilities, change output_tolerance accordingly
# The values in multi are sometimes rounded weirdly, but I didn't investigate that, since the error is negligible small

v_ref = 0.8

u_out_lower = 1.8
u_out_higher = 3.3

output_tolerance = 0.001

r23_min = 5000
r23_max = 200000

e24_series = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

decades = [10 ** x for x in range(-1, 7)]


def r23_in_range(r23):
    return r23_min <= r23 <= r23_max


def value_is_candidate(ideal, real, tolerance):
    return (1 - tolerance) * ideal <= real <= (1 + tolerance) * ideal


def calc_v_out(r1, r23):
    return v_ref * (1 + r1 / r23)


r_all_values = []

for multi in decades:
    r_all_values += [multi * val for val in e24_series]

r23_values_in_range = [val for val in r_all_values if r23_in_range(val)]

candidates_higher = []

for r2 in r23_values_in_range:
    r1_candidates = [r1 for r1 in r_all_values if value_is_candidate(u_out_higher, calc_v_out(r1, r2), output_tolerance)]
    candidates_higher += [(r1, r2) for r1 in r1_candidates]

candidates_both = []

for (r1, r2) in candidates_higher:
    r3_candidates = [r3 for r3 in r_all_values if value_is_candidate(u_out_lower, calc_v_out(r1, r2 + r3), output_tolerance)]
    candidates_both += [(r1, r2, r3) for r3 in r3_candidates if r23_in_range(r2 + r3)]

for (r1, r2, r3) in candidates_both:
    out_high_real = calc_v_out(r1, r2)
    out_low_real = calc_v_out(r1, r2 + r3)
    print("R1:", r1, "| R2:", r2, "| R3:", r3, "| higher voltage:", out_high_real, "| lower voltage:", out_low_real)
