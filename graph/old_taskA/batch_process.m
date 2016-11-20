% 
%   Simple script to batch process all the files in this directory
% 

files = dir('*.txt')

for i=1:length(files)
    graph_maker(files(i).name, 'time', 'error')
end
