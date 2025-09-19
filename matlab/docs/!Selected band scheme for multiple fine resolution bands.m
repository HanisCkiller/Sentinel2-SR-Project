%%%Selected band scheme selects a 10m band with the largest CC for each 20m band

clear all;
filepath_20m='D:\Project\data\area\Degraded_GT_clip_40m.tif';
filepath_10m='D:\Project\data\area\Degraded_10m_clip_20m.tif';
m20=imread(filepath_20m);
m10=imread(filepath_10m);
S2_20m=im2double(m20);
S2_10m=im2double(m10);
s=2;
I_MS=S2_20m;
I_PAN=S2_10m;

w=1;
sigma=s/2;
PSFh=PSF_template(s,w,sigma);%%%Gaussian PSF
%PSFh=zeros((2*w+1)*s,(2*w+1)*s);PSFh(w*s+1:w*s+s,w*s+1:w*s+s)=1/s^2;%%%Ideal square wave PSF

%%%%correlation analysis
I_PAN_upscaled=dowmsample_cube(I_PAN,s,w,PSFh);
for i=1:6
    for j=1:4
        [RMSE0,CC0]=evaluate_relation(I_MS(:,:,i),I_PAN_upscaled(:,:,j));
        CC_matrix(i,j)=CC0;
    end
end
[II,JJ]=max(CC_matrix,[],2);

Sill_min=1;
Range_min=0.5;
L_sill=20;
L_range=20;
rate=0.1;
H=20;

tic
for i=1:6
    [xrc1,RB0,Z0]=ATPRK_PANsharpen(I_MS(:,:,i),I_PAN(:,:,JJ(i)),Sill_min,Range_min,L_sill,L_range,rate,H,w,PSFh);
    Z(:,:,i)=Z0;
end
alltime=toc

FalseColorf=Z(:,:,[3,2,1]);xf=imadjust(FalseColorf/1000,stretchlim(FalseColorf/1000),[]);figure,imshow(xf);

[SS,R] = geotiffread(filepath_10m);
info = geotiffinfo(filepath_10m);
z_tz=im2uint16(Z);
geotiffwrite('D:\Project\data\area\ATPRK\new2.tif',z_tz, R, 'GeoKeyDirectoryTag', info.GeoTIFFTags.GeoKeyDirectoryTag, 'TiffType','bigtiff');

