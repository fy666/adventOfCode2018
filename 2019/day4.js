
function checkIfNumbersIncrease(str){
    for(let c = 0; c < str.length-1; c++) 
    {
        if(str[c]>str[c+1]){
            return false;
        }
    }
    return true;
}


function checkIfRepeat(str){
    if(str.match(/(\d)\1+/g)){
        return true;
    }
    else {
        return false
    }
}

function checkIfRepeat2(str){
    let a
    if(a = str.match(/(\d)\1+/g)){
        for(let item of a){
            if(item.length == 2)
            {
            return true;
            }
        }
        return false;
    }
    else {
        return false
    }
}

function firstPuzzle(start, stop){
    let count = 0
    for(let i = start; i < stop; i++){
        let st = i.toString(10)
        if(checkIfRepeat(st) && checkIfNumbersIncrease(st)){
            count +=1
            console.log("found " + st)
        }
    }
    console.log("First puzzle = " + count)
}

function secondPuzzle(start,stop){
    let index = 0
    let count = 0
    for(let i = start; i < stop; i++){
        let st = i.toString(10)
        if(checkIfRepeat2(st) && checkIfNumbersIncrease(st)){
            count +=1
            console.log("found " + st)
         }
    }
    console.log("Second puzzle = " + count)
}


firstPuzzle(193651,649729)
secondPuzzle(193651,649729)
