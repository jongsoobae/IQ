<template>
  <div>
    <template v-for="(item, index) in questions">
      <mavon-editor
        :key="index"
        :value="getQuestion(item, index)"
        :toolbars="toolbars"
        language="en"
        :subfield="false"
        default-open="preview"
        :toolbars-flag="false"
      />
      <v-checkbox
        :key="index"
        v-model="item.asked"
        label="질문여부"
      ></v-checkbox>
      <v-textarea
        :key="index"
        v-model="item.connent"
        flat
        auto-grow
        outlined
        label="코멘트"
      ></v-textarea>
    </template>
  </div>
</template>

<script>
export default {
  data: () => ({
    name: '',
    questions: [],
    toolbars: {
      bold: true,
      italic: true,
      header: true,
      underline: true,
      strikethrough: true,
      mark: true,
      superscript: true,
      subscript: true,
      quote: true,
      ol: true,
      ul: true,
      link: true,
      imagelink: true,
      code: true,
      table: true,
      fullscreen: false,
      readmodel: false,
      htmlcode: true,
      help: false,
      undo: false,
      redo: false,
      trash: false,
      save: false,
      navigation: false,
      alignleft: false,
      aligncenter: false,
      alignright: false,
      subfield: true,
      preview: true,
      defaultOpen: 'preview',
      toolbarsFlag: false
    }
  }),
  async created() {
    await this.fetchQuestions()
  },
  methods: {
    fetchQuestions() {
      fetch('http://127.0.0.1:8000/questions')
        .then((res) => res.json())
        .then((res) => {
          this.questions = res
        })
    },
    getQuestion(item, index) {
      if (item.asked) {
        return `## 문제${index} - ${item.title}`
      }
      return `## 문제${index} - ${item.title}\n${item.content}`
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

<style>
.markdown-body {
  font-size: 13px !important;
  min-height: 0 !important;
}

.markdown-body .v-show-content {
  padding: 0 !important;
}
</style>
