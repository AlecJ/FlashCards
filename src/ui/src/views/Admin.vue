<script>
import FlashCard from "../components/FlashCard.vue";
import LightBox from "../components/LightBox.vue";

export default {
  name: "admin",
  components: {
    FlashCard,
    LightBox,
  },
  data() {
    return {
      cards: [],
      isModalRevealed: false,
      userInputNewWord: '',
      userInputDefinition: '',
      error: '',
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.axios.get('/api/admin').then((response) => {
        console.log(response.data)
        this.cards = response.data
      })
    },
    addWord() {
      // verify string is valid
      if (this.userInputNewWord.match("^[A-Za-z ]{1,25}$") &&
          this.userInputDefinition.match("^[A-Za-z \.]{1,75}$")) {
        
        // Post the card to the backend
        const newCard = {word: this.userInputNewWord, definition: this.userInputDefinition}
        this.axios.post("/api", newCard).then((response) => {
          // add card to cards
          this.cards.push(response.data)
        })

        this.userInputNewWord = '';
        this.userInputDefinition = '';
        this.error = '';
      } else {
        this.error = 'Word must contain only characters and spaces. Definition may contain periods as well.';
      }
    },
    deleteWord(id) {
      console.log(id);
      // Send request to backend to delete card
      this.axios.delete("/api", {data: id}).then((response) => {
        console.log(response);
        // refresh card list
        this.loadData();
      })
    },
    toggleModal(bool) {
      this.isModalRevealed = bool;
    },
  }
};
</script>

<template>
  <div id="container">
    
    <div id="card-view">
      <!-- A card styled button sits on top to allow users to add words -->
      <div id="add-btn-row">
        <button id="add-card-btn" @click="toggleModal(true)">
          <FlashCard >
            <font-awesome-icon :icon="['fas', 'circle-plus']" />
          </FlashCard>
        </button>
      </div>

      <!-- Display a list of the users cards -->
      <div id="user-cards">
        <FlashCard class="user-card" v-for="card in cards" :key="card.id" width="280px" height="165px">
          <div id="card-word">{{ card.word }}</div>
          <div id="card-def">{{ card.definition }}</div>
          <div id="card-stats">
            <p class="small">Bin: {{ card.bin }}</p>
            <p class="small">Incorrect: {{ card.num_times_incorrect }}</p>
          </div>
          <div class="deleteBtn">
            <button @click="deleteWord(card.id)">
              <font-awesome-icon class="deleteBtnIcon" :icon="['fas', 'circle-minus']" />
            </button>
          </div>
        </FlashCard>
      </div>
    </div>
  </div>

  <LightBox :isRevealed="isModalRevealed" :toggleLightbox="toggleModal">
    <!-- This is the modal to add words -->
    <div id="add-card-modal">
      <p id="error-text">{{ error }}</p>
      <div id="modal-text-inputs">
        <label for="word-input">Word</label>
        <input id="word-input" name="word-input" v-model="userInputNewWord" maxlength="25" />
        <label for="definition-input">Definition</label>
        <textarea id="definition-input" name="definition" v-model="userInputDefinition" rows="3" maxlength="75" />
      </div>
      <div id="center-modal-btn">
        <button id="create-word-btn" @click="addWord(userInputNewWord)">Add Card</button>
      </div>
      <p :style="{'alignSelf': 'end', 'paddingBottom': '5px'}">Click anywhere outside modal to close.</p>
    </div>
  </LightBox>
</template>

<style scoped>
#container {
  width: 100%;
  height: 100%;
  display: grid;
  justify-items: center;
}

#card-view {
  width: 100%;
  max-width: 1200px;
}

#add-card-btn {
  border: none;
  background: none;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 4em;
  margin: 0;
  padding: 0;
}

#add-card-btn:hover {
  color: rgba(50, 50, 50, 0.5);
}

#user-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, 285px);
  justify-items: center;
}

.user-card {
  width: 100%;
  word-break: break-all;
}

#card-word {
  width: 100%;
  text-align: center;
  font-weight: bold;
}

#card-def {
  width: 100%;
  text-align: center;
}

.deleteBtn {
  position: absolute;
  top: 0;
  right: 0;
  width: 24px;
  height: 24px;
  transform: translateY(-6px) translateX(8px);
  border-radius: 12px;

  display:grid;
  align-items:center;
}

.deleteBtn button {
  border: none;
  background: none;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.deleteBtnIcon {
  width: 100%;
  height: 100%;
  color: red;
}

.deleteBtnIcon:hover {
  color: rgb(151, 2, 2)
}

#add-card-modal {
  min-width:300px;
  width: 60%;
  min-height: 390px;
  height: 60%;
  z-index: 2;
  
  background: rgb(211, 211, 211);
  border-radius: 15px;

  display: grid;
  grid-template-rows: 10fr 43fr 35fr 2fr;
  justify-items: center;
}

#error-text {
  color: red;
}

#modal-text-inputs {
  display: grid;
  justify-items: center;
  align-items: end;
  width: 75%;
}

#word-input {
  width: 100%;
  max-width: 800px;
  min-width: 200px;
  height: 90px;

  margin-bottom: 5px;

  align-self: end;
  text-align:center;
  font-size: 2.5rem;
}

#definition-input {
  width: 100%;
  max-width: 800px;
  min-width: 200px;
  height: 110px;

  padding: 5px;
  margin-bottom: 5px;

  align-self: end;
  text-align:center;
  font-size: 1.5rem;

  resize: none;
}

#create-word-btn {
  width: 200px;
  height: 70px;
  margin-top: 5px;
  align-self: start;
}

#card-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  justify-items: center;
}
.small {
  font-size: 80%;
}
</style>
