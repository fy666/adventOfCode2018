const fs = require('fs')
const Combinatorics = require('js-combinatorics');
// npm i js-combinatorics

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
        //    console.dir(array.slice(0,100))
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

    let res = IncodeComputer(array, 1)
    return
}


function secondPuzzle(array){
    let res = IncodeComputer(array, 2)
    return

}


let example = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
example = [104,1125899906842624,99]
example = [109, 3, 21101, 4, 3, 12 ,204,13,99]
//example = [1102,34915192,34915192,7,4,7,99,0]
for (let i = 0; i < 0 ; i++){
    example.push(0)
    }
console.log("Test")
//firstPuzzle(example)
//secondPuzzle(example)
//return


let data = fs.readFileSync('day9.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
console.log("First Puzzle")
console.log("Length " + data.length)
//firstPuzzle(data.slice(0))
//  return
console.log("Second Puzzle")
secondPuzzle(data.slice(0))
/*
console.log("Second")
firstPuzzle(data.slice(0),5)
*/
