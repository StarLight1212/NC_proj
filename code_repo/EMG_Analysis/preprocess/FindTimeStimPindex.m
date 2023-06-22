% FindTimeStimPindex
if threshold1>0
    p = find(wave>threshold1);
    [mp,in1] = max(wave(p(1):p(1)+dur/1000*getFs));
    pi1 = p(1)-1+in1-round(dur/1000*getFs*1/4);
    px = [pi1:delT*getFs:length(wave)];

else
    p = find(wave<threshold1);
    [mp,in1] = min(wave(p(1):p(1)+dur/1000*getFs));
    pi1 = p(1)-1+in1-round(dur/1000*getFs*3/4);
    px = [pi1:delT*getFs:length(wave)];
end

run("JudgeForStimByPolar");
px = px(find(Judpx==1));
px = union(pi1,px);
TStimInms = px./getFs*1000;
