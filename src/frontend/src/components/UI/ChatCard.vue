<script>
import { computed, ref, watch } from 'vue';
import { useStore } from 'vuex';
export default {
  name: "chat-card",
  props: {
    chat: {
      default: Object,
      required: true
    }
  },
  setup(props) {
      const store = useStore();
      const chat = computed(() => store.getters.getChat(props.chat.pk));

      const chatData = ref({
        chatImg: '',
      })


      watch(() => (chat.value?.groupSettings?.avatar), async (newAvatar) => {
        chatData.value.chatImg = newAvatar;
        
      }, {deep: true})


      if (chat.value.chat_type === 'G') {
          chatData.value.chatImg = chat.value?.groupSettings?.avatar
      } else {
          chatData.value.chatImg = chat.value?.partner?.img;
      }
    
    return {chatData}
  }
}
</script>

<template>
  <div class="chat-card">
    <div class="card-img">
      <img v-if="chatData.chatImg" :src="chatData.chatImg" class="short-chat-img">
    </div>
    <div class="chat-info">
      <span v-if="chat.chat_type === 'P' && chat.partner" class="chat-title">
        {{ chat.partner?.name || "Загрузка..." }}
      </span>
      <span v-else-if="chat.chat_type === 'G' && chat.groupSettings" class="chat-title">
        {{ chat.groupSettings?.title || "Загрузка..." }}
      </span>
      <div class="last-message">
        <label :for="'msg-text'" v-if="chat?.last_message?.user && chat.chat_type === 'G' && !chat?.last_message.system">{{ chat.last_message.user.name }}:</label>
        <div :id="'msg-text'" class="message">{{chat?.last_message.text_content}}</div>
      </div>
    </div>
    <div class="notifications" v-if="chat?.notifications > 0">
      {{ chat?.notifications }}
    </div>
  </div>
</template>

<style scoped>
.chat-card {
  display: flex;
  flex-direction: row;
  align-content: center;
  align-items: center;
  justify-content: space-evenly;
  margin-bottom: 10px;
}

.card-img {
  max-width: 65px;
  align-items: center;
  margin-right: 10px;
  margin-left: 5px;
}

.chat-info {
  flex-grow: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.short-chat-img {
  width: 65px;
  height: 65px;
  border-radius: 50%;
}

.notifications {
  align-self: center;
  border-radius: 50%;
  background-color: orangered;
  width: 30px;
  height: 30px;
  text-align: center;
  line-height: 30px;
  color: white;
  font-weight: bold;
  flex-shrink: 0;
  margin-left: 10px;
}

.last-message {
  display: flex;
  flex-direction: row;
  overflow: hidden;
}

.message {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-left: 3px;
  width: 100%;
  flex-grow: 1;
}
</style>
