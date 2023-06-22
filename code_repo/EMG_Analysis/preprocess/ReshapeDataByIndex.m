function data = ReshapeDataByIndex(Eseq,IndicesStim)
    % Index: n×m
%     Eseq =[10 100;20 200;30 300;40 400;50 500;60 600];
%     IndicesStim=[1 2 3;5 6 7;8 9 10];
    i = 1;
    Eseq = reshape(Eseq,[],[1]);
%     Eseq =[10;20;30;40;50;60;100;200;300;400;500;600];
    data = [];

    for i = 1:size(IndicesStim,1)
        data = [data,Eseq(IndicesStim(i,:))];
% i=1,data=[data,[10;20;30]]=[10;20;30]
% i=2,data=[data,[50;60;100]]=[10 50
%                              20 60
%                              30 100]
    end
% data=[20,40,60;30,50,100];
end
% Eseq =
%     10   100
%     20   200
%     30   300
%     40   400
%     50   500
%     60   600

% IndicesStim =
%   1     2     3
%   5     6     7
%   8     9     10

% data =
%     10    50    200
%     20    60    300
%     30    100   400


