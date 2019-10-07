let index=14;
const table=document.querySelector('.inputTable').lastElementChild
const add=document.querySelector('#add');
const total=document.querySelector('#total').lastElementChild;
total.value=0;
add.addEventListener('click',function(){
	tr=document.createElement('tr'); 
	tr.innerHTML=table.lastElementChild.innerHTML;
	table.appendChild(tr);
	const tds=tr.children;
	for(let i=1;i<5;i++){
		tds[i].lastElementChild.name=index;
		index++;
		tds[i].lastElementChild.value=0;
	}
	tds[0].textContent=(index-10)/4;
})
const validate=function(){
	document.getElementsByName('count')[0].value=(index-10)/4;
	let val=0;
	for(let i=13;i<index;i+=4){
		const n=document.getElementsByName(i)[0].value;
		val+=parseInt(n);
	}
	total.value=val;
}