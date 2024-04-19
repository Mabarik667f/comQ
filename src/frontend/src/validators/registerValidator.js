import { ref } from 'vue';
export default function registerValidator(formData, errors) {
    // более подробная валидация
    const flag = ref(false);
    for (const field in formData) {
        if (!formData[field]) {
            errors.value[field] = "Поле не заполнено";
            flag.value = true;
        }

    }

    return {flag}
}   