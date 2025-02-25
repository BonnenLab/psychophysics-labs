function[ret] = psyfxn(c,x)
% psychometric function

% c(1) = mu
% c(2) = sigma
% c(3) = guess rate
% c(4) = lapse rate

ret=(normcdf(x, c(1), c(2)) * (1 - c(3) - c(4))) + c(3);
