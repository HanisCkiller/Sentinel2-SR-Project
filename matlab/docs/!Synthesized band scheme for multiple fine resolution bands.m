%%%%%The synthesized schem in ATPRK amounts to the use of all 10m bands
clear all;
load S2_20m;%%%20m bands in a image cube (6 bands)
load S2_10m;%%%10m bands in a image cube (4 bands)
s=2;
I_MS=S2_20m;
I_PAN=S2_10m;

w=1;
sigma=s/2;
PSFh=PSF_template(s,w,sigma);%%%Gaussian PSF
%PSFh=zeros((2*w+1)*s,(2*w+1)*s);PSFh(w*s+1:w*s+s,w*s+1:w*s+s)=1/s^2;%%%Ideal square wave PSF

Sill_min=1;
Range_min=0.5;
L_sill=20;
L_range=20;
rate=0.1;
H=20;

tic
for i=1:6
    [xrc1,RB0,Z0]=ATPRK_MSsharpen(I_MS(:,:,i),I_PAN,Sill_min,Range_min,L_sill,L_range,rate,H,w,PSFh);
    Z(:,:,i)=Z0;
end
alltime=toc

FalseColorf=Z(:,:,[3,2,1]);xf=imadjust(FalseColorf/1000,stretchlim(FalseColorf/1000),[]);figure,imshow(xf);
