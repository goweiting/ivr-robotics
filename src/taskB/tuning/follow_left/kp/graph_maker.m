function graph_maker(filename, x_axis, y_axis)

clc;
fileID = fopen(filename,'r');

for k=1:1
    title=fgets(fileID)
end

[results, count]= fscanf(fileID, '%d', inf);
plot(results)
ax = gca;
ax.XAxisLocation = 'origin';

title(title);
xlabel(x_axis);
ylabel(y_axis);

[file_save, remain] = strtok(filename, '.'); % Removes the file extension

file_save = [file_save, '.jpg'];

saveas(figure(1), file_save); % Saves as a jpg

end
