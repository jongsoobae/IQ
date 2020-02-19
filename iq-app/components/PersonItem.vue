<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title>{{ name }}</v-list-item-title>
      <v-list-item-subtitle>{{ questions_asked }}</v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn class="mx-2" fab dark x-small color="error" @click="destroy">
        <v-icon dark>mdi-minus</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: 'PersonItem',
  props: ['personInfo'],
  data() {
    return {}
  },
  computed: {
    name() {
      return this.personInfo.name
    },
    questions_asked() {
      return this.personInfo.questions
        .map((q) => (q.asked ? ' o ' : ' - '))
        .join('')
    }
  },
  methods: {
    destroy(ev) {
      this.$emit('delete-person', this.name)
    }
  }
}
</script>
