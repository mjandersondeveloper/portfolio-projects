<?php
$time = date("g:i a");
$hour = 8;
if ($hour < 12) {
 echo "Good morning!";
}
else if ($hour < 15) {
 echo "Good afternoon!";
}
else {
 echo "Good evening!";
}
?>

<?php
$time = date("g:i a");
$hour = 14;
if ($hour < 12) {
 echo "Good morning!";
}
else if ($hour < 15) {
 echo "Good afternoon!";
}
else {
 echo "Good evening!";
}
?>

<?php
$time = date("g:i a");
$hour = 17;
if ($hour < 12) {
 echo "Good morning!";
}
else if ($hour < 15) {
 echo "Good afternoon!";
}
else {
 echo "Good evening!";
}
?>

<?php
$time = date("g:i a");
$hour = 2;
if ($hour > 4 && $hour < 12) {
	echo "Good morning!";
}
else if ($hour > 12 && $hour < 15) {
	echo "Good afternoon!";
}
else if ($hour > 15 && $hour < 21) {
	echo "Good evening!";
}
else {
	echo "Good night!";
}
?>

<?php
$time = date("g:i a");
$hour = date("G");
if ($hour > 4 && $hour < 12) {
	echo "Good morning!";
}
else if ($hour > 12 && $hour < 15) {
	echo "Good afternoon!";
}
else if ($hour > 15 && $hour < 21) {
	echo "Good evening!";
}
else {
	echo "Good night!";
}
?>


