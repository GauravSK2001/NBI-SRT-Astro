import numpy
import matplotlib.pyplot as plt
# f = numpy.fromfile(open("/Users/gauravsenthilkumar/Desktop/Radio_tests/processed_frequency_spectrum"), dtype=numpy.float32)
# f = numpy.fromfile(open("/Users/gauravsenthilkumar/Desktop/Radio_tests/cold/processed_frequency_spectrum"), dtype=numpy.float32)
cold=numpy.fromfile(open("/Users/gauravsenthilkumar/Desktop/Radio_tests/cold_1"), dtype=numpy.float32)
hot=numpy.fromfile(open("/Users/gauravsenthilkumar/Desktop/Radio_tests/hot_1"), dtype=numpy.float32)
measure=numpy.fromfile(open("/Users/gauravsenthilkumar/Desktop/Radio_tests/m1"), dtype=numpy.float32)
f=cold
Vector_length = int(2**13)
print(numpy.shape(f)[0]/Vector_length)


central_freq = 1420.405751768e6
# central_freq = 1420e6
Bandwidth = 6e6
frequency_spacing=Bandwidth/Vector_length
freq = (numpy.linspace((central_freq-Bandwidth/2), central_freq + Bandwidth/2 , Vector_length)/1e6) - central_freq/1e6
f = f[0:Vector_length]


def plot(f,freq,title):
    fig,ax=plt.subplots(figsize=(10,5))
    ax.axvline(x=0/1e6, color='r', linestyle='--', label='HI 21cm line')
    ax.step(freq,10**f,where='mid',label='Measured PSD')
    ax.set_xlabel(r"Frequency ($\Delta \nu$) [MHz]")
    ax.set_ylabel(r"Temperature ($T$) [K]")
    ax.set_title(title)
    ax.grid()
    ax.legend()


# plot(hot)
# plot(cold)
# plot(measure)

# plt.plot(freq,10**hot/10**cold)


# plt.show()

shape_normalization = 10**hot/numpy.sum(10**hot)


Th=285
Tc=7

hot_shape_norm = 10**hot / shape_normalization
cold_shape_norm = 10**cold / shape_normalization
measure_shape_norm = 10**measure / shape_normalization

cut_off = 1000

Cut_freq = freq[cut_off:Vector_length-cut_off]
Hot=hot[cut_off:Vector_length-cut_off]
Cold=cold[cut_off:Vector_length-cut_off]
Measure=measure[cut_off:Vector_length-cut_off]
import scipy.integrate as int
shape_normalization = 10**Hot/int.trapezoid(y=10**Hot, x=Cut_freq)

print(int.trapezoid(y=shape_normalization, x=Cut_freq))
m = 10**Measure/shape_normalization

print(numpy.shape(m))


m = numpy.log10(m)

plot(Hot,Cut_freq,'Hot')
plot(Cold,Cut_freq,'Cold')
plot(shape_normalization,Cut_freq,'Shape Normalization')
plot(Measure/shape_normalization,Cut_freq,'Measure')



def Tcal(Power,Continuum_Hot,Continuum_Cold):
    
    m= (Th-Tc)/(Continuum_Hot-Continuum_Cold)
    b= (-1*(Continuum_Hot/(Continuum_Hot-Continuum_Cold))*(Th-Tc))+Th
    
    Tcal= m*Power + b
    return Tcal


calibration = Tcal(10**Measure,10**Hot,10**Cold)
print(calibration)
plot(numpy.log10(calibration),Cut_freq,'Calibrated PSD')
plt.show()


def calibrate(Power,Hot,Cold):
    m= (Th-Tc)/(Hot-Cold)
    b= (-1*(Hot/(Hot-Cold))*(Th-Tc))+Th
    
    Tcal= m*Power + b
    return Tcal
