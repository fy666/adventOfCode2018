const fs = require('fs')

function getColor(layer){
    // 0 : black
    // 1 : white
    // 2 : transparent
    return (layer.filter(item => item != 2)[0])

}

function firstPuzzle(layers){
    let minZeroes = 25*6
    let layer = []
    let currentCount = 0
    for (item of layers){
        if( (currentCount = item.filter(item => item === 0).length) < minZeroes) {
            minZeroes = currentCount
            layer = item
        }
    }
    console.log("Min Zeroes " + minZeroes)
    console.log("Count is " + layer.filter(item => item === 1).length * layer.filter(item => item === 2).length)
}


function secondPuzzle(layers){
    let decodedImage = []
    console.log("Length of layers " + layers[0].length)
    for(let i = 0 ; i < layers[0].length ; i ++){
        decodedImage.push(getColor(layers.map(item => item[i])))
    }

    let squareImage = []
    while(decodedImage.length) squareImage.push(decodedImage.splice(0,25));
    console.log(decodedImage)
    for (elem of squareImage) {
        console.log(elem.toString())
    }
    //console.log(squareImage)

}

let data = fs.readFileSync('day8.txt', 'utf8').split('\n')
data = data[0].split('').map(e => parseInt(e,10))

let layers = [];
while(data.length) layers.push(data.splice(0,25*6));
console.log(layers.length + " layers")

console.log("Second Puzzle")
secondPuzzle(layers)

console.log("First Puzzle")
firstPuzzle(layers)
