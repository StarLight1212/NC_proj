function [diffEmgs, site1Emgs, site2Emgs] = extractBtnEmgs(filePath, channelIndexes)

allData = readSpecBTN(filePath);
nMuscles = size(channelIndexes, 1);

site1Emgs = zeros(size(allData.ad.data{1, 1}, 1), nMuscles);
site2Emgs = zeros(size(allData.ad.data{1, 1}, 1), nMuscles);

for k = 1:nMuscles
    site1Emgs(:, k) = allData.ad.data{1, channelIndexes(k, 1)};
end

diffEmgs = site1Emgs - site2Emgs;

end