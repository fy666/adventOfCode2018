const fs = require('fs')

function getFunctionParam(immediate, base)
{
    if(immediate == 1){ // immediate position
        return (array,index) => { return (array[index]? array[index] : 0) }
    }
    else if (immediate == 0) { // relative position
        return (array,index) => { return (array[array[index]]? array[array[index]] : 0)}
    }
    else if (immediate == 2){
        return (array, index) => {return (array[array[index]+base]? array[array[index]+base] : 0)}

    }
}

function operation(num, input, base){
    let fun;
    let step;
    let getVar1;
    let getVar2;

    getVar1 = getFunctionParam(Math.floor(num/100 %10), base)
    getVar2 = getFunctionParam(Math.floor(num/1000 %10), base) 
    let stepRes = (Math.floor(num/10000%10) === 2)? base : 0
    let store = true
    let mess
    let stepF

    if(num%100 == 1){ // addition
        step = 4
        fun = (array,index) => getVar1(array,index+1) + getVar2(array,index+2)
        mess = "addition"
    }
    else if (num%100 == 2){ // multiplication
        fun = (array,index) => getVar1(array,index+1) * getVar2(array,index+2)
        step = 4
        mess = "multi"
    }
    else if(num%100 == 3){ // input
        step = 2
        fun = (array,index) => {console.log("input = " + input); return input}
        mess = "input"
        stepRes=(Math.floor(num/100 % 10) === 2)? base : 0
    }
    else if(num%100 == 4){ // ouput
        fun = (array, index) => {
            return getVar1(array,index+1)
            }
        step = 2
        store = false
        mess = "output"
    }
    else if(num%100 ==5) {
        mess = 'jump if true'
        store = false
        fun = (array, number) => {}
        step = 0
        stepF = (array,index) => {
            if(getVar1(array,index+1)){
                return getVar2(array,index+2)
            }
            else
                return index+3
        }
    }
    else if(num%100 == 6){
        mess = "jump if false"
        store = false
        fun = (array, index) => {}
        step = 0
        stepF = (array,index) => {
            if(!getVar1(array,index+1)){
                return getVar2(array,index+2)
            }
            else
                return index+3
        }
    }
    else if(num%100 ==7){
        mess = "less than"
        fun = (array,index) => Number(getVar1(array,index+1) < getVar2(array,index+2))
        step = 4
    }
    else if(num%100 == 8){
        mess = "equals"
        fun = (array,index) => Number(getVar1(array,index+1) == getVar2(array,index+2))
        step = 4
    }
    else if(num%100 == 9){
        mess = "base"
        fun = (array,index) => {
            return(base + Number(getVar1(array,index+1)))
        }
        step = 2
        store = false
    }
    return {'step':step, 'getVar1':getVar1, 'getVar2':getVar2, 'fun':fun, 'store':store, 'message':mess, 'stepF':stepF, 'stepRes':stepRes}
}

function interpretGame(array){
	let points=[]
	while(array.length) { 
		points.push(array.splice(0,3));
	}
	let elements=[]
	for(let item of points){
		elements.push({'x':item[0],'y':item[1],'id':item[2]})
	}
	//console.log(elements)
	console.log(" block tiles : " + elements.filter( item => item.id == 2).length)
	let width = 0
	elements.forEach( item => {if (item.x > width ){width = item.x}})
	let height = 0
	elements.forEach( item => {if (item.y > height ){height = item.y}})
	width +=1
	height+=1
	console.log("Screen size : " + width + "," + height)
	console.log("paddle at ")
	console.log(elements.filter(item => item.id == 3))
	console.log("ball at ")
	console.log(elements.filter(item => item.id == 4))
	let gameMat = Array(height).fill().map(() => Array(width).fill(""));
	//console.log(gameMat)
//	let gameMat = []
	//draw(gameMat)
	console.log(gameMat.length)
	for(item of elements){
		gameMat[item.y][item.x] = elementToString(item.id)
	}
draw(gameMat)
	//console.log(gameMat)
}

function draw(gameMat){
	for(let line of gameMat){
		console.log(line.join(""))
	}

}

function elementToString(elem){
	if(elem == 0)
		return " "
	if(elem == 1)
		return "-"
	if(elem == 2)
		return "x"
	if(elem == 3)
		return "_"
	if(elem == 4)
		return ("o")
}

function interpretInput(item){
		if (item[0] == -1){
			return {'score': item[2]}
		}
		else {
			return {'x':item[0],'y':item[1],'id':item[2], 'st': elementToString(item[2]) } 
		}
}

function IncodeComputer(array, input){
    let index = 0
    let base = 0
	let point = []
	let num_res = 0
	let frame = []
    while (array[index] != 99 && index < array.length){
        let instruction = operation(array[index], input, base)
        let res = instruction.fun(array, index)
        if(instruction.message  === "output"){
			point.push(res)
			if(point.length == 3){
				frame.push(interpretInput(point))
                point=point.slice(3)
				if(frame[frame.length-1].score !== undefined){
                    return frame
                }
			}	
        }
            if(instruction.store){
                array[array[index+instruction.step-1]+instruction.stepRes] = res
            }
            if(instruction.message == "base"){
                base = res
            }
        if(instruction.stepF){
            index = instruction.stepF(array,index)
        }
        else{
            index += instruction.step
            }
        }
}

function firstPuzzle(array){

    let res = IncodeComputer(array, 1)
//	console.log("outputs " + res)	
	interpretGame(res)
   
}


function secondPuzzle(array){
    let elements = IncodeComputer(array, 1)
    let width = 0
	elements.forEach( item => {if (item.x > width ){width = item.x}})
	let height = 0
	elements.forEach( item => {if (item.y > height ){height = item.y}})
	width +=1
	height+=1
	console.log("Screen size : " + width + "," + height)
	console.log("paddle at ")
	console.log(elements.filter(item => item.id == 3))
	console.log("ball at ")
	console.log(elements.filter(item => item.id == 4))
	let gameMat = Array(height).fill().map(() => Array(width).fill(""));
	console.log(gameMat.length)
	for(item of elements){
        if(item.score == undefined){
		gameMat[item.y][item.x] = item.st        
    	}
    }
   draw(gameMat)
}


let data = fs.readFileSync('day13.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
/*
console.log("First Puzzle")
firstPuzzle(data.slice(0))
 return
*/
console.log("Second Puzzle")
let data2 = data.slice(0)
data2[0] = 2
secondPuzzle(data2)
/*
console.log("Second")
firstPuzzle(data.slice(0),5)
*/
