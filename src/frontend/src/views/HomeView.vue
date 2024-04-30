<template>
  <div class="main">
    <com-button
    @click="$router.push('/register')">Зарегистрироваться</com-button>
    <com-button
    @click="$router.push('/login')">Войти</com-button>
    <com-button @click.prevent="logout">Выйти</com-button>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

export default {
  name: 'HomeView',

  methods: {
    ...mapActions({
            logout: 'logout'
    })
  }
}

</script>

<style scoped>

</style>
