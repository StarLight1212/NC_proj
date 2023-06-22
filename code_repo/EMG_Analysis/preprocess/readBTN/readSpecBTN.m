function alldata = readSpecBTN(absname)

filename = strcat(absname);
alldata.spk=readBTNspike(filename);
alldata.ad=readBTNdata(filename);
alldata.event=readBTNevent(filename);

end
