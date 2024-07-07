<script>
import router from '@/router';
import { ref, onMounted, onUnmounted } from 'vue';
export default {
    emits: ["group", "private", "showUpdate"],
    props: {
        show: {
            type: Boolean,
            default: false
        },
        options: {
            type: Object,
            required: true
        },
        position: {
            type: Object
        }
    },
    setup(props, {emit}) {

        const menuRef = ref(null)

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
            emit('showUpdate', false);
        }

        return {handleClick, menuRef};
    }
}
</script>

<template>
    <transition-group name="context-fade">
    <ul class="menu" v-if="show" ref="menuRef" :style="{ top: `${position.top}px`, left: `${position.left}px` }">
        <li v-for="action in options" 
        :key="action.name" class="menu-item" @click="handleClick(action)">
            {{ action.name }}
        </li>
    </ul>
    </transition-group>
</template>

<style scoped>
.menu {
    position: absolute;
    list-style: none;
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