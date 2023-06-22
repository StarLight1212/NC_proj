clear all;
[fname, pathname] = uigetfile({'*.btn';'*.plx'}, 'Select a btn file');
filename = strcat(pathname, fname);
alldata.spk=readBTNspike(filename);
alldata.ad=readBTNdata(filename);
alldata.event=readBTNevent(filename);
emg1 = alldata.ad.data{1,1};
emg2 = alldata.ad.data{1,2};
emg3 = alldata.ad.data{1,3};
emg4 = alldata.ad.data{1,4};
TA = emg1 - emg2;
GS = emg3 - emg4;
% 
% spike1_1 = alldata.spk.data{1,1}(:, 1);
% spike2_1 = alldata.spk.data{2,1}(:, 1);
% 
% spike1_9 = alldata.spk.data{1,1}(:, 9);
% spike2_9 = alldata.spk.data{2,1}(:, 9);
% 
% spike1_20 = alldata.spk.data{1,1}(:, 20);
% spike2_20 = alldata.spk.data{2,1}(:, 20);
% 
% spkts1 = alldata.spk.ts{1,1};
% spkts2 = alldata.spk.ts{2,1};


%% 829 sti test
[fname, pathname] = uigetfile({'*.btn';'*.plx'}, 'Select a btn file');
filename = strcat(pathname, fname);
alldata.spk=readBTNspike(filename);
alldata.ad=readBTNdata(filename);
alldata.event=readBTNevent(filename);

emgs = zeros(size(alldata.ad.data{1,1}, 1), 32);
for k = 1:32
    emgs(:, k) = alldata.ad.data{1,k};
end