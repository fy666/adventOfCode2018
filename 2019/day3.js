const fs = require('fs')

function isInside(lim1, lim2, num)
{
    if(lim1 > lim2){
        return num >= lim2 && num <= lim1
    }
    else {
        return num >= lim1 && num <= lim2
    }
}

function intersect(seg1 , seg2){
    if(seg1.dir === seg2.dir){
        return false
    }
    let intersect = {}
    intersect[seg1.dir] = seg1[seg1.dir] 
    intersect[seg2.dir] = seg2[seg2.dir] // will define x1 and y1

    if (isInside(seg1.x1,seg1.x2,intersect.x1) && 
            isInside(seg1.y1, seg1.y2, intersect.y1) &&
            isInside(seg2.x1, seg2.x2, intersect.x1) &&
            isInside(seg2.y1, seg2.y2, intersect.y1)){
        let steps = Math.abs(intersect.y1 - seg2.y1) + Math.abs(intersect.x1 - seg2.x1)
            + Math.abs(intersect.y1 - seg1.y1) + Math.abs(intersect.x1 - seg1.x1)
        intersect.steps = steps
        return intersect
    }
    else {
        return false
        }
}

function getPath(array)
{
    let reg =  new RegExp('([URLD])([0-9]*)')
    let result = []
    result.push({'x1' : 0 , 'y1': 0, 'x2':0 , 'y2' : 0, 'dir':"x1", "steps":0}) // list of segments
    for(const arr of array){
        let nextPosition = [] //Object.assign({},result.slice(0)[result.length-1])i
        let lastPosition = result[result.length -1]    
        let action = reg.exec(arr)
        let steps = parseInt(action[2],10)
        nextPosition.x1 = lastPosition.x2
        nextPosition.y1 = lastPosition.y2
        nextPosition.x2 = nextPosition.x1
        nextPosition.y2 = nextPosition.y1
        nextPosition.steps = lastPosition.steps + steps
        nextPosition.lastSteps = lastPosition.steps
        if(action[1] == 'R'){
            nextPosition.x2 = nextPosition.x1 + steps
            nextPosition.dir = "y1"
        }
        else if (action[1] == 'L'){
            nextPosition.x2 = nextPosition.x1 - steps
            nextPosition.dir="y1"
        }
        else if (action[1] == 'D'){
            nextPosition.y2 = nextPosition.y1 - steps
            nextPosition.dir = "x1"
        }
        else if (action[1] == 'U'){
            nextPosition.y2 = nextPosition.y1 + steps
            nextPosition.dir = "x1"
        } 
        result.push(Object.assign({},nextPosition))
    }
    result.shift()
    return result
}

function firstPuzzle(array){
    let path1 = getPath(array[0])
    let path2 = getPath(array[1])
    let commonPoints = []
    let distances = []
    let steps = []
    path1.forEach((seg1,ix1) =>{
        path2.forEach((seg2,ix2) =>{
            let point = []
                if(point = intersect(seg1,seg2)){
                    commonPoints.push(point)
                    distances.push(Math.abs(point.x1) + Math.abs(point.y1))
                    steps.push(seg1.lastSteps + seg2.lastSteps + point.steps)
                }
                })
    })
    distances.shift()
    steps.shift()
   console.log("min distance " + Math.min(...distances))
   console.log("min steps " + Math.min(...steps))
   return
console.log('path 1')
   for(const item of path1){
        console.log(item)
    }
console.log("path2")
   for(const item of path2){
        console.log(item)
    }
console.log("intersec")
    for(const item of commonPoints){
        console.log(item)
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


//let example = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],['U62','R66','U55','R34','D71','R55','D58','R83']]
let example = [['R8','U5','L5','D3'],['U7','R6','D4','L4']]
firstPuzzle(example)
let data = fs.readFileSync('day3.txt', 'utf8').split('\n')
let input = data[0].split(',')
let input2 = data[1].split(',')
firstPuzzle([input, input2])
