<template>
  <div>
    <v-list-item v-show="!editing">
      <v-list-item-content>
        <v-list-item-title @click="editing = true">
          {{ title }}
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn class="mx-2" fab dark x-small color="error" @click="destroy">
          <v-icon dark>mdi-minus</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
    <v-list-item v-show="editing">
      <v-list-item-content>
        <MDEditor :prop-title="title" :prop-content="content"></MDEditor>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn
          class="mx-2"
          fab
          dark
          x-small
          color="success"
          @click="editing = false"
        >
          <v-icon dark>mdi-content-save</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
import MDEditor from '@/components/MDEditor'

export default {
  name: 'QuestionItem',
  components: {
    MDEditor
  },
  props: ['QuestionInfo'],
  data() {
    return {
      editing: false
    }
  },
  computed: {
    title() {
      return this.QuestionInfo.title
    },
    content() {
      return this.QuestionInfo.content
    }
  },
  methods: {
    destroy(ev) {
      this.$emit('delete-question', this.title)
    }
  }
}
</script>
