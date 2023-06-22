function ssepiniview(rat,trial)

    cd(rat)
    EMGraw = readBTNdata([trial,'.btn']);
    mkdir(trial)
    cd(trial)
    PointN = size(EMGraw.data{1},1);
    TotalT = PointN/getFs;
    TimeVector = linspace(0,TotalT,PointN)';
    run("Plot_wholeEMG")
    emgdata = EMGraw.data([3,7,2,6]);
    WaveSigs = cellfun(@FFTfreqBandPass,emgdata,num2cell(repmat([30,1000]',1,4),1),'UniformOutput',false);
    writecell({'channels:','3','7','2','6'},'raw_data.txt')
    writematrix([TimeVector,cell2mat(emgdata)],'raw_data.txt','WriteMode','append')

    writecell({'channels:','3','7','2','6'},'filtered_data.txt')
    writematrix([TimeVector,reshape(cell2mat(WaveSigs),[],4)],'filtered_data.txt','WriteMode','append')

    maxfigure
    plot(TimeVector,WaveSigs{1})
    title('channel 3')
    savefig(gcf,'RawEMG0.fig')
    cd ../../
end