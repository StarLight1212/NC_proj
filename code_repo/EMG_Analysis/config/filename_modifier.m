% modify filenames
i = 1;
trials = {};
for i=1:size(filenames,1)
    repN = KineticData.rep;
    if(repN(i)>1)
        filenames{i} = strcat(filenames{i},'-',string(repN(i)-1));
        filenames{i} = char(filenames{i});
        trials{i} = strcat(KineticData.Trial{i},'-',string(repN(i)-1));
        trials{i} = char(trials{i});
    else 
        trials{i} = KineticData.Trial{i};
    end
    
end

trials = trials';