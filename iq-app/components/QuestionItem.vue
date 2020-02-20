<template>
  <div>
    <v-list-item v-show="!editing">
      <v-list-item-content @click="editing = true">
        <v-list-item-title>
          {{ inputTitle }}
        </v-list-item-title>
        <v-list-item-subtitle>
          <vue-markdown :source="inputContent"></vue-markdown>
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn class="mx-2" fab dark x-small color="error" @click="destroy">
          <v-icon dark>mdi-minus</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
    <v-list-item v-show="editing">
      <v-list-item-content>
        <v-card>
          <v-text-field
            v-model="inputTitle"
            label="title"
            autofocus
          ></v-text-field>
          <v-textarea
            v-model="inputContent"
            flat
            auto-grow
            outlined
            label="content"
            @focus="onFocusInput"
            @blur="onBlurInput"
          ></v-textarea>
        </v-card>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn class="mx-2" fab dark x-small @click="editing = false">
          <v-icon dark>mdi-close</v-icon>
        </v-btn>
        <v-btn class="mx-2" fab dark x-small color="success" @click="save">
          <v-icon dark>mdi-content-save</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'

export default {
  name: 'QuestionItem',
  components: {
    VueMarkdown
  },
  props: ['questionInfo'],
  data() {
    return {
      editing: false,
      inputTitle: '',
      inputContent: ''
    }
  },
  computed: {
    title() {
      return this.questionInfo.title
    },
    content() {
      return this.questionInfo.content
    },
    id() {
      return this.questionInfo.id
    }
  },
  created() {
    this.initialize()
  },
  methods: {
    initialize() {
      this.editing = false
      this.inputTitle = this.title
      this.inputContent = this.content
    },
    save(ev) {
      this.$emit('save-question', {
        id: this.id,
        title: this.inputTitle,
        content: this.inputContent
      })
      this.initialize()
    },
    destroy(ev) {
      this.$emit('delete-question', this.id)
    }
  }
}
</script>
