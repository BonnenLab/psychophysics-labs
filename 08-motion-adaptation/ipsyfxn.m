function[ret] = ipsyfxn(c,p)
% define inverse psychometric function
% c(1) = mu
% c(2) = sigma
% c(3) = guess rate
% c(4) = lapse rate

ret = norminv((p - c(3))/(1 - c(3) - c(4)), c(1), c(2));
