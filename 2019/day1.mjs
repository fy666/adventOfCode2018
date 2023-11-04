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

function compute(val)
{
    return Math.floor(val/3)-2
}

function analyze(array){
let result = []
array.forEach(e => result.push(Math.floor(e/3)-2))
// console.log(result)
let sumRes = result.reduce((a,b) => a+b)
return(sumRes)
}

function analyze2(array){

let result = []
array.forEach(e => {
    let tmp = [compute(e)]
    while (tmp[tmp.length - 1] > 0){
            tmp.push(compute(tmp[tmp.length - 1]))
        }
    tmp.pop()
    console.log("New line" + tmp)
    let tmpSum = tmp.reduce((a,b) => a+b)
    result.push(tmpSum)
}
)
    // console.log(result)
let sumRes = result.reduce((a,b) => a+b)
return(sumRes)
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

let data = fs.readFileSync('day1.txt', 'utf8').split('\n');
//let arr = data.split('\n')
console.log(data[0])


/*
console.log(computeLol(4))

rl.on('close',function(line){
console.log('total lines = ' + line_no)
console.log('objects in array'+ array.length)
let n = analyze(array)
let n2 = 2
n2 = analyze2(array)
console.log('res1 =' + n + ', res2 =' + n2)
})
*/
