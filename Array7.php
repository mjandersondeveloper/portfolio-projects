<?php
$monthDays = array ('Splorch' => 23, 'Sploo' => 28,
 'Splat' => 2, 'Splatt' => 3,
 'Spleen' => 44, 'Splune' => 30,
 'Spling' => 61, 'Slendo' => 61,
'Sploctember' => 31, 'Splictember' => 31,
'Splanet' => 30, 'TheRest' => 22); 
foreach($monthDays as $month=>$days){
  echo $month." - ".$days."<br>";
};

ksort($monthDays);
  echo "<br>";
  echo "These are the months in alphabetical order!"."<br>";
  echo "<br>";
foreach($monthDays as $month=>$days){
  echo $month." - ".$days."<br>";
}
?>

