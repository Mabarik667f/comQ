<script>
import { ref, onUnmounted } from 'vue';

export default {
    name: "com-context-menu",
    props: {
        options: {
            type: Array,
            required: true
        }
    },
    setup() {
        const isVisible = ref(false);
        const x = ref(0);
        const y = ref(0);
        const menuRef = ref(null);

        const openMenu = (event) => {
            x.value = event.clientX;
            y.value = event.clientY;
            isVisible.value = true;
            event.preventDefault();
            document.addEventListener('click', handleClickOutside, true);
        };

        const closeMenu = () => {
            isVisible.value = false;
            document.removeEventListener('click', handleClickOutside, true);
        };

        const handleClickOutside = (event) => {
            if (menuRef.value && !menuRef.value.contains(event.target)) {
                closeMenu();
            }
        };

        const handleActionClick = (action) => {
            action.event();
            closeMenu();
        }
        onUnmounted(() => {
            document.removeEventListener('click', handleClickOutside, true);
        });

        return { isVisible, x, y, openMenu, closeMenu, menuRef, handleActionClick };
    }
};
</script>

<template>
    <div @contextmenu.prevent="openMenu" class="component-container">
        <transition name="context-fade">
        <div ref="menuRef" class="context-menu"
            @click.stop="closeMenu"
            v-show="isVisible"
            :style="{ top: y + 'px', left: x + 'px' }"
            tabindex="-1">
            <div class="menu-inner" @click.stop="closeMenu">
                <ul>
                    <li v-for="option in options"
                     :key="option.value"
                     @click="handleActionClick(option)">
                        {{ option.name }}
                    </li>
                </ul>
            </div>
        </div>
        </transition>
    </div>
</template>

<style scoped>
.component-container {
    position: relative;
}

.context-menu {
    position: fixed;
    z-index: 9999;
    overflow: hidden;
    background: #FFF;
    border-radius: 5px;
    box-shadow: 0 1px 4px 0 #eee;
    padding: 10px;
}

.context-menu:focus {
    outline: none;
}

ul {
    padding: 0;
    margin: 0;
    list-style: none;
}

li {
    padding: 8px 12px;
    cursor: pointer;
}

li:hover {
    background: #eee;
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
