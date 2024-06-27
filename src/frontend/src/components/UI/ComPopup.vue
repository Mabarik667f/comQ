<script>
export default {
    name: 'com-popup',
    props: ['togglePopup'],
    setup() {
    }
}
</script>

<template>
    <div class="popup" @click.stop="togglePopup()">
        <div class="popup-inner" @click.stop>
            <slot></slot>
            <button class="popup-close" @click="togglePopup()">
                Закрыть
            </button>
        </div>
    </div>
</template>

<style scoped>
.popup {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    z-index: 10000;
    background-color: rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
}

.popup-inner {
    padding: 32px;
    background: #FFF;
}

</style>