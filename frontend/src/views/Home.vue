<template lang="pug">
  #app
    navbar
</template>

<script>
import { mapGetters } from 'vuex'

import Navbar from '@/components/Navbar'

export default {
  name: 'home',
  components: {
    'navbar': Navbar
  },
  computed: mapGetters(['isGuest']),
  created () {
    if (this.isGuest) {
      this.$router.push({ name: 'login' })
    }
  }
}
</script>
