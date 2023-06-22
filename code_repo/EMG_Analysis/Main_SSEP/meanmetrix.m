function output = meanmetrix(Wave,TrangeInms)
	if nargin==1  
	    TrangeInms  =  [15,60];
    end


    Ts = -getPreTimeInms:1/getFs*1000:getObserveWin;
    
    Indsig = round(TrangeInms./1000.*getFs+getPreTimeInms./1000.*getFs);
    sig = ReshapeDataByIndex(Wave,Indsig(1):Indsig(2));
    Indnoise = intersect(find(Ts>70),find(Ts<100));
    noi = Wave(Indnoise);
    
    PPVsig = range(sig);
    PPVnoi = range(noi);
    
    PPVabs = PPVsig - PPVnoi;
    PPVrel = PPVsig ./ PPVnoi;
    PPVabs2 = PPVsig - 3.*std(noi);
    areasig = sum(abs(sig))*1000*(1/getFs)*1000;
    areanoi = sum(abs(noi))*1000*(1/getFs)*1000*(length(noi)/length(sig));
    areaauc = areasig - areanoi;
    SNNR = PPVabs./PPVnoi;
    output = [PPVsig,PPVnoi,areasig,areanoi,PPVabs,PPVrel,PPVabs2,areaauc,SNNR]';
end