const fs = require('fs')
const Combinatorics = require('js-combinatorics');
// npm i js-combinatorics

function getFunctionParam(immediate)
{
    if(immediate){
        return (array,index) => { return array[index]}
    }
    else {
        return (array,index) => { return array[array[index]]}
    }
}

function operation(num, input){
    let fun;
    let step;
    let getVar1;
    let getVar2;

    getVar1 = getFunctionParam(Math.floor(num/100 %10))
    getVar2 = getFunctionParam(Math.floor(num/1000 %10))
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
        fun = (array,index) => { return input}
        mess = "input"
    }
    else if(num%100 == 4){ // ouput
        fun = (array, index) => {
            return getVar1(array,index+1)
            }
        step = 2
        store = false
        mess = "output"
    }
    else if(num%100 ==5){
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

    return {'step':step, 'getVar1':getVar1, 'getVar2':getVar2, 'fun':fun, 'store':store, 'message':mess, 'stepF':stepF}
}

class Amplifiers {
  constructor(array, phase) {
    this.phase = phase;
    this.index = 0;
    this.program = array.slice(0)
  }
  run(input){
     // console.log("Running ampli at index " + this.index + " with input " + input)
    while (this.program[this.index] != 99 && this.index < this.program.length) {
        let instruction = operation(this.program[this.index], this.index === 0 ? this.phase : input)
        let res = instruction.fun(this.program, this.index)
        if(instruction.store){
            this.program[this.program[this.index+instruction.step-1]] = res
        }
        if(instruction.stepF){
            this.index = instruction.stepF(this.program,this.index)
        }
        else {
            this.index += instruction.step
        }
        if(instruction.message  === "output"){
            return res
        }
    }
    return false
  }
}

class FeedBackLoop {
    constructor(array, phases){
        this.amplifiers = []
        for(let i of phases){
            this.amplifiers.push(new Amplifiers(array.slice(0), i))
        }
        this.finalAmplification = 0
    }

    run(value){
        let input = value
        for(let ampli of this.amplifiers){
            input = ampli.run(input)
        }
        return input
    }
}



function IncodeComputer(array, input, phase){
let index = 0
while (array[index] != 99 && index < array.length){
    let instruction = operation(array[index], index === 0 ? phase : input)
    let res = instruction.fun(array, index)
    if(instruction.message  === "output"){
        return res
    }
        if(instruction.store){
            array[array[index+instruction.step-1]] = res
        }
    if(instruction.stepF){
        index = instruction.stepF(array,index)
    }
    else{
        index += instruction.step
        }
    }
}

function runAmplifiers(array,phases){
    let input = 0
    for(let i of phases){
        input = IncodeComputer(array.slice(0), input, i)
    }
    return input
}

function runAmplifiersFeedbackLoop(array,phases){
    let loop = new FeedBackLoop (array, phases)
    let result = 0
    let lastResult = 0
    while (result = loop.run(lastResult)){
        lastResult = result
    }
    return lastResult
}

function firstPuzzle(array){

    cmb = Combinatorics.permutation([0,1,2,3,4], 5);
    let  maxAmp = 0
    let winnerInput = []
    while ( a  = cmb.next()){
        //console.log(a)
        let res = runAmplifiers(array.slice(0), a)
        if(res > maxAmp){
            winnerInput = a.slice(0)
            maxAmp = res
        }
    }
    console.log("Max ampli is " + maxAmp +  " with input " + winnerInput)
    return
    let res = runAmplifiers(array.slice(0), [0,1,2,3,4])
    //[4,3,2,1,0])
}


function secondPuzzle(array){
    cmb = Combinatorics.permutation([9,8,7,6,5], 5);
    let  maxAmp = 0
    let winnerInput = []
    while ( a  = cmb.next()){
        //console.log(a)
        let res = runAmplifiersFeedbackLoop(array,a)
        if(res > maxAmp){
            winnerInput = a.slice(0)
            maxAmp = res
        }
    }
    console.log("Max ampli is " + maxAmp +  " with input " + winnerInput)
    return
    //console.log("Amplification " + runAmplifiersFeedbackLoop(array,phases))
}


let example = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
example = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
example = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
//console.log("Test")
//firstPuzzle(example)
//secondPuzzle(example)
//return


let data = fs.readFileSync('day7.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
//console.log(data)
console.log("First Puzzle")
firstPuzzle(data.slice(0))
console.log("Second Puzzle")
secondPuzzle(data.slice(0))
/*
console.log("Second")
firstPuzzle(data.slice(0),5)
*/
