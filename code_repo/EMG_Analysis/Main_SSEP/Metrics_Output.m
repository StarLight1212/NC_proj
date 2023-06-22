
%% statistic 

    sigs = num2cell(data(getPreTimeInms*getFs/1000:end,:),1);
    OutTrial = cellfun(@StatisticOut,sigs,'UniformOutput',false);
    OutTrial = reshape(cell2mat(OutTrial),[],size(sigs,2));
    rowNames = {'meanrecsig','SDrecsig','adjPPV','PPV_SNR','Inarea','latencyInms','meanrecnoi','SD_noise'}';

    meanOut = mean(OutTrial,2);
    MeanOut = table(rowNames,meanOut);
    OutStat = table(rowNames,OutTrial);
    
    writetable(rows2vars(MeanOut),'Statistic Output for trials.xls','WriteVariableNames',false,'WriteMode','overwrite');

    writetable(rows2vars(splitvars(OutStat)),'Statistic Output for trials.xls',"WriteMode","append","AutoFitWidth",false);
    
    %% write
    if r == 0 
    else
    Metrics(r).rowNames = rowNames;
    Metrics(r).MeanOut = meanOut;
    Metrics(r).statistics = OutStat;
    Metrics(r).case = Case;
    Metrics(r).channel = NO(Chn);
    
    end