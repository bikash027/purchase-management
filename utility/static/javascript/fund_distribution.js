const hiddenTrs=document.querySelector('#hiddenTable').lastElementChild.children;
	const newTable=document.querySelector('#newTable').lastElementChild;
	const findSum=function(){
		const inp_values=newTable.children;
		let sum=0;
		for(let i=1;i<inp_values.length;i++){
			let x=inp_values[i].lastElementChild.previousElementSibling.lastElementChild.value;
			x+='';
			x=parseInt(x);
			sum+=x;
		}
		const remain=inp_values[0].lastElementChild.previousElementSibling;
		const y=(sum<total)?total-sum:0;
		remain.textContent=y;
		const ratio=(y>total)?1:(y/total);
		inp_values[0].lastElementChild.lastElementChild.style.width=(100*ratio)+'%';
	}
	const showlimit=function(tr){
		const inp_values=newTable.children;
		let sum=0;
		for(let i=1;i<inp_values.length;i++){
			if(tr===inp_values[i])
				continue;
			let x=inp_values[i].lastElementChild.previousElementSibling.lastElementChild.value;
			x+='';
			x=parseInt(x);
			sum+=x;
		}
		const remain=inp_values[0].lastElementChild.previousElementSibling;
		const y=(sum<total)?total-sum:0;
		const limit=tr.lastElementChild.lastElementChild
		limit.style.display='block';
		const ratio=(y>total)?1:(y/total);
		limit.style.left=(100*ratio)+'%';
		limit.ratio=ratio;
	}
	const adjustLength=function(i,div2,inp){
		hiddenTrs[i+1].lastElementChild.lastElementChild.value=inp.value;
		const ratio=(inp.value>total)?1:((inp.value)/total);
		div2.style.width=(100*ratio)+'%';
		const sum=findSum();
	}
	const th=document.createElement('tr');
	newTable.appendChild(th);
	const th1=document.createElement('td');
	th.appendChild(th1);
	th1.textContent='fund remaining';
	const th2=document.createElement('td');
	th.appendChild(th2);
	th2.textContent=document.querySelector('span').textContent;
	const total=parseInt(th2.textContent);
	const th3=document.createElement('td');
	th.appendChild(th3);
	const div=document.createElement('div');
	th3.appendChild(div);
	
	// th1.style.height='50px';
	th1.style.width='8vw';
	th2.style.width='8vw';
	th3.style.width='64vw';
	div.style.height='80px';
	div.style.width='inherit';
	div.style.backgroundColor='rgb(209,209,77)';

	for(let i=0;i<hiddenTrs.length;i+=2){
		const tr=document.createElement('tr');
		newTable.appendChild(tr);
		const td1=document.createElement('td');
		tr.appendChild(td1);
		const td2=document.createElement('td');
		tr.appendChild(td2);
		const td3=document.createElement('td');
		tr.appendChild(td3);
		const div2=document.createElement('div');
		td3.appendChild(div2);
		div2.style.height='inherit';
		div2.style.width='0';
		div2.style.backgroundColor='rgb(209,209,77)';
		td3.style.height='50px';
		const div3=document.createElement('div');
		td3.appendChild(div3);


		div3.style.width='10px';
		div3.style.height='50px';
		td3.style.position='relative';
		div3.style.position='absolute';
		div3.style.top='0';
		div3.style.backgroundColor='red';
		div3.style.display='none';

		td1.textContent=hiddenTrs[i].lastElementChild.lastElementChild.value;
		const inp=document.createElement('input');
		inp.type='number';
		inp.value=0;
		td2.appendChild(inp);
		inp.addEventListener('change',function(){
			adjustLength(i,div2,inp);
		});
		td3.addEventListener('click',function(e){
			const max_width=parseFloat(window.getComputedStyle(td3).width);
			inp.value=Math.floor((e.offsetX/max_width)*total);
			adjustLength(i,div2,inp);
		})
		td3.addEventListener('mouseenter',function(){
			showlimit(tr);
		});
		td3.addEventListener('mouseleave',function(){
			div3.style.display='none';
		});
		div3.addEventListener('click',function(e){
			inp.value=Math.floor(parseFloat(div3.ratio)*total);
			adjustLength(i,div2,inp);
			e.stopPropagation();
		})
	}