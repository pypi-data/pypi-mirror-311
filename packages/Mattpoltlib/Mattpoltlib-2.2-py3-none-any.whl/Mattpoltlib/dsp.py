class DSP:
    codes = [
        "Nhi milega",
        '''
n = -10:10;
impulse_signal = (n == 0);
figure;
stem(n, impulse_signal, 'filled'); 
title('Unit Impulse Signal');
xlabel('n');
ylabel('\delta[n]');
grid on;
h_n = (0.9).^n .* (n >= 0);
figure;
stem(n, h_n, 'filled'); 
title('Impulse Response of LTI System');
xlabel('n');
ylabel('h[n]');
grid on;

n = -20:20;
step_signal = (n >= 0);
figure;
stem(n, step_signal, 'filled'); 
title('Step Signal');
xlabel('n');
ylabel('u[n]');
grid on;

A = 1;       
F = 0.1;     
phi = 0;      
sine_signal = A * sin(2 * pi * F * n + phi);
figure;
stem(n, sine_signal, 'filled'); 
title('Sine Signal');
xlabel('n');
ylabel('sin(2 \pi F n + \phi)');
grid on;

cosine_signal = A * cos(2 * pi * F * n + phi);
figure;
stem(n, cosine_signal, 'filled'); 
title('Cosine Signal');
xlabel('n');
ylabel('cos(2 \pi F n + \phi)');
grid on;
        ''',
        '''
num = [1 1]; 
den = [1 2 1]; 
sys = tf(num, den);
disp('Transfer Function:');
disp(sys);
figure;
impulse(sys);
title('Impulse Response of H(s) = 1 / (s+1)^2');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;
syms t s
F_s = 1 / (s+1)^2;
f_t = ilaplace(F_s, s, t);
disp('Inverse Laplace Transform:');
disp(f_t);
figure;
fplot(f_t, [0, 10]);
title('Inverse Laplace Transform of H(s) = 1 / (s+1)^2');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;
        ''',
        '''
clc;
clear;
close all;
x = [1 2 3 4]; 
X = fft(x); 
x_reconstructed = ifft(X);
subplot(3,1,1);
stem(x, 'filled');
title('Original Signal x[n]');
xlabel('n');
ylabel('Amplitude');
subplot(3,1,2);
stem(abs(X), 'filled');
title('Magnitude of DFT X[k]');
xlabel('k');
ylabel('|X[k]|');
subplot(3,1,3);
stem(real(x_reconstructed), 'filled');
title('Reconstructed Signal x[n] (IDFT)');
xlabel('n');
ylabel('Amplitude');
disp('DFT of the signal x[n]:');
disp(X);
disp('Reconstructed signal using IDFT:');
disp(x_reconstructed);
        ''',
        '''
x = [1, 2, 3, 4]; 
h = [1, 1, 1, 1];
X = fft(x, length(x) + length(h) - 1); 
H = fft(h, length(x) + length(h) - 1);
Y = ifft(X .* H); 
stem(0:length(Y)-1, Y, 'filled');
xlabel('n');
ylabel('Amplitude');
title('Linear Convolution using FFT');
grid on;
        ''',
        '''
fs = 1000;
t = 0:1/fs:1;
f = 1; 
ecg_signal = 1.5 * sin(2 * pi * f * t) + 0.25 * sin(2 * pi * 50 * t);
plot(t, ecg_signal);
xlabel('Time (s)');
ylabel('Amplitude');
title('Simulated ECG Signal');
grid on;
csvwrite('ecg_signal.csv', ecg_signal);
        ''',
        '''
Fs = 1000; 
t = 0:1/Fs:1-1/Fs; 
f1 = 50;
f2 = 120;
x = cos(2*pi*f1*t) + cos(2*pi*f2*t); 
X = fft(x);
P = abs(X).^2/length(X);
freq = Fs*(0:(length(X)/2))/length(X); 
plot(freq, P(1:length(X)/2+1));
xlabel('Frequency (Hz)');
ylabel('Power');
title('Power Spectrum of the Given Signal');
        ''',
        '''
fs = 8000;
t = 0:1/fs:0.5-1/fs; 
f1 = 770;
f2 = 1336;
dtmf_signal = cos(2*pi*f1*t) + cos(2*pi*f2*t);
plot(t, dtmf_signal);
xlabel('Time (s)');
ylabel('Amplitude');
title('DTMF Signal for Digit 5');
sound(dtmf_signal, fs);
        ''',
        '''
fs = 1000; 
t = 0:1/fs:1-1/fs;
f = 50; 
x = cos(2*pi*f*t); 
x_decimated = downsample(x, 2);
t_decimated = downsample(t, 2);
x_interpolated = interp(x, 2);
t_interpolated = linspace(0, 1, length(x_interpolated));
subplot(3,1,1); plot(t, x); title('Original Signal');
subplot(3,1,2); plot(t_decimated, x_decimated); title('Decimated Signal');
subplot(3,1,3); plot(t_interpolated, x_interpolated); title('Interpolated Signal')
        ''',
        '''
%For High Pass Filter:
clc;
clear all;
close all;
n=20;
fp=300;
fq=200;
fs=1000;
fn=2*fp/fs;
window=blackman(n+1);
b=fir1(n,fn,'high',window);
[H W]=freqz(b,1,128);
subplot(2,1,1);
plot(W/pi,abs(H));
title('mag res of hpf');
ylabel('gain in db-------->');
xlabel('normalized frequency------>');
subplot(2,1,2);
plot(W/pi,angle(H));
title('phase res of hpf');
ylabel('angle-------->');
xlabel('normalized frequency------>');

%For Low Pass Filter:
clc;
clear all;
close all;
n=20;
fp=200;
fq=300;
fs=1000;
fn=2*fp/fs;
window=blackman(n+1);
b=fir1(n,fn,window);
[H W]=freqz(b,1,128);
subplot(2,1,1);
plot(W/pi,abs(H));
title('magnitude respones of lpf');
ylabel('gain in db');
xlabel('normalized frequency');
subplot(2,1,2);
plot(W/pi,angle(H));
title('Phase response of lpf');
ylabel('angle');
xlabel('normalized frequency');
        ''',
        '''
%For High Pass Filter:
clc;
clear all;
close all;
disp('enter the IIR filter design specifications');
rp=input('enter the passband ripple');
rs=input('enter the stopband ripple');
wp=input('enter the passband freq');
ws=input('enter the stopband freq');
fs=input('enter the sampling freq');
w1=2*wp/fs;w2=2*ws/fs;
[n,wn]=buttord(w1,w2,rp,rs,'s');
disp('Frequency response of IIR HPF is:');
[b,a]=butter(n,wn,'high','s');
w=0:.01:pi;
[h,om]=freqs(b,a,w);
m=20*log10(abs(h));
an=angle(h);
figure,subplot(2,1,1);plot(om/pi,m);
title('magnitude response of IIR filter is:');
xlabel('(a) Normalized freq. -->');
ylabel('Gain in dB-->');
subplot(2,1,2);plot(om/pi,an);
title('phase response of IIR filter is:');
xlabel('(b) Normalized freq. -->');
ylabel('Phase in radians-->');

%For Low Pass Filter:
clc;
clear all;
close all;
disp('enter the IIR filter design specifications');
rp=input('enter the passband ripple:');
rs=input('enter the stopband ripple:');
wp=input('enter the passband freq:');
ws=input('enter the stopband freq:');
fs=input('enter the sampling freq:');
w1=2*wp/fs;w2=2*ws/fs;
[n,wn]=buttord(w1,w2,rp,rs,'s');
disp('Frequency response of IIR LPF is:');
[b,a]=butter(n,wn,'low','s');
w=0:.01:pi;
[h,om]=freqs(b,a,w);
m=20*log10(abs(h));
an=angle(h);
figure,subplot(2,1,1);plot(om/pi,m);
title('magnitude response of IIR filter is:');
xlabel('(a) Normalized freq. -->');
ylabel('Gain in dB-->');
subplot(2,1,2);plot(om/pi,an);
title('phase response of IIR filter is:');
xlabel('(b) Normalized freq. -->');
ylabel('Phase in radians-->');
        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return DSP.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(DSP.codes)}."
