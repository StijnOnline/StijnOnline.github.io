<nav id="Top">
    <img id="Logo" src="/Images/Icon.png" >
    <div id="TopText">
        <p id="FirstName" class="Write">StijnOnline</p>
        <p id="LastName" class="Write">Game Developer</p>
    </div>
    <a id="WritingNav" href=
        <?php 
            /*link*/ 
            if(isset($Project)) {
                if($Project != 'Projects')
                    echo "'.'";
                else
                    echo "'../'";
            } else{
                echo "'../'";
            }
        ?>
    >
	</a>
</nav>