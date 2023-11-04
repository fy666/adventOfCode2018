const fs = require('fs')

class Planet {
	constructor(position) {
		this.position = position
		this.speed =  {'x':0, 'y':0, 'z':0}
        this.x = [0]
        this.y = [0]
        this.z = [0]
        this.vx = [0]
        this.vy = [0]
        this.vz = [0]
	}

	applyGravity(otherPlanets) {
	otherPlanets.forEach( (item) => {
		for (let coord of ['x','y','z']){
			if(item.position[coord] > this.position[coord]){
					this.speed[coord]+=1
					item.speed[coord]-=1			
				}
			else if(item.position[coord] < this.position[coord]){
					this.speed[coord]-=1
					item.speed[coord]+=1
				}
			}
		})
	}
	
	applySpeed(){
		for (let coord of ['x','y','z']){
			this.position[coord] += this.speed[coord]
		}
	}

    checkDuplicates(){
        
    }

	printInfo(){
		console.log("pos = " + this.position.x + ","+this.position.y + "," + this.position.z 
			+ " speed = " + this.speed.x  +"," + this.speed.y + "," + this.speed.z)	
	}

	getEnergy(){
		let pot = Math.abs(this.position.x) + Math.abs(this.position.y) + Math.abs(this.position.z)
		let kin = Math.abs(this.speed.x) + Math.abs(this.speed.y) + Math.abs(this.speed.z)
		return kin*pot
	}
	
}

function firstPuzzle(planets,iterations){
	
	for(let iteration = 0; iteration < iterations; iteration++){
		//console.log("iteration " + iteration)
		//planets.map(item => item.printInfo())
		planets.forEach((item,ix) => {
			item.applyGravity(planets.filter( item => planets.indexOf(item) > ix))
		})
		planets.map( item => item.applySpeed())
	}
	let totalEnergy = 0
	planets.forEach( item => totalEnergy += item.getEnergy())
	console.log("Total energy : " + totalEnergy)

}


function secondPuzzle(asteroids){
    let all_x = []
    let iterations = 10
	for(let iteration = 0; iteration < iterations; iteration++){
		planets.forEach((item,ix) => {
			item.applyGravity(planets.filter( item => planets.indexOf(item) > ix))
		})
		planets.map( item => item.applySpeed())
        let x = []
        planets.forEach(item => x.push(item.position.x))
	}
    console.log(all_x)
}

planets = []
/* EX 1
planets.push( new Planet({'x':-1, 'y':0, 'z':2}))
planets.push( new Planet({'x':2, 'y':-10, 'z':-7}))
planets.push( new Planet({'x':4, 'y':-8, 'z':8}))
planets.push( new Planet({'x':3, 'y':5, 'z':-1}))
firstPuzzle(planets,10)
*/

// EX 2
/*
planets.push( new Planet({'x':-8, 'y':-10, 'z':0}))
planets.push( new Planet({'x':5, 'y':5, 'z':10}))
planets.push( new Planet({'x':2, 'y':-7, 'z':3}))
planets.push( new Planet({'x':9, 'y':-8, 'z':-3}))
firstPuzzle(planets,100)
*/

// PUZZLE 1
planets.push( new Planet({'x':-13, 'y':14, 'z':-7}))
planets.push( new Planet({'x':-18, 'y':9, 'z':0}))
planets.push( new Planet({'x':0, 'y':-3, 'z':-3}))
planets.push( new Planet({'x':-15, 'y':3, 'z':-13}))
//firstPuzzle(planets,1000)

secondPuzzle(planets)
return
