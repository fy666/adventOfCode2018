const fs = require('fs')

class Cards {
  constructor(numberOfCards) {
      this.cards = Array(numberOfCards).fill(0)
      this.cards.forEach( (item,ix) => this.cards[ix] = ix)
      this.numberOfCards = numberOfCards
  }

  dealNewStack(){
      this.cards = this.cards.reverse()
  }
  cut(N){
      if(N < 0){
          N = this.numberOfCards + N
      }
    this.cards = this.cards.slice(N).concat(this.cards.slice(0,N))
  }

  dealWithIncrement(N){
      let tmp = Array(this.numberOfCards).fill(0)
      let index = 0
      for(let item of this.cards){
          //console.log("put " + item + " at index " + index)
          tmp[index] = item
          index += N
          index = index%this.numberOfCards
      }
      this.cards = tmp.slice(0)

  }
  logging(){
      console.log(this.cards)
  }
  searchCards(number){
    for(let ix in this.cards){
        if(this.cards[ix] == number){
            return ix
        }
    }
    return undefined
    }
}

class Card {
    constructor(card,number){
        this.numberOfCards = number
        this.position = card
    }
    dealNewStack(){
        this.position = this.numberOfCards - this.position - 1
    }
    dealWithIncrement(N){
        let index = 0
        for(let ix = 0; ix < this.position; ix++){
            //console.log("index " + index)
            index += N
            index = index%this.numberOfCards
        }
        this.position = index
    }
    cut(N){
        if(N < 0){
            N = this.numberOfCards + N
        }
        if(this.position < N){
            this.position = this.numberOfCards - (N - this.position)
        }
        else{
            this.position = this.position - N
        }
    }
    run(operation){
        operation()
    }
}

class CardDeck {
    constructor(position,number){
        this.numberOfCards = number
        this.card = position // at first, ordered list
        this.operations =  []
    }
    dealNewStack(){
        //this.card =
        let oldPositionOfNewCard = this.numberOfCards - this.cards - 1
        // what cards was in that previous position ?
    }
    dealWithIncrement(N){
        let index = 0
        for(let ix = 0; ix < this.position; ix++){
            //console.log("index " + index)
            index += N
            index = index%this.numberOfCards
        }
        this.position = index
    }
    cut(N){
        if(N < 0){
            N = this.numberOfCards + N
        }
        if(this.position < N){
            this.position = this.numberOfCards - (N - this.position)
        }
        else{
            this.position = this.position - N
        }
    }
    interpretOrder(data){
        let cmd
        for(let item of data){
            if(cmd = item.match(/deal into new stack/g)){
                this.operations.push(() => this.dealNewStack())
            }
            else if(cmd = item.match(/([0-9-]+)/g)){
                let N = parseInt(cmd,10)
                if(cmd = item.match(/cut/g)){
                    //console.log("RE cut " + N)
                    this.operations.push(() => this.cut(N))
                }
                else if(cmd = item.match(/deal with increment/g)){
                    //console.log("RE deal with increment " + N)
                    this.operations.push( () => this.dealWithIncrement(N))
                }
            }
        }
    }
    run(){
        for (let op of this.operations){
            op()
            console.log("new position " + this.position)
            return
        }
    }
}


function firstPuzzle(data,cards){
    let draw = new Cards(cards)
    //draw.logging()
    let cmd
        for(let item of data){
            //console.log(item)
            if(cmd = item.match(/deal into new stack/g)){
                //console.log("RE deal into new stack ")
                draw.dealNewStack()
            }
            else if(cmd = item.match(/([0-9-]+)/g)){
                let N = parseInt(cmd,10)
                if(cmd = item.match(/cut/g)){
                    //console.log("RE cut " + N)
                    draw.cut(N)
                }
                else if(cmd = item.match(/deal with increment/g)){
                    //console.log("RE deal with increment " + N)
                    draw.dealWithIncrement(N)
                }
            }
            //draw.logging()
        }
    //draw.logging()
    console.log("2019 at " + draw.searchCards(2019))

}



function firstPuzzleBis(data,wantedCard, numberOfCards){

    let draw = new Card(wantedCard,numberOfCards)
    //draw.logging()
    let cmd
        for(let item of data){
            //console.log(item)
            if(cmd = item.match(/deal into new stack/g)){
                //console.log("RE deal into new stack ")
                draw.dealNewStack()
            }
            else if(cmd = item.match(/([0-9-]+)/g)){
                let N = parseInt(cmd,10)
                if(cmd = item.match(/cut/g)){
                    //console.log("RE cut " + N)
                    draw.cut(N)
                }
                else if(cmd = item.match(/deal with increment/g)){
                    //console.log("RE deal with increment " + N)
                    draw.dealWithIncrement(N)
                }
            }
            //draw.logging()
        }
    //draw.logging()
    console.log("card at " + draw.position)

}

function firstPuzzleTer(data,wantedCard, numberOfCards){

    let draw = new CardDeck(wantedCard,numberOfCards)
    draw.interpretOrder(data)
    draw.run()

}
function secondPuzzle(data){

}

let data = fs.readFileSync('day22.txt', 'utf8').split('\n')
console.log("First Puzzle")

//firstPuzzle(data,10007)
//firstPuzzleBis(data, 2019, 10007)
firstPuzzleTer(data, 2019, 10007)
