EMGraw = readBTNdata(file);
pause(10)
EMGdata = EMGraw.data([1:16]);
clear  EMGraw

NameBNT = file(1:length(file)-4);
mkdir(NameBNT)
cd(NameBNT)

c = 1;
figure;
for c = 1:size(EMGdata,2)
    subplot(4,4,c)
    plot(EMGdata{c})
    title(string(c))
end

% print('Whole picture.tif','-dtiffn');
