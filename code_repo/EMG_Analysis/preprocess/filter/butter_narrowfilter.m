function output = butter_narrowfilter(W,range)
    if nargin == 1
        range = [30,3000];
    end
    d = designfilt('bandpassiir','FilterOrder',10, ...
    'HalfPowerFrequency1',range(1),'HalfPowerFrequency2',range(2), ...
    'SampleRate',getFs);%butter 20 
    
    %figure;plot(Ts,filter(d,W))
    %fvt = fvtool(d,'Fs',getFs);
    output = filter(d,W);
    
end