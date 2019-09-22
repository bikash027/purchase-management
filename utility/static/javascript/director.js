const bars=document.querySelectorAll('.bar');

const ins=document.querySelector('#in').children;

const bottom=document.querySelector('#bottom');

bars.forEach(function(bar){
	bar.style.top='75%';
	bar.style.height='25%';
	bar.addEventListener('mousedown',begin);
	bar.addEventListener('mousemove',drag);
	bar.addEventListener('mouseup',end);
	bar.active=false;
})

for(let i=0;i<4;i++){
	ins[i].value=parseFloat(bars[i].style.height);
}

function begin(e){
	e.target.active=true;
	e.target.current=e.clientY;
}
function drag(e){
	if(e.target.active){
		const displace=e.clientY-e.target.current;
		e.target.current=e.clientY;
		let str=parseFloat(e.target.style.top);
		str+=displace/5;
		let str2=100-str;
		str=str+'%';
		e.target.style.top=str;
		str2=str2+'%';
		e.target.style.height=str2;
		let sum=0;
		for(let i=0;i<4;i++){
			const height=parseFloat(bars[i].style.height);
			ins[i].value=height;
			sum+=height;
		}
		if(sum>100){
			bottom.style.backgroundColor='#a63f3f';
			bars.forEach(function(bar){
				bar.style.backgroundColor='#a63f3f';
			});
		}
		else if(bottom.style.backgroundColor=="rgb(166, 63, 63)"){
			bottom.style.backgroundColor='#21a649';
			bars.forEach(function(bar){
				bar.style.backgroundColor='#21a649';
			});
		}
	}
}
function end(e){
	e.target.active=false;
	
}

ins.forEach(function(inp){
	inp.addEventListener('change',change);
});

function change(e){

	for(let i=0;i<4;i++){
		let value=ins[i].value;
		bars[i].style.height=value+'%';
		value=100-parseFloat(value);
		bars[i].style.top=value+'%';
	}
	let sum=0;
	for(let i=0;i<4;i++){
		const height=parseFloat(bars[i].style.height);
		ins[i].value=height;
		sum+=height;
	}
	if(sum>100){
		bottom.style.backgroundColor='#a63f3f';
		bars.forEach(function(bar){
			bar.style.backgroundColor='#a63f3f';
		});
	}
	else if(bottom.style.backgroundColor=="rgb(166, 63, 63)"){
		bottom.style.backgroundColor='#21a649';
		bars.forEach(function(bar){
			bar.style.backgroundColor='#21a649';
		});
	}
}