% Comparison of kd=.4 for different kp values
data = {
[23 23 19 5 -5 -7 -8 -7 -5 4 9 11 6 0 -3 -4 -4 -2 3 6 7 5 1 -1 -2 -1 1 3 4 3 3 2 1 1 1 3 3 3 3 2 1 1 1 1 1 2 3 3 2 1 1 1 1 2 2 2 2 2 1 1 1 1 3 3 3 4 4 4 3 3 3 3 4 4 4 4 4 5 4 4 4 4 4 4 4 4 3 3 4 4 4 3 3 3 3 2 2 1 2 2 1 1 1 1 1 1 2 3 3 2 1 1 2 2 2 2 3 3 3 3 2 2 2 2 2 2 2 3 3 2 1 1 1 2 2 2 2 2 1 1 1 1 2 2 3 3 4 5 4 3 3 3 3 1 2 4 6 7 7 ]
[36 36 20 -8 -9 -9 -9 -9 -8 -8 -8 -6 2 12 18 11 -3 -7 -8 -9 -7 3 20 22 9 -4 -8 -9 -9 -8 -2 11 16 12 2 -6 -8 -9 -7 0 11 17 13 4 -3 -7 -7 -7 -3 5 10 9 4 -1 -5 -5 -2 2 6 6 4 1 -1 -2 -1 1 3 3 3 2 2 1 2 3 4 4 3 2 1 2 3 3 3 2 3 3 3 3 3 3 4 4 4 3 1 0 1 1 2 3 2 1 0 0 0 1 1 2 2 1 0 -1 0 1 1 1 1 2 1 1 1 1 2 1 1 1 1 1 1 1 0 0 0 1 2 3 2 1 0 0 0 0 1 2 3 2 1 1 1 1 1 1 3 5 5 4 1 0 0 1]
}


kp_vals=[0.8,1.3];
[~,n] = size(kd_vals);
figure; hold on;
CM = lines(n);

% plot1 = [1]
plot1 = [1:2];
[~,m] = size(plot1);
labels = cell(m,1);

for i=1:m
    idx = plot1(i);
    labels{i} = sprintf('kp = %.1f', kp_vals(idx));
    plot(data{idx},'color', CM(idx,:), 'linewidth', 1.5);
end


title({'Error value from PD controller with kd=0.4'; 'moving along a straight line'})
xlabel('Time')
ylabel('Error from PD controller')
legend(labels, 'Location', 'northeast')
saveas(figure(1), 'kd_curve.jpg'); % Saves as a jpg
