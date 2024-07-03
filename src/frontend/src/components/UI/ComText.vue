<script>
export default {
    name: 'com-text',
    props: {
        modelValue: {
            type: [String, Number],
            default: ''
        },
        rows: {
            type: Number,
            default: 1
        }
    }
}
</script>

<template>
    <textarea class="form-control com-text" :rows="rows"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)">

    </textarea>
</template>

<style scoped>
.com-text {
    overflow-y: scroll;
    resize: none;
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

.com-text:focus {
    background-color: rgb(36, 36, 43);
    border: 1px solid rgba(30, 30, 45);
    color: whitesmoke;
    cursor: text;
}

.com-text::placeholder {
    color: whitesmoke;
    opacity: 0.4;
}

.form-control:focus {
    border-color: #a3a1a1;
    box-shadow: none;
}
</style>