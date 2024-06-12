<script>
import { ref } from 'vue';

export default {
    setup() {
        const formData = ref({
            img: '',
            status: '',
            name: ''
        })
        // type file check, validation, hook
        return {formData}
    }
}
</script>

<template>
    <com-form>
        <template v-slot:header>
            <h3>Изменить данные о себе</h3>
        </template>
        <template v-slot:fields>
            <label :for="'img'">Аватар</label>
            <com-input v-model="formData.img" class="form-control"
             :id="'img'" :type="'file'" accept="image/png, image/jpg, image/jpeg" required></com-input>
            <label :for="'status'">Статус</label>
            <com-input v-model="formData.status" class="form-control" :id="'status'" required></com-input>
            <label :for="'name'">Имя</label>
            <com-input v-model="formData.name" class="form-control" :id="'name'" required></com-input>
        </template>
        <template v-slot:button>
            <com-button>Изменить</com-button>
        </template>
    </com-form>
</template>

<style scoped>

</style>