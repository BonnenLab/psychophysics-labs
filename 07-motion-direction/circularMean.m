function [mu] = circularMean(deg)
% compute angular mean
x = deg2rad(deg);
r = sum(exp(1i*x));
mu = mod(rad2deg(angle(r)),360);


end

