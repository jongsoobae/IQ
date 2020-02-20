<template>
  <v-card>
    <v-list two-line subheader>
      <QuestionItem
        v-for="(item, id) in questions"
        :id="id"
        :key="id"
        class="markdown-area"
        :title="item.title"
        :content="item.content"
        :editing="item.editing"
        @set-editing="onChangeEditing"
        @set-content="onChangeContent"
        @save-question="saveQuestions"
        @delete-question="deleteQuestion"
        @close-question="closeQuestion"
      ></QuestionItem>
      <v-list-item>
        <v-list-item-content></v-list-item-content>
        <v-list-item-action>
          <v-btn
            v-if="!this.adding"
            class="mx-2"
            fab
            dark
            x-small
            color="success"
            @click="addNewQuestions"
          >
            <v-icon dark>mdi-plus</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import Vue from 'vue'
import QuestionItem from '@/components/QuestionItem'

export default {
  components: {
    QuestionItem
  },
  data: () => ({
    questions: {},
    adding: false
  }),
  created() {
    this.initialize()
  },
  methods: {
    initialize() {
      this.fetchQuestions()
      this.adding = false
    },
    onChangeEditing({ id, value }) {
      this.questions[id].editing = value
      this.closeAdd()
    },
    onChangeContent({ id, value }) {
      this.questions[id].content = value
    },
    fetchQuestions() {
      this.questions = {}
      fetch('http://127.0.0.1:8000/questions')
        .then((res) => res.json())
        .then((res) => {
          res.forEach((item) => {
            Vue.set(this.questions, item._id, {
              id: item._id,
              title: item.title,
              content: item.content,
              editing: false
            })
          })
        })
    },
    addNewQuestions() {
      Vue.set(this.questions, '', { editing: true })
      this.adding = true
    },
    closeAdd() {
      Vue.delete(this.questions, '')
      this.adding = false
    },
    saveQuestions(question) {
      const { id, title, content } = question
      if (id) this.updateQuestions(id, title, content)
      else this.createQuestions(title, content)
    },
    createQuestions(title, content) {
      fetch('http://127.0.0.1:8000/questions', {
        method: 'POST',
        body: JSON.stringify({
          title,
          content
        })
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    },
    updateQuestions(id, title, content) {
      fetch(`http://127.0.0.1:8000/questions/${id}`, {
        method: 'PUT',
        headers: {
          'Content-type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({
          title,
          content
        })
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    },
    closeQuestion() {
      this.closeAdd()
    },
    deleteQuestion(id) {
      fetch(`http://127.0.0.1:8000/questions/${id}`, {
        method: 'DELETE'
      })
        .then(() => {
          this.initialize()
        })
        .catch((err) => {
          alert(err)
        })
    }
  }
}
</script>

<style>
.markdown-area {
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial,
    sans-serif, Apple Color Emoji, Segoe UI Emoji;
  font-size: 0.8em;
  line-height: 1.5;
  word-wrap: break-word;
}
.markdown-area pre {
  display: inline-block;
  white-space: pre;
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #e6e8ea;
  color: #2b2927;
  border-radius: 3px;
  word-wrap: normal;
}
.markdown-area pre code {
  display: inline-block;
  padding: 0;
  margin: 0;
  overflow: visible;
  line-height: inherit;
  word-wrap: normal;
  background-color: initial;
  border: 0 !important;
  font-size: 100%;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border-radius: 3px;
  box-shadow: none;
  color: inherit;
  font-weight: 500;
}
.markdown-area pre code:after,
.markdown-area pre code:before {
  content: none !important;
}
</style>
