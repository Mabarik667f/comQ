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
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}

.popup-inner {
    position: relative;
    padding: 32px;
    background: rgb(36, 36, 43);
    color: whitesmoke;
    border-radius: 20px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 10%;
}

</style>