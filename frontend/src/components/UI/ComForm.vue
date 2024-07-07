<template>
    <form method="post" :class="['form-default', customClass]">
        <slot name="header"></slot>
        <slot name="fields"></slot>
        <slot name="button"></slot>
    </form>
</template>

<script>
export default {
    name: 'com-form',
    props: {
        buttonText: {
            type: String,
            default: 'Подтвердить'
        },
        customClass: {
            type: String
        }
    }
}
</script>

<style scoped>
.form-default{
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    align-content: center;
    justify-content: center;
    align-items: flex-start;
    height: 80vh;
    max-width: 700px;
    margin: 10vh auto;
    box-shadow: 0 0 10px rgba(255, 69, 0, 0.5); 
    border-radius: 20px; 
    padding: 20px;
}
</style>