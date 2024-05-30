<script>
export default {
  name: "chat-card",
  props: {
    chat: {
      default: Object,
      required: true
    }
  },
  methods: {
    openChat() {
      console.log(1);
    }
  }
}
</script>

<template>
  <div @click="openChat">
     
      <div>
            <img src="defaultChat.jpg" class="chat-img">
      </div>
      <div>
            <label>{{ chat.title }}</label>
            <div>{{ chat.lastMessage }}</div>
      </div>
        
 
  </div>
</template>

<style scoped>
  
</style>
