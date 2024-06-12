<script>
import { ref, toRefs } from 'vue';
export default {
  name: "chat-card",
  props: {
    chat: {
      default: Object,
      required: true
    }
  },
  setup(props) {
    const {chat} = toRefs(props);
    const chatImg = ref('');
    if (chat.value.chat_type === 'G') {
      chatImg.value = chat.value.groupSettings.group_settings.avatar
    }
    else {
      chatImg.value = chat.value.partner.img;
    }
    return {chatImg}
  }
}
</script>

<template>
  <div>
      <div>
            <img :src="chatImg" class="short-chat-img">
      </div>
      <div>
        {{ chat.notifications }}
        {{ chat.partner }}
        {{ chat.groupSettings }}
       
            <label v-if="chat.chat_type === 'P'">
              PRIVATE</label>
            <label>{{ chat.title }}</label>
            <div>{{ chat.last_message }}</div>
            
            
      </div>
        
 
  </div>
</template>

<style scoped>
.short-chat-img {
  width: 65px;
  border-radius: 50%;
}
</style>
