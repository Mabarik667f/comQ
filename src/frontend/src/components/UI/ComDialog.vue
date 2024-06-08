<script>
import toggleMixin from "@/mixins/toggleMixin"
export default {
    name: 'com-dialog',
    mixins: [toggleMixin]
}
</script>

<template>
    <div class="modal" v-if="show" @click.stop="hideDialog">
        <div @click.stop class="modal__content">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.modal {
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    background: rgba(0,0,0,0.5);
    position: fixed;
    display: flex;
}

.modal__content {
    margin: auto;
    border-radius: 12px;
    padding: 20px;
}
</style>