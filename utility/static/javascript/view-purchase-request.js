const dummy=document.querySelector('.dummy');
// dummy.style.display='none';
dummy.lastElementChild.style.color='rgb(230,190,105)';
dummy.lastElementChild.style.backgroundColor='rgb(15,80,96)';
const button1=document.querySelector('#button1');
const button2=document.querySelector('#button2');
button2.style.backgroundColor='rgb(15,80,96)';
button2.style.color='white';
button1.style.backgroundColor='white';
const stats=document.querySelector('#stats')
stats.style.display='none';
button1.addEventListener('click',function(){
	dummy.style.display='none';
	stats.style.display='block';
	button1.style.backgroundColor='rgb(15,80,96)';
	button1.style.color='white';
	button2.style.backgroundColor='white';
	button2.style.color='black';
})
button2.addEventListener('click',function(){
	stats.style.display='none';
	dummy.style.display='block';
	button2.style.backgroundColor='rgb(15,80,96)';
	button2.style.color='white';
	button1.style.backgroundColor='white';
	button1.style.color='black';
})
// const bars=document.querySelectorAll('.bar');
// const barNames=document.querySelectorAll('.barNames')
// const numbers=[];
// depNames.map(function(depName){
	// return depName.lastElementChild.textContent
// })
// }
