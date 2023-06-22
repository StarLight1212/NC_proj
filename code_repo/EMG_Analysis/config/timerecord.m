 tic ;%tic2
 t2=clock;
    pause(3*rand)
    %计算到上一次遇到tic的时间，换句话说就是每次循环的时间
    disp(['toc计算第',num2str(RunTestCount),'次循环运行时间：',num2str(toc)]);
    %计算每次循环的时间
    disp(['etime计算第',num2str(RunTestCount),'次循环运行时间：',num2str(etime(clock,t2))]);
    %计算程序总共的运行时间
    disp(['etime计算程序从开始到现在运行的时间:',num2str(etime(clock,t1))]);
    disp('======================================')