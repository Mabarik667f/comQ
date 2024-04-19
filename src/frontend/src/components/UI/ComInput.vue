<template>
    <input 
    :type="type"
    @input="$emit('update:modelValue', $event.target.value)"
    :id="id">
</template>

<script>
export default {
    name: "com-input",
    props: {
        modelValue: {
            type: [String, Number],
            default: ''
        },
        type: {
            type: String,
            default: 'text'
        },
        id: {
            type: String,
            required: true
        },
    }
}
</script>

<style scoped>

</style>