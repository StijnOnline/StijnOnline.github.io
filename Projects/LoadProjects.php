<?php
	$MasterDirectory = getcwd();

	function LoadProjects(){
		global $MasterDirectory;

		$Projects = array();

		foreach (glob($MasterDirectory."/ProjectFiles/*",GLOB_ONLYDIR)  as $Directory) {			
			$DirectoryName = str_replace($MasterDirectory . "/ProjectFiles/","", $Directory);
			if(! file_exists("ProjectFiles/".$DirectoryName.'/_meta.json')){
				$Meta = "Meta file was Missing";
				$Priority=0;
			}else{
				$Meta = json_decode(file_get_contents("ProjectFiles/".$DirectoryName.'/_meta.json'), true);
				$Priority=$Meta['Priority'];
			}
			$Projects[$DirectoryName] = $Priority;
		}

		arsort($Projects);

		foreach ($Projects as $DirectoryName => $val) {	
			//echo"Prority: $val";
			DisplayProject($DirectoryName);
		}
	}

	function DisplayProject($DirectoryName){
		global $ProjectsPath;

			//$Title = str_replace("_"," ",$DirectoryName);

			if(! file_exists("ProjectFiles/".$DirectoryName.'/_thumbnail.jpg')){
				$ThumbNail = "ThumbNailError.png";
			}else{
				$ThumbNail = "ProjectFiles/".$DirectoryName.'/_thumbnail.jpg';
			}

			if(! file_exists("ProjectFiles/".$DirectoryName.'/_meta.json')){
				$Description = "Meta file was Missing";
			}else{
				$Meta = json_decode(file_get_contents("ProjectFiles/".$DirectoryName.'/_meta.json'), true);
				$Title = $Meta['FullName'];
				$Description = $Meta['Description'];
			}	

			$Link = $DirectoryName;

			/*echo "<a href='index.php?Project=" . $Link . "' class='ImageTextBox CursorHover'>";*/
			echo "<a href='" . $Link . "' class='ImageTextBox CursorHover'>";
				echo "<img src='" . $ThumbNail . "' class='ImageTextBoxImage'>";
				echo "<h class='ImageTextBoxTitle Write Cursor'>" . $Title . "</h>";
				echo "<div class='ImageTextBoxText'>";
					echo "<p class='ImageTextBoxDescription Write'>" . $Description . "</p>";
				echo "</div>";

			echo '</a>';

	}
?>