// FUEL REACTION
const fs = require('fs')


function getIngredient(str){
    //console.log("Parsing " + str)
    const qtity = parseInt(str.match(/(\d+)/g)[0],10)
    const ing = str.match(/([A-Z]+)/g)[0]
    //console.log("INGR " + qtity + " : " + ing)
    return {'mat' : ing, "qty" : qtity}

}
function printReactions(reactions){
        for (let i of reactions) {
            console.log(JSON.stringify(i))
        }
}

function inputParser(data){
    let reactions = []
    for (item of data){
        //console.log(item.split('=>')[0].split(','))
        let products = item.split('=>')[1]
        let reaction = {}
        reaction['out'] = getIngredient(item.split('=>')[1])
        reaction['in']=[]
        for (let reactive of item.split('=>')[0].split(',')){
            reaction['in'].push(getIngredient(reactive))
        }
        reactions.push(reaction)
    }
    return reactions

}

function findRepeatObject(array, newObj){
    //console.log("obj to compair " + JSON.stringify(newObj))
    let answer = false
    array.forEach(item => {
    //    console.log("item " + JSON.stringify(item))
        if(Object.keys(newObj).filter( key => item[key] == newObj[key]).length == Object.keys(newObj).length)
        {answer = true; return}
    })
    return answer
}

function onlyFirstElement(ingredients){
    for(key of Object.keys(ingredients)){
        if(ingredients[key] != 0 && key != 'ORE'){
            return false
        }
    }
    return true
}

function addInDict(dict,key, value){
    if(dict[key]){
        dict[key] += value
    }
    else {
        dict[key] = value
    }
}

function addInDictArray(dict,key, value){
    if(dict[key]){
        dict[key].push(value)
    }
    else {
        dict[key] = [value]
    }
}

function firstPuzzle(reactions){
//    printReactions(reactions)
    let wanted = {'FUEL' : 1} //{'mat' : 'FUEL', 'qty' : 1}
    let extra_produced = {}
    while(!onlyFirstElement(wanted)){
    //    console.log("Not complete, wanted : " + JSON.stringify(wanted))
        for(key of Object.keys(wanted)){
            if(wanted[key] != 0 && key!="ORE"){
    //            console.log("treating " + key)
                let res = reactions.filter(item => item.out.mat == key)[0] // only one found ?
    //            console.log("reaction used " + JSON.stringify(res))
                let mul = Math.ceil(wanted[key] / res.out.qty)
                for(neededIngredient of res.in){
                    let needed = mul*neededIngredient.qty
                    if(extra_produced[neededIngredient.mat]){
                        needed -= extra_produced[neededIngredient.mat]
                        extra_produced[neededIngredient.mat] = 0
                    }
                    addInDict(wanted, neededIngredient.mat, needed)
                }
                addInDict(extra_produced,key, (mul*res.out.qty - wanted[key]))
                wanted[key] = 0
    //            console.log("Wanted : " + JSON.stringify(wanted))
    //            console.log("Extra : " + JSON.stringify(extra_produced))
            }
        }
    }

    console.log("Number of ORE : " + wanted['ORE'])
}

function secondPuzzle(reactions){

    let numberFuel = 0
    let usedOre = 0
    let wanted = {'FUEL' : 1, 'ORE':0}
    let extra_produced = {}
    let extras = []
    let allElementUsed = true
    while(allElementUsed){
        numberFuel+=1
        wanted = {'FUEL' : 1}
        while(!onlyFirstElement(wanted)){
        //    console.log("Not complete, wanted : " + JSON.stringify(wanted))
            for(key of Object.keys(wanted)){
                if(wanted[key] != 0 && key!="ORE"){
                    let res = reactions.filter(item => item.out.mat == key)[0] // only one found ?
                    let mul = Math.ceil(wanted[key] / res.out.qty)
                    for(neededIngredient of res.in){
                        let needed = mul*neededIngredient.qty
                        if(extra_produced[neededIngredient.mat]){
                            needed -= extra_produced[neededIngredient.mat]
                            extra_produced[neededIngredient.mat] = 0
                        }
                        addInDict(wanted, neededIngredient.mat, needed)
                    }
                    addInDict(extra_produced,key, (mul*res.out.qty - wanted[key]))
                    wanted[key] = 0
                }
            }
        }
        /*
        for(key of Object.keys(extra_produced)){
            addInDictArray(extras, key, extra_produced[key])
        }
        console.log(extras)*/
        //console.log(extras)
        let repeatFound = false
        if (!findRepeatObject(extras,extra_produced)) {
            extras.push(Object.assign({}, extra_produced))
        }
        else {
            console.log("Find Repeating! ")
            allElementUsed = false
        }

        //console.log("Extra " + JSON.stringify(extra_produced))
        //allElementUsed = !onlyFirstElement(extra_produced)

        usedOre += wanted['ORE']
    }
    console.log(usedOre + " ORE used to produce exactly " + numberFuel + " FUEL")
    console.log(Math.floor(numberFuel / usedOre * 1000000000000) + " FUEL could be created with 1 trillion ORE")
}


let data = fs.readFileSync('day14_3.txt', 'utf8').split('\n')
data.pop()

console.log("First Puzzle")
//let reactions = inputParser(data)
firstPuzzle(inputParser(data))
secondPuzzle(inputParser(data))
