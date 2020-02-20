<template>
  <div>
    <v-card flat>
      <v-text-field
        v-model="inputName"
        append-outer-icon="mdi-send"
        :prepend-icon="icon"
        filled
        autofocus
        clear-icon="mdi-close-circle"
        clearable
        label="면접자 추가"
        type="text"
        @keyup.enter="addNewPerson"
        @click:append-outer="addNewPerson"
      ></v-text-field>
    </v-card>
    <v-card>
      <v-list two-line subheader>
        <v-subheader>
          Today
        </v-subheader>
        <v-divider></v-divider>
        <PersonItem
          v-for="(item, name) in todayItems"
          :key="name"
          :person-info="item"
          @delete-person="deletePerson"
        ></PersonItem>

        <v-subheader>
          Previous
        </v-subheader>
        <v-divider></v-divider>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'
import PersonItem from '@/components/PersonItem'

export default {
  components: {
    PersonItem
  },
  data: () => ({
    inputName: '',
    questions: [],
    todayItems: {}
  }),
  async created() {
    await this.fetchQuestions()
    await this.fetchPersons()
  },
  methods: {
    fetchQuestions() {
      fetch('http://127.0.0.1:8000/questions')
        .then((res) => res.json())
        .then((res) => {
          this.questions = res
        })
    },
    fetchPersons() {
      fetch('http://127.0.0.1:8000/persons')
        .then((res) => res.json())
        .then((res) => {
          this.todayItems = {}
          res.forEach((person) => {
            const questions =
              person.questions ||
              this.questions.map((q) => {
                q.asked = false
                return q
              })
            Vue.set(this.todayItems, person.name, {
              name: person.name,
              questions
            })
          })
        })
    },
    addNewPerson(ev) {
      if (!this.inputName) {
        ev.target.focus()
        return
      }

      fetch('http://127.0.0.1:8000/persons', {
        method: 'POST',
        body: JSON.stringify({
          name: this.inputName,
          date: '2020-02-21'
        })
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    },
    onAddNew(ev) {
      if (!this.inputName) {
        ev.target.focus()
        return
      }

      this.addNewPerson(this.inputName)
    },
    deletePerson(name) {
      fetch(`http://127.0.0.1:8000/persons/${name}`, {
        method: 'DELETE'
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    },
    initialize() {
      this.inputName = ''
      this.fetchPersons()
    }
  }
}
</script>
