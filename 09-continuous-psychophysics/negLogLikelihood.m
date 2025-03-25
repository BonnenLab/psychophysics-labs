function negLL = negLogLikelihood(params, x, k, N)

% define psychometric function
psyfxn = @(c,x) (normcdf(x, c(1), c(2)) * (1 - c(3) - c(4))) + c(3);
% c(1) = mu
% c(2) = sigma
% c(3) = guess rate
% c(4) = lapse rate

% calculate the probability from the psychometric function
p = psyfxn(params, x);
p = min(max(p, 1e-5), 1-1e-5);  % avoid log(0)

% compute negative log-likelihood
negLL = -sum(k .* log(p) + (N - k) .* log(1 - p));

end
