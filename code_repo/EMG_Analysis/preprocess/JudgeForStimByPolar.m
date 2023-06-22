%
dp = diff(p);
pi_x = p(find(dp>delT*0.7*getFs)+1);
Judpx = [];
x = 1;
jud = (abs(pi_x - px) - 0.5*delT*getFs)<0;
Judpx = sum(jud);
  
