%% V768 - Measuring Vision with Psychophysics
% Lab 2 - Signal Detection Theory
% 
% Based on https://gru.stanford.edu/doku.php/tutorials/sdt by Justin Gardner, 
% Stanford University
% 
% Learning Outcomes (what you will be able to do at the end):
%   1. Define and calculate Hits, Misses, False Alarms, Correct Rejections
%   2.

%% A. Simulating a Signal Detection Experiment
% We are going to simulate a signal detection experiment and an "ideal observer" 
% (an observer who behaves exactly according to signal detection theory).  This 
% is a useful thing to do when trying to understand any decision model, experimental 
% method, or an analysis tool. You get to control and play around with the simulation 
% to see what effect it has on the analysis that comes out.
% 
% Signal detection is a general framework in which an observer tries to detect 
% the presence or absence of a signal. What's a signal? Anything, really. Signal 
% might be to detect a faint light (can you see whether a candle is lit in a window 
% 1 mile away?). It could be to detect whether you see a friend's face within 
% a crowd. Sometimes these experiments are called “Yes / No” experiments in that 
% the observer has to say either “Yes” I saw it or “No” I did not. Sometimes there 
% is a signal there (the candle was lit, your friend was in the crowd) and these 
% are called signal present trials. Sometimes there is no signal there and those 
% are called signal absent trials. 
% 
% You did a Yes/No experiment last week in the method of constant stimuli portion 
% of the lab. Sometimes there was a grating in the circle, sometimes there wasn't.
% 
% Questions: 
% 
% * A.1 - 
% * A.2 - 
% * A.3 - 

%% Visualizing Hits/Misses/False Alarms/Correct Rejections
% Subjects are right if the correctly detect a signal when it is present (hit) 
% or when the correctly say the signal absent (correct reject). Similarly, subjects 
% can make two kinds of mistakes - say that the signal was there when it was actually 
% absent (false-alarm) or say that it was not there when it actually was (miss). 
% These kinds of errors have completely unhelpful names in statistics (type 1 
% or alpha for false-alarm and type 2 or beta for miss), so its more helpful to 
% think about them with these intuitive names! 
% 
% A key idea that motivates the theory of signal detection is that you want 
% to determine sensitivity (how good are subjects at detecting that faint candle 
% light), but that there is an unaccounted for cognitive factor - what criteria 
% the subject uses. A subject can have a very conservative criteria (only say 
% there is a light if they are very sure). This will lower false-alarm rates, 
% but then the subject may make more misses. A subject alternatively can change 
% their criteria so that they are less prone to missing, but then they will make 
% more false-alarms. Signal detection theory allows you to compute sensitivity 
% and criteria separately from subject responses (i.e. the hit and false-alarm 
% rates) so that you can determine how sensitive a subject is regardless of what 
% arbitrary criteria they used. 
% 
% We often visualize these components like this: 

fig=figure(); clf;
imshow('sdt.png')  
%% 
% By the end of this tutorial you should be able explain all the labelled pieces 
% of this picture (Hit, Miss, False Alarm, Correct Reject, Signal Absent, Signal 
% Present, Criterion, signal strength)

%% Simulating a signal-detection experiment.
% On each trial, our observer sees an element sampled from either the signal 
% present gaussian distribution or the signal absent distribution, which is also 
% gaussian with the same standard deviation.  Another way of saying this is that 
% on each trial the signal is either there or not.  What the observer sees is 
% determined by a draw from the signal present distribution or the signal absent 
% distribtion. The observer chooses to say “signal present” when the signal they 
% see on that trial is above criterion and “signal absent” otherwise.

% Signal trials should come from some gaussian distribution and noise trials 
% should come from another gaussian distribution that differ only in the means. 
% This is an assumption about the process that is termed iid - the signal 
% and noise come from independent identical distributions. 

% First we need to determine which trials will be signal and which will be
% signal-absent (or noise)
ntrials = 1000; % there will be n trials
% we choose to make the trials so that they are 1/2 signal present and 1/2 signal absent
signalPresentAbsent =  [ones(ntrials/2,1);zeros(ntrials/2,1)]; 
signalPresentAbsent = Shuffle(signalPresentAbsent); % shuffle the trial order

% Then we need to simulate the signal for the ideal observer on every trial.
% cycle over every trial
for i = 1:length(signalPresentAbsent)
  % if signal present trial
  if signalPresentAbsent(i) == 1
    % then pull a random draw from the signal distribution with mean = 1 and std = 1
    signal(i) = random('norm',1,1);
  else
    % otherwise it is a noise trial so pull a random draw from the noise distribution with mean = 0 and std = 1
    signal(i) = random('norm',0,1);
  end
end

figure(2); clf;
% Plot the signal-present distribution and the signal-absent distribution
 hold on;
% set up the x axis to have the same histogram bins for both trial types
histogram_bins = -5:.5:5;
% show signal present distribution
histogram(signal(signalPresentAbsent==1),histogram_bins);
% show signal absent distribution
histogram(signal(signalPresentAbsent==0),histogram_bins);
xlabel('signal strength');
ylabel('count');
box off;
axis square;
legend('signal-present','signal-absent')

%% Check your distributions to make sure they match what you expect.
% Now confirm numerically that the means and standard deviations of the signal-present 
% and signal-absent distributions are what they should be:

% display mean of signal present distribution (should be near 1)
mean(signal(signalPresentAbsent==1))
% display std of signal present distribution (should be near 1)
std(signal(signalPresentAbsent==1))
% mean and standard deviation for signal absent distribution should be 0 and 1 respectively
mean(signal(signalPresentAbsent==0))
std(signal(signalPresentAbsent==0))

%% Simulation Part II -- Simulating the response of the ideal observer
% Now we are going to simulate an ideal observer which will behave just as signal 
% detection says. The ideal observer will choose signal present (response=1) when 
% the signal they get to see (signal array from above) is greater than their internal 
% criterion and they will choose signal absent (response=0) when the signal is 
% below their internal criterion.
% 
% Let's start by making the criterion right in between the signal present and 
% absent distributions that we created above. That is, let's set criterion=0.5 
% and make an array of responses.

% setting up the "internal criterion"
criterion = .5;

% let's add the criterion to the visualization of the two distributions
figure(3); clf;
subplot(131); hold on;
% set up the x axis to have the same histogram bins for both trial types
histogram_bins = -5:.5:5;
% show signal present distribution
histogram(signal(signalPresentAbsent==1),histogram_bins);
% show signal absent distribution
histogram(signal(signalPresentAbsent==0),histogram_bins);
xlabel('signal strength');
ylabel('count');
box off;
axis square;
legend('signal-present','signal-absent')
subplot(131); hold on;
ax = gca;
plot([criterion,criterion],[0,ax.YLim(2)],'k--','LineWidth',2)
legend('signal-present','signal-absent','criterion')
% calculating the ideal observer response
response = signal >= criterion;
% get total number of present trials
nPresent = sum(signalPresentAbsent==1);

% compute hits as all the responses to trials in which signal was present (signalPresentAbsent==1) in which the response was present (i.e. == 1). Divide by number of present trials.
hits = sum(response(signalPresentAbsent==1)==1)/nPresent
% misses are the same except when the responses are 0 (absent even though signal was present)
misses = sum(response(signalPresentAbsent==1)==0)/nPresent

% same idea for correctRejects and falseAlarms
correctRejects = sum(response(signalPresentAbsent==0)==0)/nAbsent
falseAlarms = sum(response(signalPresentAbsent==0)==1)/nAbsent