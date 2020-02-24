<template>
  <div>
    <template v-for="(item, index) in questions">
      <mavon-editor
        :key="item.id"
        :value="getQuestion(item, index)"
        :toolbars="toolbars"
        language="en"
        :subfield="false"
        default-open="preview"
        :toolbars-flag="false"
      />
      <v-checkbox
        :key="item.id + '_' + 'asked'"
        :input-value="item.asked"
        label="질문여부"
        @change="onChangeAsked(index, $event)"
      ></v-checkbox>
      <v-textarea
        :key="item.id + '_' + 'comment'"
        :value="item.comment"
        flat
        auto-grow
        outlined
        label="코멘트"
        @blur="onSaveComment(index, $event)"
      ></v-textarea>
    </template>
  </div>
</template>

<script>
export default {
  async asyncData({ store, params }) {
    await store.dispatch('person/fetchSetPerson', params.id)
    const { socket, created } = await store.dispatch(
      'socket',
      `ws://localhost:8000/person/${params.id}/question/ws`
    )

    if (created) {
      socket.onmessage = function(event) {
        const { qidx, value } = JSON.parse(event.data)
        store.commit('person/updatePerson', {
          pid: params.id,
          qidx,
          value
        })
      }
    }

    const person = store.state.person.persons[params.id]
    store.commit('setLayoutTitle', `면접자 - ${person.name}`)

    return {
      id: params.id,
      person,
      questions: person.questions,
      socket
    }
  },
  data: () => ({
    name: '',
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
  methods: {
    getQuestion(item, index) {
      index++
      if (item.asked) {
        return `## 문제 ${index}. - ${item.title}`
      }
      return `## 문제 ${index}. - ${item.title}\n${item.content}`
    },
    onChangeAsked(index, value) {
      this.socket.send(
        JSON.stringify({
          qidx: index,
          value: {
            asked: value
          }
        })
      )
    },
    onSaveComment(index, event) {
      this.socket.send(
        JSON.stringify({
          qidx: index,
          value: {
            comment: event.target.value
          }
        })
      )
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
