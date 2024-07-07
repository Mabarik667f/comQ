import { ref } from 'vue';
export default async function baseValidator(formData, errors) {
    
    const flag = ref(false);
    for (const field in errors.value) {
        errors.value[field] = '';
    }
    
    for (const field in formData) {
        if (!formData[field]) {
            errors.value[field] = "Поле не заполнено";
            flag.value = true;
        }

    }

    return {flag}
}   