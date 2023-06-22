%% ---- read files ----
run("E:/CaoJian_Cell_Drug/Program/config/SetPath")
tic
cd([rootdir,'SSEP\']);

file = readtable('data_summary_ssep.csv');
rats = file.Label;
trials = file.Trial;
cd("data")

cellfun(@ssepiniview,rats,trials)

