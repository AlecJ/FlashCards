<script>
import FlashCard from "../components/FlashCard.vue";

export default {
  name: "user",
    components: {
    FlashCard,
  },
  data() {
    return {
      timeout: null,
      userGuessed: false,
      card: null,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.axios.get('/api').then((response) => {
        this.card = response.data
      })
      
    },
    handleFlashCardClick(bool) {
      if (this.timeout) clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.userGuessed = bool;
      }, 20)
    },
    handleUserGuess(bool) {
      this.handleFlashCardClick(false)
      // Send the guess to the backend service
      const data = {id: this.card.id, wasCorrect: bool}
      this.axios.put('/api', {data: data}).then((response) => {
        if (!!response.data) {
          this.card = response.data
        } else {
          this.card = null
        }
        console.log(response.data)
      })
    }
  }
};
</script>

<template>
  <div id="container">
    <FlashCard id="card" width="100%" height="100%"
               @click="!userGuessed && handleFlashCardClick(true)">
      <div id="isThereACard" v-if="!!this.card">
        <div id="wordCard" v-if="!userGuessed">
          <h1 id="wordToGuess">{{ card.word }}</h1>
          <p id="bottomText">Click anywhere on the card to see the definition.</p>
        </div>
        <div id="resultCard" v-else>
          <h1 id="wordToGuess">{{ card.definition }}</h1>
          <p>Select a result to continue.</p>
          <div id="btnRow">
            <button class="guessBtn" @click="handleUserGuess(true)">Correct</button>
            <button class="guessBtn" @click="handleUserGuess(false)">Incorrect</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>You are temporarily done; please come back later to review more words.</p>
      </div>
    </FlashCard>
  </div>
</template>

<style scoped>
#container {
  width: 100%;
  height: 70vh;
  display: grid;
  justify-items: center;
}

#card {
  width: 100%;
  max-width: 1030px;
  height: 100%;
  max-height: 600px;
  background: rgba(163, 163, 163, 0.5);

  border-radius: 15px;

  display: grid;
  align-items: center;
  justify-items: center;
  grid-template-rows: 5fr 1fr;
}

#isThereACard {
  width: 100%;
  height: 100%;
  display: grid;
  align-items: center;
  justify-items: center;
}

#wordCard {
  width: 90%;
  height: 100%;

  display: grid;
  align-items: center;
  grid-template-rows: 4fr 1fr;
}

#resultCard {
  width: 90%;
  height: 100%;

  display: grid;
  align-items: center;
  text-align: center;
  grid-template-rows: 8fr 1fr 1fr;
}

#wordToGuess {
  text-align: center;
  font-weight: bold;
  font-size: 5rem;
}

#bottomText {
  text-align: center;
  align-self: end;
}

#btnRow {

}

.guessBtn {
  width: 33%;
  max-width: 200px;
  margin: 5px;

  height: 100%;
  max-height: 130px;
  min-height: 40px;


}
</style>
