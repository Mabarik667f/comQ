import axiosInstance from "@/axiosInstance";
import { ref } from "vue";
/**
 * Функция возвращает данные о чате для отрисовки в sidebar-е
 * @param {*} data 
 * @returns 
 */
export default async function getChatCardData(data) {

    const chatData = ref({});
    try {
        if (typeof(data) == "string") {
            const response = await axiosInstance.get(`/v1/users/userOnChat/${data}`, {
            })
            chatData.value = response.data
        } else {
            const response = await axiosInstance.get(`/v1/main/group-chat-detail/${data}/`, {
            })
            chatData.value = response.data
        }
    } catch{(error) => {
        console.log(error)
    }}

    return {chatData}
}