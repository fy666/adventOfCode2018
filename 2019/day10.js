const fs = require('fs')

function createAsteroids(data){
    let asteroids = []
    data.forEach( (line,iy) => {
        line.forEach( (item,ix) => {
            if(item === "#"){
                asteroids.push({'x':ix, 'y': iy})
            }
        })
    })
    return asteroids
}


function getDirection (a, b){ // angle between 2 points
    let dir = Math.atan2((b.y - a.y), -(b.x - a.x))
    return dir
}

function getRelativePos(a,b){
    let ang = getDirection(a,b)
    ang = ang > 0 ? ang : ang + 2*Math.PI
    ang = ang - Math.PI/2
    ang = ang > 0 ? ang : ang + 2*Math.PI
    if(ang == 0){
        ang = 2*Math.PI
    }
    ang = ang > 0 ? ang : ang + 2*Math.PI
    let r = (b.y - a.y)**2 + (b.x - a.x)**2 // dx^2 + dy^2
    return [ang , r]
}

function computeAllPositionsFrom(asteroid, asteroids)
{
    asteroids.filter(item => item !== asteroid).map( item => {
            let pos = (getRelativePos(item,asteroid))
            item['angle']=pos[0]
            item['range']=pos[1]
            }
            )
}

function numberOfDetections(asteroid, asteroids)
{
    let allDirections = []
    asteroids.filter(item => item !== asteroid).forEach( item => allDirections.push(getDirection(asteroid,item)))
    return (new Set(allDirections)).size
}


function firstPuzzle(asteroids){

    asteroids.map( item => item["detections"] = numberOfDetections(item, asteroids))
    let maxD = {'x':0, 'y':0, 'detections':0}
    asteroids.forEach(item => {
        if(item.detections > maxD.detections){
            maxD = item
        }
    } )
    console.log("Max detections ")
    console.log(maxD)
}


function secondPuzzle(asteroids){
    let winner={}
    let index
    asteroids.forEach(item => {
        if(item.x == 28 && item.y == 29)
        {winner = item}
    })
    winner['range'] = 0
    winner['angle'] = 0
    computeAllPositionsFrom(winner, asteroids)
    
    asteroids.map(item => {
        let f = asteroids.filter(x => x.angle == item.angle)
        f.sort((a,b) => { 
            if(a.range > b.range){
                return 1
            }
            else if (a.range < b.range){
                return -1
            }
            return 0
        })
        item["rep"] = f.indexOf(item)
    })
    asteroids.sort((a,b) => {
        if(a.rep > b.rep) {return 1}
        if(a.rep < b.rep) {return -1}
        if(a.angle > b.angle){return -1}
        if(a.angle < b.angle){return 1}
        if(a.range > b.range){return 1}
        return -1
    })
    let wanted = asteroids.filter(item => item !== winner)[199]
    console.log(wanted)
    console.log(wanted.x*100 + wanted.y)
}

let data = fs.readFileSync('day10.txt', 'utf8').split('\n')
data = data.map(item => item.split(''))
firstPuzzle(createAsteroids(data))
secondPuzzle(createAsteroids(data))
    return
