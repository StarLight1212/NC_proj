function plotEmgClip(muscleNames, emgClip, timingIndexes, nameG)

nMuscles = size(muscleNames, 2);

tAxis = (0:timingIndexes(end)) / EMG_FS() * 1000;
timings = timingIndexes / EMG_FS() * 1000;

% maxEmg = max(emgClip, [], 'all');
% minEmg = min(emgClip, [], 'all');
maxEmg = 0.45;
minEmg = -0.45;

figure,
tiledlayout(nMuscles, 1, 'TileSpacing', 'none')
for m = 1:nMuscles
    nexttile
    plot(tAxis, emgClip(:, m), 'Color', 'k')
    csvwrite(strcat(nameG, int2str(m),".csv"),emgClip(:,m));
    pbaspect
    ylim([minEmg maxEmg])
    xlim([0, tAxis(end)])
    pbaspect([5 1 1])
    
    ylabel(muscleNames{m})
    ax = gca;
    ax.TickDir = 'out';
    
end

end
