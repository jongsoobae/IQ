const createQuestion = (title, content) => {
  return fetch(`${process.env.apiUrl}/questions`, {
    method: 'POST',
    body: JSON.stringify({
      title,
      content
    })
  })
}

const updateQuestions = (id, title, content) => {
  return fetch(`${process.env.apiUrl}/questions/${id}`, {
    method: 'PUT',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify({
      title,
      content
    })
  })
}

export const state = () => ({
  questions: {}
})

export const mutations = {
  setQuestions(state, questions) {
    const newItems = {}
    questions.forEach((question) => {
      newItems[question.id] = question
    })
    state.questions = newItems
  },
  setQuestion(state, question) {
    state.questions[question.id] = question
  },
  newQuestion(state) {
    state.questions = {
      '': { editing: true },
      ...state.questions
    }
  },
  deleteQuestion(state, id) {
    const { [id]: deleted, ...rest } = state.questions
    state.questions = rest
  },
  insertQuestion(state, question) {
    state.questions = { [question.id]: question, ...state.questions }
  }
}

export const actions = {
  saveQuestion({ commit, state }, question) {
    let response
    if (question.id)
      response = updateQuestions(question.id, question.title, question.content)
    else response = createQuestion(question.title, question.content)
    return response
      .then((res) => res.json())
      .then((res) => {
        const data = res.data
        if (question.id) {
          commit('setQuestion', question)
        } else {
          commit('deleteQuestion', question.id)
          commit('insertQuestion', data)
        }
      })
  },
  deleteQuestion({ commit, state }, id) {
    return fetch(`${process.env.apiUrl}/questions/${id}`, {
      method: 'DELETE'
    }).then(() => {
      commit('deleteQuestion', id)
    })
  }
}
