const dummy=document.querySelector('.dummy');
		// dummy.style.display='none';
		dummy.lastElementChild.style.color='black';
		dummy.lastElementChild.style.backgroundColor='rgb(21,195,100)';
		const button1=document.querySelector('#button1');
		const button2=document.querySelector('#button2');
		button2.style.backgroundColor='rgb(21,195,100)';
		const stats=document.querySelector('#stats')
		stats.style.display='none';
		button1.addEventListener('click',function(){
			dummy.style.display='none';
			stats.style.display='block';
			button1.style.backgroundColor='rgb(21,195,100)';
			button2.style.backgroundColor='rgb(167,224,183)';
		})
		button2.addEventListener('click',function(){
			stats.style.display='none';
			dummy.style.display='block';
			button2.style.backgroundColor='rgb(21,195,100)';
			button1.style.backgroundColor='rgb(167,224,183)';
		})
		const bars=document.querySelectorAll('.bar');
		const depNames=document.querySelectorAll('.depNames')
		const numbers=[];
		// depNames.map(function(depName){
			// return depName.lastElementChild.textContent
		// })
		for(let i=0;i<3;i++){
			numbers.push(depNames[i].lastElementChild.lastElementChild.textContent);
			console.log(numbers[i]);
		}
		let max=0;
		for(let i=0;i<3;i++){
			numbers[i]=parseInt(numbers[i]);

			if(numbers[i]>max)
				max=numbers[i];
		}
		for(let i=0;i<3;i++){
			bars[i].style.height=300*(numbers[i]/max)+'px';
			bars[i].style.top=(400-300*(numbers[i]/max))+'px';
		}
		bars[0].style.backgroundColor='rgb(166,75,92)';
		bars[1].style.backgroundColor='rgb(209,209,77)';
		bars[2].style.backgroundColor='rgb(166,75,92)';