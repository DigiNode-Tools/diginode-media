#!/bin/bash
# recolour.sh in.png out.png : Imager's Mac red (171,30,58) -> Windows red (140,57,60), keeping blends with white
magick "$1" -channel RGB -fx 'xa=((1-u.r)*0.32941+(1-u.g)*0.88235+(1-u.b)*0.77255)/1.48390; xr=abs(u.r-(1-xa*0.32941))+abs(u.g-(1-xa*0.88235))+abs(u.b-(1-xa*0.77255)); (xa>0.03 && xa<1.08 && xr<0.2*xa+0.01) ? 1-xa*channel(0.45098,0.77647,0.76471,0) : u' +channel "$2"
