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
import {onMounted, ref} from "vue";
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
    
    onMounted(async () => {
      fetchUserData();
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
