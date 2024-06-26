import axiosInstance from "@/axiosInstance";
import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';
export default function createPrivateChat() {
    const asyncCall = async (formData) => {
        const currentUsers = [];
        
        currentUsers.push(formData.username)
         
        try {
            await axiosInstance.post("/v1/main/create-private/", {
                chat_type: formData.chatType,
                current_users: currentUsers,
                host: jwtDecode(Cookies.get('access'))['user_id']
            })
        } catch (error) {
            console.log(error)
        }
        
        
    }
    return {asyncCall}
}