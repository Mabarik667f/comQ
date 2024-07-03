<script>
import router from '@/router';
import { useStore } from 'vuex';
import { ref, onMounted, onUnmounted } from 'vue';
export default {
    emits: ["group", "private", "showUpdate"],
    props: {
        show: {
            type: Boolean,
            default: false
        }
    },
    setup(props, {emit}) {

        const store = useStore();
        const menuRef = ref(null)

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

        const handleOutsideClick = (event) => {
            if (menuRef.value && !menuRef.value.contains(event.target)) {
                emit('showUpdate', false);
            }
        };

        onMounted(() => {
            document.addEventListener('click', handleOutsideClick);
        });

        onUnmounted(() => {
            document.removeEventListener('click', handleOutsideClick);
        });

        const handleClick = (action) => {
            if (action.event) {
                action.event();
            } else {
                router.push(action.to)
            }
        }

        return {actions, handleClick, menuRef};
    }
}
</script>

<template>
    <transition-group name="context-fade">
    <ul class="menu" v-if="show" ref="menuRef">
        <li v-for="action in actions" :key="action.name" class="menu-item" @click="handleClick(action)">
            {{ action.name }}
        </li>
    </ul>
    </transition-group>
</template>

<style scoped>
.menu {
    list-style: none;
    position: absolute;
    top: 5%;
    left: 10%;
    padding: 0;
    margin: 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 15px;
    width: 200px;
    color: whitesmoke;
    background-color: rgb(36, 36, 43);
}
.menu[show] {
    opacity: 1;
    transform: translateY(0);
}

.menu-item {
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    border-radius: 15px;
}

.menu-item:hover {
    background-color: rgba(255, 255, 255, 0.3);
}

.context-fade-enter-active, 
.context-fade-leave-active {
    transition: opacity 0.5s;
}

.context-fade-enter-from,
.context-fade-leave-to {
    opacity: 0;
}
</style>