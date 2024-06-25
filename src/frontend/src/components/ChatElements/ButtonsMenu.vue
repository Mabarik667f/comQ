<script>
import router from '@/router';
import { useStore } from 'vuex';
import { ref } from 'vue';
import toggleMixin from '@/mixins/toggleMixin';
export default {
    mixins: [toggleMixin],
    emits: ["group", "private"],
    setup(props, {emit}) {

        const store = useStore();

        const showPrivateDialog = () => {
            emit("private", true);
        }

        const showGroupDialog = () => {
            emit("group", true);
        }

        const logout = () => {
            store.dispatch("logout");
        }

        const actions = ref([
            {"name": 'Профиль', "to": '/profile'},
            {"name": "Новая группа", "event": showGroupDialog},
            {"name": "Новый чат", "event": showPrivateDialog},
            {"name": 'Выйти', "event": logout}
        ])

        const handleClick = (action) => {
            if (action.event) {
                action.event();
            } else {
                router.push(action.to)
            }
        }

        return {actions, handleClick}
    }
}
</script>

<template>
    <ul class="menu" v-if="show" @click.self="hideDialog">
        <li v-for="action in actions" :key="action.name" class="menu-item" @click="handleClick(action)">
            {{ action.name }}
        </li>
    </ul>
</template>

<style scoped>
.menu {
    list-style: none;
    position: absolute;
    top: 5%;
    left: 10%;
    padding: 0;
    margin: 0;
    border: 1px solid blue;
    width: 200px;
}
.menu[show] {
    opacity: 1;
    transform: translateY(0);
}

.menu-item {
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.menu-item:hover {
    background-color: #f5f5f5;
}
</style>