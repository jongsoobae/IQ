export const state = () => ({
  sockets: {},
  layout: {
    title: '면접자'
  }
})

export const mutations = {
  setLayoutTitle(state, title) {
    state.layout.title = title
  },
  setSockets(state, { url, socket }) {
    state.sockets = { [url]: socket, ...state.sockets }
  }
}

export const actions = {
  socket({ commit, state }, url) {
    let socket
    const created = !(url in state.sockets)
    if (!created) socket = state.sockets[url]
    else {
      socket = new WebSocket(url)
      commit('setSockets', { url, socket })
    }

    return {
      created,
      socket
    }
  }
}
