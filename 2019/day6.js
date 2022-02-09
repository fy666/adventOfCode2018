const fs = require('fs')

function distanceFromRootPath(dico, key, keyToFind, path){

    let dist = -1;
    if(key == keyToFind){
        return dist+1
    }
    if(!dico[key]){
        return -1
    }
    for(let item of dico[key]){
        if( (dist = distanceFromRootPath(dico, item, keyToFind, path)) >= 0){
           path.push(item)
           return dist+1
        }
    }
    return dist
}


function distanceFromRoot(dico, key, keyToFind ){
    if(!dico[key]){
        return -1
    }

    let dist = 0;
    if(dico[key].includes(keyToFind)){
        return dist+1
    }
    for(item of dico[key]){
         if((dist = distanceFromRoot(dico, item, keyToFind)) >= 0)
        {
            return dist+1
        }
    }
    return dist
}

function analyze(array) {
    let dico = {}
    let all_keys = []
    array.forEach(item => {
    	let c = item.split(')');
        if(dico[c[0]]){
            dico[c[0]].push(c[1])
        }
        else{
        	dico[c[0]] = [c[1]];
    	}
        all_keys.push(c[0])
        all_keys.push(c[1])
    })

    all_keys = [...new Set(all_keys)]
    all_keys = all_keys.filter(item => item != "COM")

    let count = 0
    let res = 0
    let way = []
    for (item of all_keys){
        res = distanceFromRoot(dico, 'COM', item)
        //way=[]
        //res = distanceFromRootPath(dico, 'COM', item, way)
        count += res
        //console.log("way of " + item +" = "+ way)
    }
    console.log("Count is " + count)
}

function analyze2(array) {
    let dico = {}
    let all_keys = []
    array.forEach(item => {
    	let c = item.split(')');
        if(dico[c[0]]){
            dico[c[0]].push(c[1])
        }
        else{
        	dico[c[0]] = [c[1]];
    	}
        all_keys.push(c[0])
        all_keys.push(c[1])
    })

    all_keys = [...new Set(all_keys)]
    all_keys = all_keys.filter(item => item != "COM")

    let waySanta=[]
    let stepSanta = distanceFromRootPath(dico, 'COM', 'SAN', waySanta)
    let wayYou=[]
    let stepYou = distanceFromRootPath(dico, 'COM', 'YOU', wayYou)

    console.log("Way santa is " + waySanta)
    console.log("Way you is " + wayYou)
    let commonItem = []
    waySanta.forEach(itemSanta => {
        wayYou.forEach(itemYou => {
        if(itemSanta === itemYou){
            commonItem.push(itemSanta);
        }
        })
    })

    console.log("First common = " + commonItem[0])
    const result = stepSanta + stepYou - 2 - 2*commonItem.length
    console.log("Number of jumps : " + result)
    /*

    for (item of all_keys){
        //res = distanceFromRoot(dico, 'COM', item)
        way=[]
        res = distanceFromRootPath(dico, 'COM', item, way)
        count += res
        console.log("way of " + item +" = "+ way)
    }
    console.log("Count is " + count)
    */
}

let array = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']
//findPath('F')
//analyze2(array)

let data  = fs.readFileSync('day6.txt', 'utf8').split('\n')
console.log(data)
analyze(data.slice(0))
analyze2(data.slice(0))
