import numpy as np
import wave, struct
import soundMixer as sm

def generator_whiteNoise(amplitude=sm.default_amplitude, y_modifier=0):
    return [int(np.random.uniform(-amplitude, amplitude) + y_modifier) for x in range(sm.num_samples)]

def saveFile(samples1, samples2, filename):
    nframes = sm.num_samples
    comptype = "NONE"
    compname = "not compressed"
    nchannels = 1
    sampwidth = 2
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((nchannels, sampwidth, int(
        sm.sampleRate), nframes, comptype, compname))
    for s, t in zip(samples2, samples1):
        wav_file.writeframes(struct.pack('h', s))
        wav_file.writeframes(struct.pack('h', t))


def saveFile2(samples1, filename):
    nframes = sm.num_samples
    comptype = "NONE"
    compname = "not compressed"
    nchannels = 1
    sampwidth = 2
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((nchannels, sampwidth, int(
        sm.sampleRate), nframes, comptype, compname))
    for s in samples1:
        wav_file.writeframes(struct.pack('h', s))

if __name__ == '__main__':
    samplesWhite = sm.low_passFilter(generator_whiteNoise())
    samplesBrown = sm.FilterBrown(generator_whiteNoise())
    saveFile(samplesWhite, samplesBrown, "WindAudio.wav")


