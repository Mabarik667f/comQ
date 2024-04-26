import router from '@/router';
import axios from 'axios';
import {baseHeaders} from "@/headers/baseHeaders";
import {ref} from "vue";

export default async function register(formData) {
    let response;
    const updatedErrors = ref({});
    try {
        response = await axios.post('/v1/users/register/', {
            email: formData.email,
            username: formData.username,
            password: formData.password,
            password2: formData.password2
        },
        {
            headers: {
                ...baseHeaders
            }
        })
        if (response.status === 201 && response.statusText === 'Created'){
            router.push('/login');
        }
        
        return {}
    } catch (error){
        console.log(error);
        const responseData = error.response.data;
        for (let key in responseData) {
            updatedErrors.value[key] = [];
        }
        for (let key in responseData) {
            updatedErrors.value[key] = responseData[key];
        }
        return updatedErrors;
    }
    
}