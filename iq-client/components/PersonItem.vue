<template>
  <v-list-item :to="`persons/${id}`">
    <v-list-item-content>
      <v-list-item-title>{{ name }}</v-list-item-title>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn
        class="mx-2"
        fab
        dark
        x-small
        color="error"
        @click.prevent="destroy"
      >
        <v-icon dark>mdi-minus</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  name: 'PersonItem',
  props: {
    id: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    }
  },
  data() {
    return {}
  },
  computed: {},
  methods: {
    destroy(ev) {
      this.$emit('delete-person', this.id)
    }
  }
}
</script>
