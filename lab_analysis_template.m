%% V768 - Measuring Vision with Psychophysics
%  Lab XX - 
%
%  Learning Outcomes (what you will be able to do at the end):
%  1.
%  2. 
%

%% A. 
%
% Instructions: 
%
% Questions:
% A.1 - 
% A.2 - Write a figure caption for 
% A.3 - 
%


%% Load the data -- 
% 

% change the filename to the one you generated during data collection
filename = '.csv';
limit_data = readtable(filename);

% remove the rows/columns associated with the instructions in psychopy
limit_data(1,:)=[];
remove = {'notes','instructions_started','instructions_stopped'};
limit_data(:,remove) = [];

%% Visualize the trials
% 


%% Analyze

%% Plot


%% B. 
%
% Instructions: 
%
% Questions:
% B.1 - 
% B.2 - Write a figure caption for 
% B.3 - 
%


%% Load the data -- 
% 

% change the filename to the one you generated during data collection
filename = '.csv';
limit_data = readtable(filename);

% remove the rows/columns associated with the instructions in psychopy
limit_data(1,:)=[];
remove = {'notes','instructions_started','instructions_stopped'};
limit_data(:,remove) = [];

%% Visualize the trials
% 


%% Analyze

%% Plot
