<script>
import toggleMixin from "@/mixins/toggleMixin"
export default {
    name: 'confirm-win',
    mixins: [toggleMixin]
}
</script>

<template>
    <div class="confirm" v-if="show" @click.stop="hideDialog">
        <div @click.stop class="content">
            <h1>dssadad</h1>
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.confirm {
    border: 1px blue solid;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    background: rgba(0,0,0,0.5);
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
}

.content {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 300px red solid;
}
</style>