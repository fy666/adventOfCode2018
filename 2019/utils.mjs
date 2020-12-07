import readline from "readline"
import fs from "fs"

function readPuzzle(file, functionToApply)
{
    let rl = readline.createInterface({
        input:fs.createReadStream(file)
        });

    let line_no = 0
    let line
    let array=[]
    let newArray=[]

    rl.on('line', function(line){
       line_no ++
       array.push(line)
        })

    rl.on('close',function(line){
        functionToApply(array)
    })
}

function computeLol(a)
{
    return a+1
}

export default readPuzzle;
