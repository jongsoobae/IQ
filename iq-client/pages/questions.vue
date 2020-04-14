<template>
  <v-card>
    <v-list two-line subheader>
      <v-list-item>
        <v-list-item-content></v-list-item-content>
        <v-list-item-action>
          <v-btn
            v-if="!('' in questions)"
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
      <QuestionItem
        v-for="(item, id) in questions"
        :id="id"
        :key="id"
        class="markdown-area"
        :editing="!item.id"
      ></QuestionItem>
    </v-list>
  </v-card>
</template>

<script>
import QuestionItem from '@/components/QuestionItem'

export default {
  components: {
    QuestionItem
  },
  async asyncData({ store }) {
    store.commit('setLayoutTitle', '문제')
    await store.dispatch('tag/fetchTags')
    return {
      adding: false
    }
  },
  computed: {
    questions() {
      return this.$store.state.question.questions
    }
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize() {
      this.fetchQuestions()
      this.adding = false
    },
    fetchQuestions() {
      fetch(`${process.env.apiUrl}/questions`)
        .then((res) => res.json())
        .then((res) => {
          this.$store.commit('question/setQuestions', res)
        })
    },
    addNewQuestions() {
      this.$store.commit('question/newQuestion')
      this.adding = true
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
