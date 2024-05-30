<template>
    <input 
    :type="type"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :id="id"
    required>
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