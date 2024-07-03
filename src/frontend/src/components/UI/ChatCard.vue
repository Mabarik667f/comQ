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

      // const card = ref(null)
      // const sidebarWidth = computed(() => store.getters.getSidebarWidth)
      // const truncatedMessage = ref("");

      // const updateTruncatedMessage = () => {
      //   if (!card.value) {
      //     truncatedMessage.value = chat.value.last_message.text_content;
      //     return
      //   }

      //   const maxCharsPerWidth = 20;
      //   const maxMessageLength = Math.floor(card.value.clientWidth / maxCharsPerWidth);
      //   const text = chat.value.last_message.text_content;

      //   if (text.length> maxMessageLength) {
      //     truncatedMessage.value = text.slice(0, maxMessageLength) + '...';
      //   } else {
      //     truncatedMessage.value = text;
      //   }
      // };

      // watchEffect(() => {
      //   updateTruncatedMessage();
      // });

      // watch(sidebarWidth, () => {
      //   updateTruncatedMessage();
      // }, {immediate: true});
    
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
        <label :for="'msg-text'" v-if="chat.last_message.user && chat.chat_type === 'G'">{{ chat.last_message.user.name }}: </label>
        <p :id="'msg-text'" class="message">{{chat?.last_message.text_content}}</p>
      </div>
    </div>
    <div class="notifications">
      {{ chat.notifications }}
    </div>
  </div>
</template>

<style scoped>
.chat-card {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: space-evenly;
}

.card-img {
  max-width: 65px;
  align-items: center;
  margin-right: 10px;
  margin-left: 5px;
}

.chat-info {
  flex-grow: 1;
}

.chat-title {
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
  text-align: center;
  margin-right: 5px;
}

.last-message {
  display: flex;
  flex-direction: row;
}

.message {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 70px;
}
</style>
