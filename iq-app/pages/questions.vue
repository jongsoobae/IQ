<template>
  <v-card>
    <v-list two-line subheader>
      <QuestionItem
        v-for="(item, name) in questions"
        :key="name"
        :question-info="item"
        @delete-question="deleteQuestion"
      ></QuestionItem>
      <v-list-item>
        <v-list-item-content></v-list-item-content>
        <v-list-item-action>
          <v-btn class="mx-2" fab dark x-small color="success" @click="destroy">
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
    questions: {}
  }),
  created() {
    this.fetchQuestions()
  },
  methods: {
    fetchQuestions() {
      fetch('http://127.0.0.1:8000/questions')
        .then((res) => res.json())
        .then((res) => {
          res.forEach((question) => {
            Vue.set(this.questions, question.title, {
              title: question.title
            })
          })
        })
    }
  }
}
</script>
