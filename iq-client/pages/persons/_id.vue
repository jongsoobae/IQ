<template>
  <div>
    <template v-for="(item, index) in questions" class="markdown-area">
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
      `${process.env.wsUrl}/person/${params.id}/question/ws`
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
