import axiosInstance from "@/axiosInstance";
import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';
import { ref } from "vue";
export default function createPrivateChat() {
    const asyncCall = async (formData) => {
        const currentUsers = [];
        currentUsers.push(formData.username)
        const chat = ref();
         
        try {
            const response = await axiosInstance.post("/v1/main/create-private/", {
                chat_type: formData.chatType,
                current_users: currentUsers,
                host: jwtDecode(Cookies.get('access'))['user_id']
            })
            chat.value = response.data;
            return {chat}
        } catch (error) {
            return error.response.data
        }
        
        
    }
    return {asyncCall}
}