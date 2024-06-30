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
import { useStore } from "vuex";
import refresh from "@/hooks/refresh"
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

    const userData = ref();
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

    };  

    const hub = computed(() => store.getters.getHub)

    hub.value.onmessage = function(e) {
        const data = JSON.parse(e.data)

        console.log(data)
        const chatId = ref(data.chat.pk)
        if (data.new_users) {
            console.log(data.new_users)
            for (const user of data.new_users) {
                store.dispatch('addUser', {user: user, chatId: chatId.value, chat: data.chat})
            }
        } else if (data.deleted_user) {
            if (store.getters.getUserName !== data.deleted_user.username) {
              store.dispatch('deleteUser', {user: data.deleted_user, chatId: chatId.value});
            }
            if (store.getters.getUserName === data.deleted_user.username) {
                store.commit('deleteChat', {chatId: chatId.value})
            }
        } else if (data.leaved_user) {
            if (store.getters.getUserName !== data.leaved_user.username) {
              store.dispatch('leaveUser', {user: data.leaved_user, chatId: chatId.value});
            }
            if (store.getters.getUserName === data.leaved_user.username) {
                store.commit('deleteChat', {chatId: chatId.value})
            }
        } 

    }

    onMounted(async () => {
      fetchUserData();
      setInterval(() => {
        refresh();
      }, 14 * 60 * 1000); 
    });

    return {userData}
  }
}

</script>

<style scoped>
.main {
  display: flex;
  flex-direction: row;
}
</style>
