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
        fun = (array,index) => {return input}
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

function IncodeComputer(array, input){
    let index = 0
    let base = 0
    while (array[index] != 99 && index < array.length){
        let instruction = operation(array[index], input, base)
        let res = instruction.fun(array, index)
        if(instruction.message  === "output"){
            console.log("output " + res)
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

class PaintingRobot {
  constructor(array) {
    this.directions = [];
    this.directions.push( (item) => {item.x+=1; return item}) // x+=1
    this.directions.push( (item) => {item.y-=1; return item})
    this.directions.push( (item) => {item.x-=1; return item})
    this.directions.push( (item) => {item.y+=1; return item})
    this.direction = 3
    this.trace = [];
    this.program = array.slice(0)
	this.index = 0
	this.trace.push({'x':0, 'y':0, 'color':0, 'painted':false})
    this.base = 0
    this.paintedFaces = 0
	// 0 : black
	// 1 : white
  }

  move(){
      let newPos = Object.assign({},this.trace[this.trace.length - 1])
      newPos = this.directions[this.direction](newPos)
      let doubles = this.trace.filter((item) => (newPos.x == item.x && newPos.y == item.y))
      if(doubles.length > 0){
          console.log("already passed")
          newPos.color = doubles[doubles.length - 1].color
          newPos.painted = doubles[doubles.length - 1].painted
          /*
          if(!doubles[doubles.length-1].painted){
              this.paintedFaces +=1
          }*/
      }
      else {
          newPos.color = 0
          newPos.painted = false
         // this.paintedFaces +=1
      }

    //  console.log("new pos" + newPos)
      this.trace.push(newPos)
  }

  runNext(input){
	let color;
	let dir;
    while (this.program[this.index] != 99 && this.index < this.program.length) {
        let instruction = operation(this.program[this.index], input, this.base)
        let res = instruction.fun(this.program, this.index)
        if(instruction.message  === "output"){
            if(color === undefined){
                 color = res
             }
             else if(dir === undefined) {
                 dir = res;
                 return {"color":color, "dir":dir}
             }
        }
        if(instruction.store){
            this.program[this.program[this.index+instruction.step-1]+instruction.stepRes] = res
        }
        if(instruction.message == "base"){
            this.base = res
        }
        if(instruction.stepF){
            this.index = instruction.stepF(this.program, this.index)
        }
        else {
            this.index += instruction.step
        }
    }
    return
  }

 run(){
    let res
    let count = 0
    while( (res =  this.runNext(this.trace[this.trace.length -1].color)) ){
        if(this.trace[this.trace.length-1].painted == false){
            this.trace[this.trace.length-1].painted = true
            this.paintedFaces +=1
        }
        this.trace[this.trace.length-1].color = res.color

    //    console.log("new color " + res.color + " new Dir " + res.dir)
    //    console.log(this.trace[this.trace.length-1])
    console.log("New command " + res.color + "," + res.dir)
        if(res.dir == 0){
            if(this.direction == 0 ){
                this.direction = 3
            }
            else {
                this.direction = (this.direction-1)%4
            }
        }
        else {
            this.direction = (this.direction+1)%4
        }
        this.move()
        console.log(this.trace)
        count +=1
        if(count > 20){console.log(this.paintedFaces);
            return}
//        console.log('last color ' + this.trace[this.trace.length -1].color)
        //newColor, newDir = this.runNext(this.trace[this.trace.length -1].color)
    }
    this.trace.pop()
    let yoco = 0
    console.log( this.trace.length + " moves")
    console.log(this.paintedFaces + " painted")
    return
    this.trace.forEach(item => {
        if(this.trace.filter( (otherItem) => {
            return (otherItem.x == item.x && otherItem.y == item.y)
        }).length === 1){
            yoco +=1
        }
    })
    console.log("Different objects " + yoco)
}
}


function firstPuzzle(array){
    let robby = new PaintingRobot(array)
    robby.run()

}


function secondPuzzle(array){
    let res = IncodeComputer(array, 2)
    return

}

let data = fs.readFileSync('day11.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
console.log("First Puzzle")
firstPuzzle(data.slice(0))
return
//console.log("Second Puzzle")
//secondPuzzle(data.slice(0))
/*
console.log("Second")
firstPuzzle(data.slice(0),5)
*/
