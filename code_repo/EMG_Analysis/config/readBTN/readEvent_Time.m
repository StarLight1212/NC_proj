Eventdata = readBTNevent(file);
Chn_stim = Eventdata.nevs;

if cell2mat(Chn_stim(1))>3
    Chstim = 1;
elseif cell2mat(Chn_stim(2))>3
    Chstim = 2;
else 
    print('No stim events were found!')
end

try
    TStimInms = cell2mat(Eventdata.tsevs(Chstim))*1000;
    
catch
    % no action

end


