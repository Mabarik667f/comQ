<script>
import Multiselect from 'vue-multiselect'
import { ref, watch } from 'vue'
export default {
    name: 'com-tagging',
    components: {
        Multiselect
    },
    props: {
        modelValue: {
            required: true,
            type: Array
        },
        options: {
            type: Object,
            required: true
        },
        isChat: {
            type: Boolean,
            default: false
        }
    },
    setup(props, {emit}) {

        const currentUsers = ref([])

        const addUserToRommHook = () => {
            emit('addUserToRommHook')
            currentUsers.value = [];
        }
        watch(() => currentUsers, () => {
            emit("updateCurrentUsers", currentUsers.value)
        }, {deep: true})

        return {currentUsers, addUserToRommHook}
    }
}
</script>

<template>
    <div>
        <label class="typo__label">Добавить</label>
        <div class="tagging-wrapper">
        <multiselect v-model="currentUsers"
            required
            placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
            track-by="value" :options="options"
            :multiple="true" :taggable="true">
        </multiselect>
        <transition name="button-fade">
            <div v-if="isChat && currentUsers.length >= 1">
                <com-button @click=addUserToRommHook()
            >Добавить</com-button>
            </div>
        </transition>
        </div>
    </div>
</template>

<style>

.button-fade-enter-active, .button-fade-leave-active {
    transition: opacity 0.5s;
}
.button-fade-enter-from, .button-fade-leave-to {
    opacity: 0;
}

.tagging-wrapper {
    display: flex;
    align-items: center; 
    justify-content: space-between;
    margin-top: 5px;
}

.multiselect {
    box-sizing: border-box;
    display: block;
    position: relative;
    min-width: 50px;
    min-height: 40px;
    width: 250px;
    text-align: left;
    color: whitesmoke;
}

.multiselect__select {
    line-height: 16px;
    display: block;
    position: absolute;
    box-sizing: border-box;
    width: 40px;
    height: 38px;
    right: 1px;
    top: 1px;
    padding: 4px 8px;
    margin: 0;
    text-align: center;
    cursor: pointer;
    transition: transform .2s ease;
}

.multiselect__select::before {
    position: relative;
    right: 0;
    top: 65%;
    margin-top: 4px;
    border-style: solid;
    border-width: 5px 5px 0 5px;
    border-color: #999 transparent transparent transparent;
    content: "";
}

.multiselect__tags {
    min-height: 40px;
    display: block;
    padding: 8px 40px 0 8px;
    border-radius: 5px;
    border: 1px solid rgba(30, 30, 45);
    background: rgb(36, 36, 43);
    font-size: 14px;
}

.multiselect__tags-wrap {
    display: inline;
}

.multiselect__tag {
    position: relative;
    display: inline-block;
    padding: 4px 26px 4px 10px;
    border-radius: 5px;
    margin-right: 10px;
    line-height: 1;
    background: orangered;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    max-width: 100%;
    text-overflow: ellipsis;
}

.multiselect__tag-icon {
    cursor: pointer;
    margin-left: 7px;
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    font-weight: 700;
    width: 22px;
    text-align: center;
    line-height: 22px;
    transition: all .2s ease;
    border-radius: 5px;
}

.multiselect__tag-icon::after {
    content: "×";
    color: rgba(30, 30, 45);
    font-size: 14px;
}

.multiselect__input {
    display: none;
}

.multiselect--above .multiselect__content-wrapper {
    border-bottom-color: currentColor;
    border-top-color: rgb(54, 59, 61);
}

.multiselect--above .multiselect__content-wrapper {
    bottom: 100%;
    border-radius: 5px 5px 0 0;
    border-bottom: none;
}

.multiselect__content-wrapper {
    background-color: rgb(36, 36, 43);
    border-color: currentColor rgba(30, 30, 45) rgba(30, 30, 45);
    position: absolute;
    display: block;
    width: 100%;
    max-height: 240px;
    overflow: auto;
    border: 1px solid rgba(30, 30, 45);
    border-top: none;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    z-index: 50;
    -webkit-overflow-scrolling: touch;
}

.multiselect__content {
    list-style: none;
    display: inline-block;
    padding: 0;
    margin: 0;
    min-width: 100%;
    vertical-align: top;
}

.multiselect__option--selected {
    background-color: rgb(31, 33, 35);
    color: rgb(166, 187, 205);
}

.multiselect__option {
    text-decoration-color: currentColor;
}

.multiselect__option--selected {
    background: orangered;
    font-weight: 700;
}

.multiselect__option {
    display: block;
    padding: 12px;
    min-height: 40px;
    line-height: 16px;
    text-decoration: none;
    vertical-align: middle;
    position: relative;
    cursor: pointer;
    white-space: nowrap;
}
</style>
