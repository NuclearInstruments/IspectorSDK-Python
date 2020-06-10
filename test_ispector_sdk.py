from ispector_sdk import ispector_sdk
import pprint
import numpy as np
import matplotlib.pyplot as plt

I1 = ispector_sdk("192.168.50.2")

I1.set_hv_basic(True,41.5)
ChStatus = I1.getChannelStatus()
print(ChStatus["ICR"])

I1.configureMCA(trigger_threshold=100,
                trigger_inibit=300,
                pre_int_time=150,
                int_time=10,
                int_gain=100,
                pileup_inib=25,
                pileup_penality=25,
                baseline_inib=25,
                baseline_len=ispector_sdk.BaselineLength.BASELINE_512,
                target_run=ispector_sdk.RunMode.FREE,
                target_value=0
                )

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(ChStatus)


SysStatus = I1.getSystemStatus()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(SysStatus)


WaveMatrix = I1.getWave()

A = np.array(WaveMatrix)
wave_track = A[:,0]

plt.plot(wave_track)
plt.show()

while 1:
    SpectrumData = I1.getSpectrum()
    plt.plot(SpectrumData)
    plt.pause(1)

plt.show()


