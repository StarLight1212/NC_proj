function alldata = readBTN()

[fname, pathname] = uigetfile({'*.btn';'*.plx'}, 'Select a btn file') ;
filename = strcat(pathname, fname);
alldata.spk=readBTNspike(filename);
alldata.ad=readBTNdata(filename);
alldata.event=readBTNevent(filename);

end
