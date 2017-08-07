<?php
 session_start();

$_SESSION['page'][] = $_SERVER['PHP_SELF'];

echo "The last page you visited was: ".$_SERVER['PHP_SELF'].'<br />';
echo "List of pages you've visited: ".'<br />'; 

foreach ($_SESSION['page'] as $key) {
	
	echo $key.'<br>';
};
?>
<a href="page1.php">Page 1</a> 
<a href="page2.php">Page 2</a> 
<a href="page3.php">Page 3</a> 
<a href="page4.php">Page 4</a> 
<a href="page5.php">Page 5</a> 
