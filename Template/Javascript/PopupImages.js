var ModalInnerHTML = `
  <span class=\"close\">&times;</span>
  <img class=\"modal-image\" >
`;

window.addEventListener('load', function () {
	var elements = document.querySelectorAll('img.PopupImage');
	if(elements.length != 0){
		for (var e = 0; e < elements.length; e++) {
			var element = elements[e];

			var newModal = document.createElement('div');
			newModal.setAttribute('class', 'modal');
			newModal.innerHTML = ModalInnerHTML;
			newModal.querySelector("img").src = element.src.replace("-small","");


			element.onclick = function(){
			  this.parentNode.querySelector(".modal").style.display = "block";
			};

			var close = newModal.querySelector("span.close");

			close.onclick = function() {
			  this.parentNode.style.display = "none";
			}

			element.parentNode.appendChild(newModal);
		}
		console.log("Added Image Popup Events to " + elements.length + " elements");
	}


});