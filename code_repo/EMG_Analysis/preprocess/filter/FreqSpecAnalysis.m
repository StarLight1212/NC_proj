function freqspc = FreqSpecAnalysis(wave)
    wave = reshape(wave,[1],[]);
    N = length(wave);
    fhat = fft(wave); %Compute the fast Fourier transform
    w = 2*pi*(0:N-1)./N; % normalized radian frequency
    freq = w./(2*pi)*getFs; % radian frequency to Hz
    %angsig = 180*unwrap(angle(fhat))./pi;
    magnitude = abs(fhat).^2/N;
    freqspc = [freq',magnitude'];
    figure
    plot(freq,magnitude,'c','LineWidth',3)
    
    xlim([0 3000])

    xlabel('Frequency (Hz)')
    ylabel('R.Magnitude (dB)')
    title('frequency-domain signal, magnitude vs. frequency');
    print('Frequency Spectrum.tif','-dtiffn');
    savefig('Frequency Spectrum.fig')
end
