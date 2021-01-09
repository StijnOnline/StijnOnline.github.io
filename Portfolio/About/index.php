<!DOCTYPE html>
<HTML>
<head>
	<?php include dirname(__FILE__)."/../_Header.php" ?>
	<title>About</title>
</head>
<body>
	<?php include dirname(__FILE__)."/../_Nav.php"; ?>

	<div class="Bottom">
		<div class="TextBox CursorHover">
			<h class="TextBoxTitle Write Cursor">About</h>
			<p class="TextBoxText Write">
				Welcome to my site,<br>
				<br>
				I am Stijn van Deijzen, a 				
				<?php
					/*n-year code*/
					$startYear = new DateTime('2017-09-01');
					$now = new DateTime();
					$years = $now->diff($startYear)->y;
					switch($years){
						case 2: echo "second";break;
						case 3: echo "third";break;
						case 4: echo "fourth";break;
						default: echo "[Error]";break;
					}
					echo "-year";
				?>
				Game Development student at the University of the Arts Utrecht. I am mostly interested in creating unique experiences for Virtual Reality.
			</p>
		</div>
		<div class="TextBox CursorHover">
			<h class="TextBoxTitle Write Cursor">Profile Picture</h>
			<div class="TextBoxText">
			
			<img src="/About/ProfilePicture.jpg" class="FloatyImageLeft" style="height: 300px;width: 200px;">
				<p class="TextBoxDescription Write">This is how I look, just in case you wanted to know.</p>
			</div>
		</div>
	</div>
</body>
<HTML>