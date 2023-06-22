function Out = StatisticOut(sig)

    meansig = mean(sig);
    SDsig = std(sig);


    %Amplitude = max(abs(sig));
    noidata = sig((getObserveWin-200+getPreTimeInms)/1000*getFs:(getObserveWin-100+getPreTimeInms)/1000*getFs);
    sigdata = sig(getPreTimeInms/1000*getFs:(getPreTimeInms+500)/1000*getFs);
    
    meanrecsig = mean(abs(sigdata));
    SDrecsig = std(abs(sigdata));
    PPVsig = range(sigdata);

    SDnoi = std(abs(noidata));
    meanrecnoi = mean(abs(noidata));
    PPVnoi = range(noidata);

    adjPPV = PPVsig - PPVnoi;
    PPV_SNR = PPVsig/PPVnoi;
    Inarea = sum(abs(sigdata))*(1/getFs) - SDnoi/length(noidata)*length(sigdata)*(1/getFs);

    try 
        latency = find(abs(sig)>3*SDsig);
        latencyInms = latency(1)/getFs*1000;
    catch
        latencyInms = 50;
    end
    
    Out = [meanrecsig;SDrecsig;adjPPV;PPV_SNR;Inarea;latencyInms;meanrecnoi;SDnoi];
end
