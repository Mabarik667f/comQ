<script>
import ComProfile from '@/components/ComProfile';
import getProfileData from "@/hooks/getProfileData"
import refresh from "@/hooks/refresh"

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
      setInterval(() => {
        refresh();
      }, 14 * 60 * 1000); 
    })

    return {user}
  }
}
</script>

<template>
    <ComProfile :user="user"></ComProfile>  
</template>

<style scoped>

</style>
