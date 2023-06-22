function [clip, relativeTimingIndexes] = clipEmgs(emgs, absTimings)

absTimingIndexes = round(absTimings * 30000);
relativeTimingIndexes = absTimingIndexes - absTimingIndexes(1, 1);


clip = emgs(absTimingIndexes(1):absTimingIndexes(end), :);

end