<template lang="pug">
  section.section
    .container
      .columns
        .column.is-one-third
        .column
          .card
            form(@submit.prevent="onSubmit")
              .card-content
                .content
                  .field
                    p.control
                      input.input(v-model="usernameOrEmail" type="text" placeholder="Username or email")
                  .field.has-addons
                    p.control.is-expanded
                      input.input(v-model="password" type="password" placeholder="Password")
                    p.control
                      a.button Forgot?
                footer.card-footer
                  a.card-footer-item
                    button.button.is-success(type="submit" @click="login") Log in
          .content.has-text-centered.mt4
            p
              | Don't have an account?
              router-link(:to="{ name: 'signup'}")  Sign up
        .column.is-one-third
</template>

<script>
import { mapGetters } from 'vuex'

import User from '@/api/user'

export default {
  name: 'sign',
  computed: mapGetters(['isAuthenticated', 'token']),
  data () {
    return {
      usernameOrEmail: '',
      password: ''
    }
  },
  methods: {
    login () {
      User.login({ username_or_email: this.usernameOrEmail, password: this.password })
        .then(response => {
          this.$store.dispatch('login', { token: response.token })
          this.$router.push({ name: 'home' })
        })
        .catch(error => {
          console.log(error.response)
          // TODO: catch error
        })
    }
  }
}
</script>
