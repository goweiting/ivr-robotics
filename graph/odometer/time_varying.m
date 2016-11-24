% varying time with constant duty_cycle_sp and speed_sp


a = [0 0 1 3 6 9 12 15 18 21 24 28 31 35 39 42 46 49 52 56 ];
b = [0 0 1 3 5 7 10 13 16 19 23 26 30 34 38 42 45 48 52 56 60 63 67 71 74 77 81 85 88 91 94 98 101 104 107 110 114 117 121 123 ];
c = [0 0 1 3 5 8 11 14 17 20 23 27 31 34 38 41 45 48 52 55 59 63 67 71 74 78 81 85 89 93 99 103 108 112 115 119 123 127 130 134 137 141 144 148 151 155 159 163 166 170 173 177 181 184 188 191 195 199 203 207 ];
d = [0 0 1 2 6 8 11 14 17 21 24 27 31 35 39 42 45 48 52 55 59 62 65 69 72 76 79 82 86 89 92 96 99 102 105 109 112 116 120 123 126 129 133 136 139 143 146 150 153 157 161 164 168 171 175 179 183 187 190 194 197 201 205 208 212 215 219 222 226 229 233 237 241 244 248 251 255 258 262 265 ];
e = [0 0 1 3 5 8 10 13 16 19 23 26 30 34 37 40 44 47 51 55 59 63 67 71 75 79 82 87 90 94 97 101 105 108 111 114 118 121 125 128 131 134 138 141 144 148 151 155 158 161 164 168 171 174 178 181 184 188 191 194 198 201 205 208 212 215 219 223 227 230 234 237 241 245 249 253 256 260 264 268 271 275 279 283 286 289 293 297 301 304 307 311 315 318 322 326 329 333 337 341];
dataStrct= {a,b,c,d,e};
data = zeros(5,100);
time = [2000,4000,6000,8000,10000];
dist = [4,8,12,15,18];

[~,n] = size(dist);
labels = cell(n,1);
% XTickLabels = cell(n,1);
figure; hold on;
for i=1:n
    labels{i} = sprintf('time %d ms, dist %.1f cm', time(i), dist(i));
    data(i,:) = [dataStrct{i} zeros(1, 100-length(dataStrct{i}))];
end

for i=1:11
    XTickLabels{i} = sprintf('%d', (i-1)*1000);
end

plot(data', 'LineWidth', 2)
title('Tacho counts with varying time and constant duty 25');
xlabel('Time (ms)')
set(gca, 'XTickLabel', XTickLabels, 'XTickLabelRotation', 90)
ylabel('Average Tacho Counts between L and R motor')
legend(labels, 'Location', 'best')
saveas(figure(1), 'time_varying.jpg'); % Saves as a jpg
