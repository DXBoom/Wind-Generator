import numpy as np
import math

duration = 2
sampleRate = 44100.0
num_samples = int(sampleRate * duration)
default_amplitude = 16000

def low_pass_filterSample(x, cutting_frequency, resonance_value, previous_values):
    s = math.sin(2 * np.pi * cutting_frequency / sampleRate)
    c = math.cos(2 * np.pi * cutting_frequency / sampleRate)
    alpha = s / (2 * resonance_value)
    r = 1 / (1 + alpha)
    a0 = 0.5 * (1-c) * r
    a1 = (1-c)*r
    a2 = a0
    b1 = -2 * c * r
    b2 = (1 - alpha) * r

    y = (a0 * x) + (a1 * previous_values["x1"]) + (a2 * previous_values["x2"]) - \
        (b1 * previous_values["y1"]) - (b2 * previous_values["y2"])
    return int(y)


def low_passFilter(samples, modulated_cf=[]):
    cutting_frequency = 1000
    resonance_value = 1
    new_samples = [0] * len(samples)
    if not modulated_cf:
        modulated_cf = [cutting_frequency] * len(samples)
    previous_values = {
        "x1": 0,
        "x2": 0,
        "y1": 0,
        "y2": 0
    }
    for i in range(2, len(samples)):
        new_samples[i] = low_pass_filterSample(
            samples[i], modulated_cf[i], resonance_value, previous_values)
        previous_values = {
            "x1": samples[i],
            "x2": samples[i-1],
            "y1": new_samples[i],
            "y2": new_samples[i-1]
        }
    return new_samples


def filterSampleBrown(x, cutting_frequency, resonance_value, previous_values):
    s = math.sin(2 * np.pi * cutting_frequency / sampleRate)
    c = math.cos(2 * np.pi * cutting_frequency / sampleRate)
    alpha = s / (2 * resonance_value)
    r = 1 / ((1 + alpha) ** 2)
    a0 = 0.5 * (1-c) ** r
    a1 = (1-c)**r
    a2 = a0
    b1 = -2 * c * r
    b2 = (1 - alpha) ** r

    y = (a0 * x) + (a1 * previous_values["x1"]) + (a2 * previous_values["x2"]) - \
        (b1 * previous_values["y1"]) - (b2 * previous_values["y2"])
    return int(y)


def FilterBrown(samples, modulated_cf=[]):
    cutting_frequency = 450
    resonance_value = 1
    new_samplesBrown = [0] * len(samples)
    if not modulated_cf:
        modulated_cf = [cutting_frequency] * len(samples)
    previous_values = {
        "x1": 0,
        "x2": 0,
        "y1": 0,
        "y2": 0
    }
    for i in range(2, len(samples)):
        new_samplesBrown[i] = filterSampleBrown(
            samples[i], modulated_cf[i], resonance_value, previous_values)
        previous_values = {
            "x1": samples[i],
            "x2": samples[i-1],
            "y1": new_samplesBrown[i],
            "y2": new_samplesBrown[i-1]
        }
    return new_samplesBrown