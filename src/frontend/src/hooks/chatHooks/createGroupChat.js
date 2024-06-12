import axiosInstance from "@/axiosInstance";
import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';
export default function createGroupChat() {
    const asyncCall = async (formData) => {
        const currentUsers = [];
        for (let user of formData.currentUsers) {
            currentUsers.push(user.value);
        } 
            
        try {
            await axiosInstance.post("/v1/main/create-group/", {
                chat_type: formData.chatType,
                current_users: currentUsers,
                host: parseInt(jwtDecode(Cookies.get('access'))['user_id']),
                title: formData.title
            })
        } catch (error) {
            console.log(error)
        }
        
        
    }
    return {asyncCall}
}