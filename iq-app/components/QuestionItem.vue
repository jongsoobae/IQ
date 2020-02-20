<template>
  <div>
    <v-list-item v-show="!editMode">
      <v-list-item-content @click="editMode = true">
        <v-list-item-title>
          {{ title }}
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
        </v-card>
      </v-list-item-content>
      <v-list-item-action>
        <v-speed-dial open-on-hover="true" direction="bottom" absolute top>
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
          <v-btn v-if="this.id" icon small color="error" @click="destroy">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-speed-dial>
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'QuestionItem',
  props: ['id', 'title', 'content', 'editing'],
  data: () => ({
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
    editMode: {
      get() {
        return this.editing
      },
      set(value) {
        this.$emit('set-editing', {
          id: this.id,
          value
        })
      }
    },
    preview: {
      get() {
        return `# ${this.title}\n\n${this.content}`
      }
    }
  },
  created() {},
  methods: {
    initialize() {},
    save(ev) {
      this.$emit('save-question', {
        id: this.id,
        title: this.title,
        content: this.content
      })
      this.initialize()
    },
    destroy(ev) {
      if (this.id) {
        if (confirm('delete ? y/n')) this.$emit('delete-question', this.id)
      } else {
        this.$emit('close-question')
      }
    },
    close(ev) {
      this.editMode = false
      if (!this.id) this.destroy()
    }
  }
}
</script>
