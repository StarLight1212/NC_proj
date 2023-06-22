function output = sepfilename(filename,rank)
    output = [char(filename(1:3)),'\',char(rank),char(filename(5:end))];
end
