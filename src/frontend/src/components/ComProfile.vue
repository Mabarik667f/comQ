<script>
export default {
    data() {
        return {
            name: "Aboba",
            status: 'online',
            userStatus: 'lox',
            userName: "@bibus",
        }
    }
}
</script>

<template>
    <div class="profile">
        <img src="../assets/default/defaultChat.jpg" style="width: 300px;">
        <span class="name">{{ name }}</span>
        <span class="status">{{ status }}</span>
        <div class="user-status-block">
            <label>&#9432;</label>
            <span class="user-status">{{ userStatus }}</span>
        </div>
        <div class="user-name-block">
            <label>Username</label>
            <span class="user-name">{{ userName }}</span>
        </div>
    </div>
</template>

<style scoped>

.profile {
    display: flex;
    flex-direction: column;
}
</style>