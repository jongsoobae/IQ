<template>
  <v-form>
    <VoerroTagsInput
      v-model="tags"
      element-id="allTags"
      :typeahead="true"
    ></VoerroTagsInput>
    <v-btn color="success" @click="saveTags">
      Save
    </v-btn>
    <v-btn color="error" class="mr-4" @click="resetTags">
      Reset
    </v-btn>
  </v-form>
</template>

<script>
import VoerroTagsInput from '@voerro/vue-tagsinput'

export default {
  components: { VoerroTagsInput },
  async asyncData({ store, params }) {
    await store.dispatch('tag/fetchTags')
    store.commit('setLayoutTitle', 'Tags')
    return {
      tags: store.state.tag.tags,
      initTags: store.state.tag.tags
    }
  },
  computed: {},
  created() {},
  methods: {
    async saveTags() {
      await this.$store.dispatch('tag/saveTag', this.tags)
      location.reload()
    },
    resetTags() {
      this.tags = [...this.initTags]
    }
  }
}
</script>
