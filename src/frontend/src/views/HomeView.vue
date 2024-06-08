<template>
  
  <div class="main">
    <ChatsSidebar></ChatsSidebar>
    <router-view></router-view>
  </div>
</template>

<script>
import {mapActions} from "vuex";
import ChatsSidebar from "@/components/ChatsSidebar";
import getUserData from "@/hooks/getUserData";
import { useStore } from "vuex";
import {onMounted} from "vue";
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
  // onMounted() {
  //   this.$store.dispatch('verifyToken');
  //   this.interval = setInterval(() => {
  //     this.$store.dispatch('verifyToken');
  //   }, 14 * 60 * 1000);
  // },
  // unmounted() {
  //   clearInterval(this.interval);
  // },
  setup() {
    const store = useStore();

    const fetchUserData = async () => {
      const { asyncCall } = getUserData();
      const { userData: fetchedUserData } = await asyncCall();
      store.commit('setUserData', { username: fetchedUserData.value.username,
         id: fetchedUserData.value.id });
    };
    
    onMounted(async () => {
      fetchUserData();
    });

  }
}

</script>

<style scoped>
.main {
  display: flex;
  flex-direction: row;
}
</style>
