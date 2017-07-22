<template lang="pug">
  section.section
    .container
      .columns
        .column.is-one-third
        .column(v-if="loading")
          sync-loader.spinner-loader
        .column(v-else)
          .notification(:class="isSucceeded ? 'is-success' : 'is-danger'")
            | Verification {{ isSucceeded ? 'succeeded' : 'failed' }}!
          .has-text-centered
            router-link(:to="{ name: 'login'}") Back to log in
        .column.is-one-third
</template>

<script>
import SyncLoader from 'vue-spinner/src/SyncLoader'

import User from '@/api/user'

export default {
  name: 'activate',
  components: {
    'sync-loader': SyncLoader
  },
  data () {
    return {
      loading: true,
      isSucceeded: false
    }
  },
  methods: {
    activate () {
      const uid = this.$route.params.uid
      const token = this.$route.params.token
      User.activate({ uid, token })
        .then(_ => {
          this.isSucceeded = true
        })
        .catch(_ => {})
        .then(_ => {
          this.loading = false
        })
    }
  },
  created () {
    this.activate()
  }
}
</script>
