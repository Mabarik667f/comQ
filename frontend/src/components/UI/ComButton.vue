<template>
 <button :class="{'btn': true, 'btn-primary': true, 'com__btn': orange, 'no-bg': !orange}" :type="type">
    <slot></slot>
 </button>
</template>

<script>
export default {
    name: "com-button",
    props: {
        type: {
            type: String,
            default: 'submit'
        },
        orange: {
            type: Boolean,
            default: true
        }
    }
}
</script>

<style scoped>

.com__btn {
    --bs-btn-color: #fff;
    --bs-btn-bg: orangered;
    --bs-btn-border-color: orangered;
    --bs-btn-hover-color: #fff;
    --bs-btn-hover-bg: rgb(240, 70, 8);
    --bs-btn-hover-border-color: rgb(240, 70, 8);
    --bs-btn-focus-shadow-rgb: 49, 132, 253;
    --bs-btn-active-color: #fff;
    --bs-btn-active-bg: orangered;
    --bs-btn-active-border-color: orangered;
    --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
    --bs-btn-disabled-color: #fff;
    --bs-btn-disabled-bg: orangered;
    --bs-btn-disabled-border-color: orangered;
    cursor: pointer;
}

.no-bg {
    background-color: transparent !important;
    border: none !important;
    cursor: pointer;
    --bs-btn-hover-bg: transparent !important;
    --bs-btn-hover-border-color: transparent !important;
    --bs-btn-active-bg: transparent !important;
    --bs-btn-active-border-color: transparent !important;
    --bs-btn-disabled-bg: transparent !important;
    --bs-btn-disabled-border-color: transparent !important;
    --bs-btn-focus-shadow-rgb: inherit;
}
</style>