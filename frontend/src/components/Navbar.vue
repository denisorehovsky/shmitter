<template lang="pug">
  .container
    nav.nav.has-shadow
      .container
        .nav-left
          a.nav-item
            img(src='http://bulma.io/images/bulma-logo.png', alt='Bulma logo')
          a.nav-item.is-tab.is-hidden-mobile.is-active Home
          a.nav-item.is-tab.is-hidden-mobile Features
          a.nav-item.is-tab.is-hidden-mobile Pricing
          a.nav-item.is-tab.is-hidden-mobile About
        span.nav-toggle(@click='showNav = !showNav')
          span
          span
          span
        .nav-right.nav-menu(:class="showNav ? 'is-active' : ''")
          a.nav-item.is-tab.is-hidden-tablet.is-active Home
          a.nav-item.is-tab.is-hidden-tablet Features
          a.nav-item.is-tab.is-hidden-tablet Pricing
          a.nav-item.is-tab.is-hidden-tablet About
          a.nav-item.is-tab
            figure.image.is-16x16.mr1
              img(src='http://bulma.io/images/jgthms.png')
            | Profile
          a.nav-item.is-tab
            | Tweet
          a.nav-item.is-tab(@click='logout') Log out
</template>

<script>
export default {
  name: 'navbar',
  data () {
    return {
      showNav: false
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('logout')
      location.reload()  // reload page after logout
    }
  }
}
</script>
