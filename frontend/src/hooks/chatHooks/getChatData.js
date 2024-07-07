import axiosInstance from "@/axiosInstance";

import { ref } from "vue";

/**
 * Получает контент из чата
 * @param {*} pk 
 * @returns
 */
export default async function getChatData(pk) {
    const chatData = ref({});

    try{
        const response = await axiosInstance.get(`/v1/main/chat-detail/${pk}/`, {
        })
        chatData.value = response.data;
    }
    catch{(error) => {
        console.log(error)
    }}

    return {chatData}
}