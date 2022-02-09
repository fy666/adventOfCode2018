// REPAIRING DOIDS
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

class Droid(){
    constructor(array){
        this.program = array
        this.index = 0
        this.base = 0
    }

    run(input){
        while (this.program[this.index] != 99 && this.index < this.program.length){
            let instruction = operation(this.program[this.index], input, base)
            let res = instruction.fun(this.program, this.index)
            if(instruction.message  === "output"){
    			return res
            }
                if(instruction.store){
                    this.program[this.program[this.index+instruction.step-1]+instruction.stepRes] = res
                }
                if(instruction.message == "base"){
                    this.base = res
                }
            if(instruction.stepF){
                this.index = instruction.stepF(this.program,this.index)
            }
            else{
                this.index += instruction.step
                }
            }
    }

    explore(){

    }
}


function firstPuzzle(array){
    let droid = new Droid(array)


}


function secondPuzzle(array){

}


let data = fs.readFileSync('day15.txt', 'utf8').split('\n')
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
