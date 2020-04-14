export const state = () => ({
  tags: []
})

export const mutations = {
  initTags(state, tags) {
    const newItems = []
    if (tags) {
      tags.forEach((tag) => {
        newItems.push({ key: '', value: tag.name })
      })
      state.tags = newItems
    }
  },
  removeTag(state, name) {
    state.tags.splice(state.tags.indexOf(name), 1)
  },
  appendTag(state, name) {
    state.tags.push({
      key: name,
      value: name
    })
  }
}

export const actions = {
  async saveTag({ commit, state }, tags) {
    await fetch(`${process.env.apiUrl}/tags`, {
      method: 'POST',
      body: JSON.stringify(tags.map((tag) => tag.value))
    })
  },
  fetchTags({ commit, state }) {
    return fetch(`${process.env.apiUrl}/tags`, {
      method: 'GET'
    })
      .then((res) => res.json())
      .then((res) => commit('initTags', res))
  }
}
