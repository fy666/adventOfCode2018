const fs = require('fs')
/* FFT */

function *  patternGenerator(iter) {
const pattern = [0,1,0,-1]
let index = 0
let iterCount = 0
let firstIter = 1
//console.log("Calling pattern with iter = " + iter)
if(iter == 1 )
{
    while (true){
        index++
        yield pattern[index%4]
    }
}
else {
    while (true) {
    //    console.log("index : " + index + " iterCount : " + iterCount)
        yield pattern[index%4]
        iterCount = (++iterCount)%(iter-firstIter)
        if(iterCount == 0){index +=1; firstIter = 0;}
        }
    }
}

function fftAdvent(numbers,ix){
    const gen = patternGenerator(ix+1)
    let result = 0
    numbers.forEach(item => result += gen.next().value * item)
    return Math.abs(result%10)
}

function fftApplyOnePhase(numbers){
    result = []
    numbers.forEach( (item,ix) => {
        result.push(fftAdvent(numbers,ix))
    }
    )
    return result
}


function firstPuzzle(number,phase){

    let newNumber = number.split("").map(x => parseInt(x) )
    for(let j = 0; j < phase;j++){
        newNumber = fftApplyOnePhase(newNumber)
        //console.log("New " + newNumber.join(""))
    }
    console.log("Afer " + phase + " iterations : " + newNumber.join(""))
    console.log(newNumber.slice(0, 8).join(""))
}

function secondPuzzle(number){
    let phase = 100
    let smallNumber = number.split("").map(x => parseInt(x))
    let wantedPos = parseInt(smallNumber.slice(0,7).join(""))
    console.log("size of input : " + (smallNumber.length * 10000) + ", wanted position : "+ wantedPos)

    if(wantedPos > smallNumber.length * 10000/2){
        console.log("Luckily wanted position after N/2 !")
        let input = [].concat(...Array(10000).fill(smallNumber))
        let reducedList = input.slice(wantedPos).reverse() // only take tail of input and reverse
        // cum sum for every phase
        //const cumulativeSum = (sum => value => sum += value)(0);
        //console.log("reducedList before" + reducedList.slice(0,7).join(""))
        for(let j = 0; j < phase;j++){
            const cumulativeSum = (sum => value => sum = (sum+value)%10)(0);
            reducedList = reducedList.map(cumulativeSum)
        }
        //console.log("reducedList " + reducedList.slice(0,7).join(""))
        console.log("result is " + reducedList.reverse().slice(0,8).join(""))

    }
    else {
        console.log("No trick yet...")
        return
    }
}


//firstPuzzle(12345678,4)
let dataN = '80871224585914546619083218645595'
//[8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5]

let dataS = '59790132880344516900093091154955597199863490073342910249565395038806135885706290664499164028251508292041959926849162473699550018653393834944216172810195882161876866188294352485183178740261279280213486011018791012560046012995409807741782162189252951939029564062935408459914894373210511494699108265315264830173403743547300700976944780004513514866386570658448247527151658945604790687693036691590606045331434271899594734825392560698221510565391059565109571638751133487824774572142934078485772422422132834305704887084146829228294925039109858598295988853017494057928948890390543290199918610303090142501490713145935617325806587528883833726972378426243439037'
//console.log("input size is " + dataS.length)
//return
let data2='203036732577212944063491565474664'
data2= '03036732577212944063491565474664'
//firstPuzzle(dataS,100)
secondPuzzle(dataS)
return

let data = fs.readFileSync('day16.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
console.log("First Puzzle")

firstPuzzle(193651,649729)
secondPuzzle(193651,649729)
