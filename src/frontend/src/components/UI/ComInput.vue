<template>
    <input 
    :type="type"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :id="id"
    :placeholder="placeholder"
    >
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
        },
        placeholder: {
            type: String
        }
    }
}
</script>

<style scoped>

</style>