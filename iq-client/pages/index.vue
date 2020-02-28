<template>
  <div>
    <v-card flat>
      <v-text-field
        v-model="inputName"
        append-outer-icon="mdi-send"
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
          Newer
        </v-subheader>
        <v-divider></v-divider>
        <PersonItem
          v-for="(item, id) in persons"
          :id="id"
          :key="id"
          :name="item.name"
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
import PersonItem from '@/components/PersonItem'

export default {
  components: {
    PersonItem
  },
  asyncData: ({ store, params }) => {
    store.commit('setLayoutTitle', '면접자')
    return {
      inputName: ''
    }
  },
  computed: {
    persons() {
      return this.$store.state.person.persons
    }
  },
  created() {
    this.fetchPersons()
  },
  methods: {
    fetchPersons() {
      fetch(`${process.env.apiUrl}/persons`)
        .then((res) => res.json())
        .then((res) => {
          this.$store.commit('person/setPersons', res)
        })
    },
    addNewPerson(ev) {
      if (!this.inputName) {
        ev.target.focus()
        return
      }

      fetch(`${process.env.apiUrl}/persons`, {
        method: 'POST',
        body: JSON.stringify({
          name: this.inputName
        })
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    },
    deletePerson(id) {
      if (!confirm('delete? Y/N')) return
      fetch(`${process.env.apiUrl}/persons/${id}`, {
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
