function Out = StatisticOut_SSEP(W)
    sig = W(getPreTimeInms/1000*getFs+10/1000*getFs:getPreTimeInms/1000*getFs+45/1000*getFs);
    %10到45
    meansig = mean(sig);
    SDsig = std(sig);
    Amplitude = max(abs(sig));
    PPV = range(sig);
    noisedata = W(1:getPreTimeInms/1000*getFs-10/1000*getFs);
    SDnoi = std(noisedata);
    adjPPV_minus2SDnoi = PPV - 2*SDnoi;
    normedAmplitude = max(abs((sig - meansig)/SDsig));
    NormedPPV = range((sig - meansig)/SDsig);
    NormedAUC = sum(abs((sig - meansig)/SDsig))*(1/getFs);%(mV`s);
    try 
        latency = find(abs(sig)>2*SDnoi);
        latencyInms = latency(1)/getFs*1000+10;
        Out = [meansig;SDsig;latencyInms;Amplitude;normedAmplitude;PPV;NormedPPV;SDnoi;adjPPV_minus2SDnoi;NormedAUC];
    catch
        latencyInms = 50;
        Out = [meansig;SDsig;latencyInms;Amplitude;normedAmplitude;PPV;NormedPPV;SDnoi;adjPPV_minus2SDnoi;NormedAUC];
    end
end
