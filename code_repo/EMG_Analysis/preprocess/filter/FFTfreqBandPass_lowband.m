function newsig = FFTfreqBandPass_lowband(wave,range)
% Input: wave for filtering
%        bandpass range
%        save freq
% Output: filtered data
     if (nargin<2)
        range = [1,30];
    end


    BandpassRange = range;
    wave  = reshape(wave,[1],[]);
    N = length(wave);
    fhat = fft(wave); %Compute the fast Fourier transform
    w = 2*pi*(0:N-1)./N; % normalized radian frequency
    freq = w./(2*pi)*getFs; % radian frequency to Hz
    magnitude = abs(fhat).^2/N;

    %% Construct the filtering
    % frequency vector of the filter. attenuates undesired frequency components
    % and keeps desired components. 
    H = ones(1, N);
    [m,p] = sort(magnitude,'descend');
   
    
    cutfreq=[p(find(m>m(1)*0.05))];
    i = 1;
    for i = 1:length(cutfreq)
        cutind1 = find(abs(freq-cutfreq(i))<0.8);
        H(cutind1) = 0;
        H(N+2-cutind1) = 0;
    end


    cutindhigh1 = intersect(find(freq>BandpassRange(2)),[2:getFs/2]);
    H(cutindhigh1) =  0;
    H(N+2-cutindhigh1) =  0;

    cutindlow2=intersect(find(freq>0),find(freq<BandpassRange(1)));
    H(cutindlow2) = 0;
    H(N+2-cutindlow2) = 0;
   
    clear Cutindhigh1 cutindlow1 

    %% Apply the filtering
    Transffhat = [];
    dR = 5000;
    R = ceil(length(H)./dR);
    H1 = H(1:dR*(R-1));

    HI1=num2cell(reshape(H(1:dR*(R-1)),[dR,R-1]),1);
    fhatI1 = num2cell(reshape(fhat(1:dR*(R-1)),[dR,R-1]),1);
    Transffhat1 = cellfun(@dotmulti,fhatI1,HI1,'UniformOutput',false);

    Transffhat1 = reshape(cell2mat(Transffhat1),[1],[]);

    rt = (R-1).*dR+1:length(H);
    Transffhat = [Transffhat1,fhat(rt).*H(rt)];
    clear Transffhat1

    newsig = ifft(Transffhat);
   
end