<template>
  <div class="main">
    <com-button
    @click="$router.push('/register')">Зарегистрироваться</com-button>
    <com-button
    @click="$router.push('/login')">Войти</com-button>
  </div>
</template>

<script>

export default {
  name: 'HomeView',
  
}
</script>

<style scoped>

</style>
