<?php
 $font = "./verdana.ttf";
 $text = $_GET["text"];
 $size = 13;

if (isset($_GET["inactive"])) {

 $im = ImageCreateFromPNG('marker-template-medium-inactive.png');
}
else {

 $im = ImageCreateFromPNG('marker-template-medium.png');
}

 imagesavealpha($im, true);
 // calculate position of text
 $tsize = ImageTTFBBox($size,18,$font,$text);
 $dx = abs($tsize[2]-$tsize[0]);
 $dy = abs($tsize[5]-$tsize[3]);
 $x = ( ImageSx($im) - $dx ) / 2;
 $y = 23;
 // draw text
if (isset($_GET["inactive"])) {

 $color = ImageColorAllocate($im,248,211,96);
}
else {

 $color = ImageColorAllocate($im,33,80,159);
}
 ImageTTFText($im, $size, 0, $x, $y, $color, $font, $text);
 header('Content-Type: image/png');
 ImagePNG($im);
?>