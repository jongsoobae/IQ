import Vue from 'vue'

export const state = () => ({
  persons: {}
})

export const mutations = {
  setPerson(state, person) {
    state.persons = { [person.id]: person, ...state.persons }
  },
  setPersons(state, persons) {
    const newItems = {}
    persons.forEach((person) => {
      newItems[person.id] = person
    })
    state.persons = newItems
  },
  updatePerson(state, updated) {
    const { pid, qidx, value } = updated
    for (const key in value) {
      Vue.set(state.persons[pid].questions[qidx], key, value[key])
    }
  }
}

export const actions = {
  fetchSetPerson({ commit, state }, id) {
    return fetch(`${process.env.apiUrl}/persons/${id}`)
      .then((res) => res.json())
      .then((res) => {
        commit('setPerson', res)
      })
  }
}
