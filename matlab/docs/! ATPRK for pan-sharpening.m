clear all;
load Landsat_30m;%%%30m bands in a image cube (e.g., 8 bands for Landsat 8)
load Landsat_15m;%%%the 15m PAN band
s=2;
I_MS=Landsat_30m;
I_PAN=Landsat_15m;
[a,b,number_band]=size(Landsat_30m);

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
for i=1:number_band
    [xrc1,RB0,Z0]=ATPRK_PANsharpen(I_MS(:,:,i),I_PAN,Sill_min,Range_min,L_sill,L_range,rate,H,w,PSFh);
    Z(:,:,i)=Z0;
end
alltime=toc

FalseColorf=Z(:,:,[5,4,3]);xf=imadjust(FalseColorf/1000,stretchlim(FalseColorf/1000),[]);figure,imshow(xf);
