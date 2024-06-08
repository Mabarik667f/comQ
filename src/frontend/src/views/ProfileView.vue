<script>
import ComProfile from '@/components/ComProfile';
import getProfileData from "@/hooks/getProfileData"
export default {
  components: {
    ComProfile
  },
  setup() {
    const {userData} = getProfileData();
    return {userData}
  }
}
</script>
<template>
  <div>
    <ComProfile :user="userData"></ComProfile>
    {{ userData }}
  </div>
</template>
