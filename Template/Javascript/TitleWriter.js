var WritingNavElement;
var PageTitle;
var Writer;
var PageWriteTime = 2000;


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

doneWriting = false
window.addEventListener('load', function () {
	WritingNavElement = document.getElementById('WritingNav');
	//PageTitle = document.title;
	PageTitle = WritingNavElement.textContent;

	Writer = new TextWriter("< "+PageTitle);	
	Writer.Start();

	/*add checking to prevent queing too many of the same event*/
	if(WritingNavElement != null){
		WritingNavElement.addEventListener('mouseenter', async function () {			
			Writer.SetText('< Back');
		})

		WritingNavElement.addEventListener('mouseleave', async function () {			
			Writer.SetText("< "+PageTitle);

		})
	}

	WriteTexts();
	SetCursorEvents();
});

//Set CursorHover events
async function SetCursorEvents(){
	var elements = document.querySelectorAll('.CursorHover');
	if(elements.length != 0){
		for (var e = 0; e < elements.length; e++) {
			elements[e].querySelectorAll('.Cursor')[0].innerHTML = elements[e].querySelectorAll('.Cursor')[0].innerHTML + "&nbsp;";


			elements[e].addEventListener('mouseenter', async function () {
			    if (!doneWriting) return;
				var element = this.querySelectorAll('.Cursor')[0];							
				element.innerHTML = element.innerHTML.replace("&nbsp;",'') + '|';
			})

			elements[e].addEventListener('mouseleave', async function () {
			    if (!doneWriting) return;
				var element = this.querySelectorAll('.Cursor')[0];
				element.innerHTML = element.innerHTML.replace('|',"&nbsp;");
			})
		}
		console.log("Added CursorHover Events to " + elements.length + " elements");
	}
}



async function WriteTexts(){
	var elements = document.getElementsByClassName('Write');
	var texts = [];
	var totalcharacters = 0;
	if(elements.length != 0){
		for (var e = 0; e < elements.length; e++) {
			texts[e] = elements[e].innerHTML;
			totalcharacters + elements[e].innerHTML.length;
			elements[e].innerHTML = "&nbsp;";
		}

		for (var e = 0; e < elements.length; e++) {
			
			var i = 1;		
			elements[e].innerHTML = "|";
			while(i<=texts[e].length)
	    	{    	
	    		await sleep(PageWriteTime / totalcharacters);	
		    	elements[e].innerHTML = texts[e].slice(0,i) +"|";
		    	i++;
		    	
			}
			elements[e].innerHTML = texts[e];
		}
	}
	doneWriting = true
}




class TextWriter{
	RemoveDelay = 10;
	WriteDelay = 10;

	text = "";
	state= "writing"; /*writing,removing,done*/

	constructor(startText) {
        this.text = startText;
    }

	SetText(_text){
		if(_text.includes(WritingNavElement.innerHTML.replace("|","")) || WritingNavElement.innerHTML=="&nbsp;"){
			this.state = "writing";
		}else{
			this.state = "removing";
		}
		this.text = _text;	
	}

	async Start(){
		var i = 0;		
		while(true){
			if (this.state == "removing") {	
				await sleep(this.RemoveDelay);			
				if(i<1){
					WritingNavElement.innerHTML = "&nbsp;";
					this.state = "writing";
				}else{
					WritingNavElement.innerHTML = WritingNavElement.innerHTML.replace("|","").slice(0,i)  +"|";
		    		i--;
				}
				//console.log(i+" removing: "+ WritingNavElement.innerHTML);
				
				
			}else if(this.state == "writing"){
				await sleep(this.WriteDelay);
				if(i>this.text.length){
					WritingNavElement.innerHTML = this.text.slice(0,i);
					this.state = "done";
				}else{
					WritingNavElement.innerHTML = this.text.slice(0,i).replace("|","")  +"|";
		    		i++;
				}
				//console.log(i+" writing: "+ WritingNavElement.innerHTML);
				
			}

			await sleep(0);
		}
	}
}

