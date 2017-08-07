<?php
$monthDays = array ('Splorch' => 23, 'Sploo' => 28,
 'Splat' => 2, 'Splatt' => 3,
 'Spleen' => 44, 'Splune' => 30,
 'Spling' => 61, 'Slendo' => 61,
'Sploctember' => 31, 'Splictember' => 31,
'Splanet' => 30, 'TheRest' => 22); 
echo "The shortest month is ", min($monthDays)."<br>";
echo "The longest month is ", max($monthDays)."<br>";
echo "The total number of days in the year is ", array_sum($monthDays)."<br>";

foreach ($monthDays as $month=>$days)
{
	if ($days == min($monthDays))
	{
  	  echo "The shortest month is ",$month."<br>";
	}
	if ($days == max($monthDays))
	{
  	  echo "The longest month is ",$month."<br>";
	}
}
?>

