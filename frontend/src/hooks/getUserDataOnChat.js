import axiosInstance from "@/axiosInstance";

import { ref } from "vue";
/**
 * Функция возвращает данные о пользователе в чате
 * @param {*} data 
 * @returns 
 */
export default async function getUserDataOnChat(name) {

    const userData = ref({});
    try {
        const response = await axiosInstance.get(`/v1/users/userOnChat/${name}`, {
        })

        userData.value = response.data;
    } catch {(error) => {
        console.log(error);
    }}


    return {userData}
}