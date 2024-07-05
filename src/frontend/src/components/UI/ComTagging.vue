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
        }
    },
    setup(props, {emit}) {

        const currentUsers = ref([])
        watch(() => currentUsers, () => {
            emit("updateCurrentUsers", currentUsers.value)
        }, {deep: true})

        return {currentUsers}
    }
}
</script>

<template>
    <div>
        <label class="typo__label">Добавить</label>
        <multiselect v-model="currentUsers"
            required
            placeholder="Кого добавим?" tag-placeholder="Участник" label="name"
            track-by="value" :options="options"
            :multiple="true" :taggable="true">
        </multiselect>
    </div>
</template>

<style>
.multiselect {
    box-sizing: border-box;
    display: block;
    position: relative;
    width: 100%;
    min-height: 40px;
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
    color: #999;
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
    border: 1px solid #e8e8e8;
    background: #fff;
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
    color: #fff;
    line-height: 1;
    background: #41b883;
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
    color: #266d4d;
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
    border-top: 1px solid #e8e8e8;
}

.multiselect__content-wrapper {
    background-color: rgb(24, 26, 27);
    border-color: currentColor rgb(54, 59, 61) rgb(54, 59, 61);
    position: absolute;
    display: block;
    background: #fff;
    width: 100%;
    max-height: 240px;
    overflow: auto;
    border: 1px solid #e8e8e8;
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
    background: #f3f3f3;
    color: #35495e;
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
