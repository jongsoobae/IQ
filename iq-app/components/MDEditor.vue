<template>
  <v-card flat :style="'background: inherit'">
    <v-text-field v-model="title" label="title" autofocus></v-text-field>
    <v-textarea
      v-model="content"
      flat
      auto-grow
      outlined
      label="content"
      @focus="onFocusInput"
      @blur="onBlurInput"
    ></v-textarea>
  </v-card>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  name: 'MarkdownEditor',
  props: ['propTitle', 'propContent'],
  data: () => ({
    title: '',
    content: ''
  }),
  mounted() {
    this.initialize()
  },
  methods: {
    onFocusInput(ev) {},
    onBlurInput(ev) {
      // if (!this.title) {
      //   this.$el.querySelector('input[type=text]').focus()
      //   return
      // }
      // if (!this.content) {
      //   ev.target.focus()
      // }
      // this.$emit('create-memo', this.title, this.content)
      // this.initialize()
    },
    initialize() {
      this.title = this.propTitle
      this.content = this.propContent
    }
  }
})
</script>
