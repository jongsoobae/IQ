<template>
  <div>
    <v-list-item v-show="!editMode">
      <v-list-item-content @click="editMode = true">
        <v-list-item-title>
          {{ title }}
          <v-chip
            v-for="tag in tags"
            :key="tag.value"
            class="ma-1"
            small
            label
            color="#cde"
          >
            <v-icon left small>mdi-tag</v-icon>
            {{ tag.value }}
          </v-chip>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item v-show="editMode">
      <v-list-item-content>
        <v-card>
          <v-text-field v-model="title" label="title" autofocus></v-text-field>
          <mavon-editor
            v-model="content"
            :toolbars="toolbars"
            language="en"
            :subfield="false"
          />
          <VoerroTagsInput
            v-model="tags"
            :existing-tags="existTags"
            :typeahead="true"
          ></VoerroTagsInput>
        </v-card>
      </v-list-item-content>
      <v-list-item-action>
        <v-speed-dial :open-on-hover="true" direction="bottom" absolute top>
          <template v-slot:activator>
            <v-btn icon x-small>
              <v-icon>mdi-dots-horizontal</v-icon>
            </v-btn>
          </template>
          <v-btn icon small @click="close">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-btn icon small color="success" @click="save">
            <v-icon>mdi-content-save</v-icon>
          </v-btn>
          <v-btn v-if="id" icon small color="error" @click="destroy">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-speed-dial>
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
import VoerroTagsInput from '@voerro/vue-tagsinput'

export default {
  name: 'QuestionItem',
  components: { VoerroTagsInput },
  props: {
    id: {
      type: String,
      required: true
    },
    editing: Boolean
  },
  data: () => ({
    editMode: false,
    title: '',
    content: '',
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
  computed: {
    preview: {
      get() {
        return `# ${this.title}\n\n${this.content}`
      }
    },
    question() {
      return this.$store.state.question.questions[this.id]
    },
    existTags() {
      return this.$store.state.tag.tags
    }
  },
  created() {
    this.editMode = this.editing
    this.title = this.question.title
    this.content = this.question.content
    this.tags = (this.question.tags || []).map((tag) => ({
      key: '',
      value: tag
    }))
  },
  methods: {
    initialize() {
      this.editMode = false
      this.title = this.question.title
      this.content = this.question.content
      this.tags = (this.question.tags || []).map((tag) => ({
        key: '',
        value: tag
      }))
    },
    save(ev) {
      this.$store
        .dispatch('question/saveQuestion', {
          id: this.id,
          title: this.title,
          content: this.content,
          tags: this.tags.map((slug) => slug.value)
        })
        .then(() => {
          this.editMode = false
          this.$store.dispatch('tag/fetchTags')
        })
        .catch((err) => {
          alert(err)
        })
    },
    destroy(ev) {
      if (confirm('delete ? y/n'))
        this.$store.dispatch('question/deleteQuestion', this.id)
    },
    close(ev) {
      this.initialize()
      this.$store.commit('question/deleteQuestion', '')
    }
  }
}
</script>
