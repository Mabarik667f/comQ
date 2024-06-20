<script>
import ComProfile from '@/components/ComProfile';
import getProfileData from "@/hooks/getProfileData"
import { onMounted, ref } from 'vue';
export default {
  components: {
    ComProfile,
  },
  setup() {
    const user = ref({});
    onMounted(async () => {
      const {userData} = await getProfileData();
      user.value = userData.value;
    })
    return {user}
  }
}
</script>
<template>
  <div class="profile">
    <ComProfile :user="user"></ComProfile>
    {{ userData }}
  </div>
</template>

<style scoped>
.profile{
  display: flex;
  flex-direction: row;
}
</style>
