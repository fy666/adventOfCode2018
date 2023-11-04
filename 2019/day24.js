const fs = require('fs')

const COL = 5

// generator to all adjacent positions
function *  adjacentPositionGenerator(ix) {
    let position = getMatrixPos(ix)
    //console.log("Treating tile " + position.x + "," + position.y)
    let indice
    const pattern = [1,0,-1]
    for(let i = 0; i < 3; i++){
        for(let j = 0; j < 3; j++){
            if( (pattern[j] != 0 || pattern[i] != 0) && (pattern[i]==0 || pattern[j]==0)) {
                // not itself + cross adjacent (must contain 0)
                //console.log(" i = " + i + ", j= " + j)
                if( (indice = getLinearPos(position.x+pattern[i], position.y+pattern[j])) != undefined)
                    yield indice
            }
        }
    }
    return
}


function getLinearPos(x,y){
    if(y >= COL || x < 0 || y < 0){
        return undefined
    }
    return (x * COL + y)
}

function getMatrixPos(ix){
    let x = Math.floor(ix/COL)
    let y = ix%COL
    return {'x':x,'y':y}
}

function update(mat, ix){
    // TO REDO !
    let gen = adjacentPositionGenerator(ix)
    let res
    let adjacentBugs = 0
    //console.log("At " + ix)
    while(!(res = gen.next()).done){
        console.log("check mat at pos " + res.value + " value is : " + mat[res.value])
        if(mat[res.value] == "#"){
            adjacentBugs++
        }
    }
    console.log("At " + ix + " " + adjacentBugs + " bugs")
    if(adjacentBugs == 1 && mat[ix] == "#"){ console.log("new val is ."); mat[ix] = "."; return}
    if( (adjacentBugs == 1 || adjacentBugs == 2) && mat[ix] == "."){ console.log("new val is #"); mat[ix] = "#";return}
    console.log("unchanged value ")
    return
}

function getNewValue(mat, ix){
    let gen = adjacentPositionGenerator(ix)
    let res
    let adjacentBugs = 0
    //console.log("At " + ix)
    while(!(res = gen.next()).done){
        //console.log("check mat at pos " + res.value + " value is : " + mat[res.value])
        if(mat[res.value] == "#"){
            adjacentBugs++
        }
    }
    //console.log("At " + ix + " " + adjacentBugs + " bugs")
    if(adjacentBugs == 1 && mat[ix] == "#"){ return "#"} // UNLESS
    if(mat[ix] == "#"){ return "."}

    if( (adjacentBugs == 1 || adjacentBugs == 2) && mat[ix] == "."){return "#"}
    return mat[ix]
}

function plotMat(mat){
    let ix = 0
    console.log("-------------")
    while(ix <= mat.length - COL){
        console.log(mat.slice(ix, ix + COL).join(""))
        ix += COL
    }
    console.log("-------------")
}

function getNewGrid(mat){
    let newMat = []
    mat.map((item,ix) => newMat.push(getNewValue(mat,ix)))
    return newMat
}

function arrayEquality(arr1, arr2){
    if(arr1.length != arr2.length){return false}
    for (let ix in arr1) {
        if(arr1[ix] != arr2[ix]){
            return false
        }
    }
    return true
}

function isInMatrix(mat, arr)
{
    for (let ix in mat) {
        if(arrayEquality(mat[ix], arr)){
            return true
        }
    }
    return false
}

function getBiodiversity(mat){
    let result = 0
    for (let ix in mat) {
        if(mat[ix] == "#"){
            result += 2**ix
        }
    }
    return result
}

function firstPuzzle(data){
    //plotMat(data)
    let allMat = [data]
    let sameNotFound = true
    let it = 0
    //plotMat(data)
    let newMat
    while(sameNotFound){
        //console.log("Start with")
        //plotMat(allMat[allMat.length-1])
        newMat = getNewGrid(allMat[allMat.length-1])
        //console.log("New : ")
        //plotMat(newMat)
        sameNotFound = !isInMatrix(allMat,newMat)
        //if(it ==2){
        //sameNotFound = false}
        allMat.push(newMat.slice())
        //console.log("Nex lenght " + allMat.length)
        it++
    }
    console.log("same mat found afer " + it + " iterations")
    plotMat(allMat[allMat.length-1])
    console.log("Biodiversity is " + getBiodiversity(allMat[allMat.length-1]))


    //let newMat = []
    //data.map((item,ix) => newMat.push(getNewValue(data,ix)))
    //plotMat(newMat)
}

function secondPuzzle(){
console.log("yo")
}


let data = '....##..#.#..##..#..#....'.split("")
data='##.#..##..##.#..#######..'.split("")

firstPuzzle(data)

return
/*
let data = fs.readFileSync('day16.txt', 'utf8').split('\n')
data = data[0].split(',').map(e => parseInt(e,10))
*/
