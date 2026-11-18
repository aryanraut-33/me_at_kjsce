% Take threshold input
thresh = input('Input the threshold: ');

if (thresh > 255)
    disp('Input should be less <= 255')
elseif (thresh < 0)
    disp('Input should be greater than 0')
else
    disp(['The threshold is ', num2str(thresh)])
end

% Read image
A = imread("/Users/aryan/Me@KJSCE/Sem VI/DSIP_lab/cosmos.jpg");

% Convert to grayscale if RGB
if size(A,3) == 3
    A = rgb2gray(A);
end

% Get image size
[m, n] = size(A);

% Initialize output image
B = zeros(m, n, 'uint8');

% Thresholding operation
for i = 1:m
    for j = 1:n
        r = A(i,j);
        if r <= thresh
            B(i,j) = 0;
        else
            B(i,j) = 255;
        end
    end
end

% Save and display result
imwrite(B, 'test1.bmp');
imshow(B);
title('Thresholded Image');
