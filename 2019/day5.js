const fs = require('fs')

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
        fun = (array,index) => {return input}
        mess = "input"
    }
    else if(num%100 == 4){ // ouput
        fun = (array, index) => console.log("output is"   + getVar1(array,index+1))
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

function firstPuzzle(array,input){
let index = 0
while (array[index] != 99 && index < array.length){
    let instruction = operation(array[index],input)
    let res = instruction.fun(array, index)
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
console.log("First puzzle = " + array[0])
}


function secondPuzzle(array1){
let index = 0
let array = array1.slice(0)
while (array[index] != 99 && index < array.length){
    if(array[index] == 1 || array[index] == 2)
    {
        let var1 = array[array[index+1]]
        let var2 = array[array[index+2]]
        let res = var1*var2
        if (array[index] == 1){
         res = var1 + var2
         }
        array[array[index+3]] = res
    }
    index = index + 4
}
return array[0]
}


let example = [1101,100,-1,4,0]
example = [3,0,4,0,99]
example = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
example = [3,3,1108,-1,8,3,4,3,99]
console.log("Test")
firstPuzzle(example,8)

let data = fs.readFileSync('day5.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
console.log("First")
firstPuzzle(data.slice(0), 1)
console.log("Second")
firstPuzzle(data.slice(0),5)
