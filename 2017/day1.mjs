/*
const readline = require('readline')
const fs = require('fs')
const fetch = require("node-fetch");
*/

import readline from "readline"
import fs from "fs"
import fetch from "node-fetch"
import computeLol from "./utils.mjs"

let rl = readline.createInterface({
input:fs.createReadStream('day1.txt')
        });

let line_no = 0
let line
let array=[]

rl.on('line', function(line){
   line_no ++
   array.push(line)
})

function analyze(array){
const result = []
array.forEach(e => result.push(Math.floor(e/3)-2))
// console.log(result)
let sumRes = result.reduce((a,b) => a+b)
return(sumRes)
}

function analyze2(array){
let sum = 0
let newSum = 0
let i = 0
for (ele of array){
    let localSum = []
    newSum = Math.floor(ele / 3) - 2
    console.log(newSum)
    while (newSum > 0){
        localSum.push(newSum)
        newSum = Math.floor(newSum / 3) - 2
    }
    let result = localSum.reduce((a,b) => a+b,0)

    //console.log("Input : " + ele + " subsums = " + localSum + " sum = " + result)
    //console.log(ele)
    //console.log("Input : "  + ele + " , output : " + newSum)
    sum += result
}
return(sum)
}

/*
async function testRead(){
    const response = await fetch('https://adventofcode.com/2019/day/1/input');
    const data = await response.text()
    console.log(data)
}


testRead()


*/

/*
const response = await fetch('https://adventofcode.com/2019/day/1/input');
const data = response.json()
console.log(data)
*/


console.log(computeLol(4))

rl.on('close',function(line){
console.log('total lines = ' + line_no)
console.log('objects in array'+ array.length)
let n = analyze(array)
let n2 = 2
//let n2 = analyze2(array)
console.log('res1 =' + n + ', res2 =' + n2)
})
