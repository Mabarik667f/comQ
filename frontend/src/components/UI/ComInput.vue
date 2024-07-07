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
input {
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

input:focus {
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

input::placeholder {
    color: whitesmoke;
    opacity: 0.4;
}
</style>