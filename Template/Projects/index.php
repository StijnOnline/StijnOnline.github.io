<?php 
	if(!isset($_GET['Project']) || empty($_GET['Project'])){
	    $Project = "Projects";
	}else{ 
	    $Project = $_GET['Project']; 
	    if(file_exists("ProjectFiles/".$Project."/_page.php")){
	        $Project = $Project;
	    }else{
	    	$Project = "Projects";
	    }
	}
?>

<!DOCTYPE html>
<HTML>
<head>
	<?php include dirname(__FILE__)."/../_Header.php" ?>	
	<title>
		<?php 
			if($Project != 'Projects'){
				echo "PROJECT: ";
				echo str_replace("_"," ",$Project);
			}else{
				echo str_replace("_"," ",$Project);
			} 
		?> 
	</title>
</head>
<body> 	
	<?php include dirname(__FILE__)."/../_Nav.php"; ?>
 	<div class="Bottom">
		<?php
			if($Project == "Projects"){
				include 'LoadProjects.php';
				LoadProjects();
			}else{
				include "ProjectFiles/".$Project."/_page.php";
			}
		?>
	</div>
</body>
<HTML>