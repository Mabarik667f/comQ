<script>
import { ref, onUnmounted, nextTick } from 'vue';

export default {
    name: "context-menu",
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
        const menuWidth = ref(null);
        const menuHeight = ref(null);
        const windowWidth = ref(null);
        const windowHeight = ref(null);
        const menuRef = ref(null);

        const openMenu = async (event) => {
            x.value = event.clientX;
            y.value = event.clientY;

            isVisible.value = true;
            event.preventDefault();

            await nextTick()

            menuWidth.value = menuRef.value.offsetWidth + 4;
            menuHeight.value = menuRef.value.offsetHeight + 4;

            windowHeight.value = window.innerHeight;
            windowWidth.value = window.innerWidth;

            if ((windowWidth.value - x.value) < menuWidth.value) {
                menuRef.value.style.left = windowWidth.value - menuWidth.value + "px"
            } else {
                menuRef.value.style.left = x.value + "px"
            }
            
            if ((windowHeight.value - y.value) < menuHeight.value) {
                menuRef.value.style.top = windowHeight.value - menuHeight.value + "px"
            } else {
                menuRef.value.style.top = y.value + "px"
            }

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
    background-color: rgb(36, 36, 43);
    border-radius: 5px;
    padding: 10px;
    color: whitesmoke;
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
    border-radius: 5px;
}

li:hover {
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 5px;
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
