
%% statistic 

    sigs = num2cell(data,1);
    OutTrial = cellfun(@StatisticOut_SSEP,sigs,'UniformOutput',false);
    OutTrial = reshape(cell2mat(OutTrial),[],size(sigs,2));
    rowNames = {'PPV' ,'latencyInms','T_Px','PPVnoi','SNR','adjPPVbyPPVnoi','adjPPVbySDnoi','Amplitude','SDnoi'
    }';
    meanOut = mean(OutTrial,2);
    MeanOut = table(rowNames,meanOut);
    Q25 = table(prctile(OutTrial',25)');
    Q50 = table(prctile(OutTrial',50)');
    Q75 = table(prctile(OutTrial',75)');
    OutStat = table(rowNames,OutTrial);
    
    writetable(rows2vars(MeanOut),'Statistic Output for trials.xls','WriteVariableNames',false,'WriteMode','overwrite');
    writetable(rows2vars(Q25),'Statistic Output for trials.xls',"WriteMode","append","AutoFitWidth",false);
    writetable(rows2vars(Q50),'Statistic Output for trials.xls',"WriteMode","append","AutoFitWidth",false);
    writetable(rows2vars(Q75),'Statistic Output for trials.xls',"WriteMode","append","AutoFitWidth",false);

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