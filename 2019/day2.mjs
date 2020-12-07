import fs from "fs"

function firstPuzzle(array){
let index = 0
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
console.log("First puzzle = " + array[0])
}

function compute(val)
{
    return Math.floor(val/3)-2
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


let example = [2,3,0,3,99,2,4,4,5,99,0,1,1,1,4,99,5,6,0,99]
example = [2,4,4,5,99,0]
example = [1,1,1,4,99,5,6,0,99]
console.log("Test")
firstPuzzle(example)
let data = fs.readFileSync('day2.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
data[1] = 12
data[2] = 2
console.log("First")
firstPuzzle(data.slice(0))

for (let noun = 0; noun < 100 ; noun ++) {
    for (let verb = 0; verb < 100 ; verb++ ){
    data[1] = noun
    data[2] = verb
    let a = secondPuzzle(data)
    if(a == 19690720){
        console.log("Second puzzle")
        console.log("Noun : " + noun + ", verb : " + verb + ", result : " + (100*noun+verb))
        break
        }
    }
}

