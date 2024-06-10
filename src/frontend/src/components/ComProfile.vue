<script>
export default {
    props: {
        user: {
            require: true
        }
    },

    data() {
        return {
            name: "Aboba",
            status: 'online',
            userStatus: 'lox',
            userName: "@bibus",
        }
    },
    setup() {
 
    }
}
</script>

<template>
    <div class="profile">
        <span class="name">{{ user.name }}</span>
        <span class="status">{{ status }}</span>
        <div class="user-status-block">
            <label>&#9432;</label>
            <span class="user-status">{{ user.status }}</span>
        </div>
        <div class="user-name-block">
            <label>Username: </label>
            <span class="user-name">{{ user.username }}</span>
        </div>
    </div>
</template>

<style scoped>

.profile {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: auto;
    align-items: center;
}
</style>