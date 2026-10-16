#!/bin/bash
W=$1/win; O=$W/out
R="-fill none -stroke #E0102F -strokewidth 3"
NEXT="roundrectangle 764,604 847,635 7,7"
crop() { magick "$W/$1" $R -draw "$NEXT" "${@:3}" -crop 598x464+341+178 +repage "$O/$2"; }
crop 05-next.png imager2-win-install-04-welcome.png
crop 06-licence.png imager2-win-install-05-licence.png -draw "roundrectangle 376,548 526,568 6,6"
crop 07-folder.png imager2-win-install-06-folder.png
crop 09-tasks-ticked.png imager2-win-install-07-shortcut.png -draw "roundrectangle 379,344 547,365 6,6"
magick "$W/10-installing.png" -crop 598x464+341+178 +repage "$O/imager2-win-install-08-installing.png"
magick "$W/11-finish.png" $R -draw "$NEXT" -crop 598x464+341+178 +repage "$O/imager2-win-install-09-finish.png"
