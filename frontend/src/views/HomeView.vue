<template>
  
  <div class="main">
    <ChatsSidebar :userData="userData"></ChatsSidebar>
    <router-view></router-view>
  </div>
</template>

<script>
import {mapActions} from "vuex";
import ChatsSidebar from "@/components/ChatsSidebar";
import getUserData from "@/hooks/getUserData";
import getRelatedUsers from "@/hooks/getRelatedUsers"
import cleanChatData from "@/hooks/chatHooks/cleanChatData";
import { useStore } from "vuex";
import {computed, onMounted, ref} from "vue";
export default {
  name: 'HomeView',
  components: {
    ChatsSidebar,
  },

  methods: {
    ...mapActions({
        logout: 'logout'
    }),
  },

  setup() {
    const store = useStore();

    const userData = ref({});
    const chatId = ref(null);

    const fetchUserData = async () => {
      const { asyncCall: getUserDataHook } = getUserData();
      const { userData: fetchedUserData } = await getUserDataHook();
      userData.value = fetchedUserData;
      store.commit('setUserData', { username: fetchedUserData.value.username,
         id: fetchedUserData.value.id });

      const { asyncCall: getRelatedUsersHook } = getRelatedUsers()
      const { relatedUsers } = await getRelatedUsersHook(fetchedUserData.value.username);
  
      relatedUsers.value[0].users.forEach(user => {
        store.dispatch('addRelatedUser', {user: {value: user.username, name: user.name}})
      })

      hubInit()

    };  

    const hubInit = () => {
      hub.value.onmessage = function(e) {
        const data = JSON.parse(e.data)
        if (data.new_users) {
            chatId.value = data.chat.pk
            for (const user of data.new_users) {
                store.dispatch('addUser', {user: user, chatId: chatId.value, chat: data.chat})
            }
        } else if (data.deleted_user) {
            chatId.value = data.chat.pk
            if (store.getters.getUserName !== data.deleted_user.username) {
              store.dispatch('deleteUser', {user: data.deleted_user, chatId: chatId.value});
            }
            if (store.getters.getUserName === data.deleted_user.username) {
                store.commit('deleteChat', {chatId: chatId.value})
            }
        } else if (data.leaved_user) {
            chatId.value = data.chat.pk
            if (store.getters.getUserName !== data.leaved_user.username) {
              store.dispatch('leaveUser', {user: data.leaved_user, chatId: chatId.value});
            }
            if (store.getters.getUserName === data.leaved_user.username) {
                store.commit('deleteChat', {chatId: chatId.value})
            }
        } else if (data.new_chat) {
          if (data.new_chat.current_users.some(currentUser => currentUser.username === store.getters.getUserName)) {
              addChat(data.new_chat)
              store.commit('updateCreateGroupError', {error: ""})
              store.commit('updateCreatePrivateError', {error: ""})
              if (data.new_chat.chat_type === 'P') {
                const newUser = data.new_chat.current_users.find(currentUser => currentUser.username !== store.getters.getUserName);
                store.commit('addRelatedUserMutation', {user: {"name": newUser.name, "value": newUser.username}});
              }
            }
        } else if (data.error && data.chat_type) {
          if (data.chat_type === 'G') {
            store.commit('updateCreateGroupError', {error: data.error[0] || data.error.current_users[0]})
          } else {
            store.commit('updateCreatePrivateError', {error: data.error[0] || data.error.current_users[0]})
          }
        }

      }
    }

    const hub = computed(() => store.getters.getHub)

    const addChat = async (chat) => {
      await cleanChatData(chat)
    }

    onMounted(async () => {
      store.commit('setHub')
      fetchUserData();
    });

    return {userData}
  }
}

</script>

<style scoped>
.main {
  display: flex;
  background-color: rgba(30, 30, 35);
  flex-direction: row;
}
</style>
