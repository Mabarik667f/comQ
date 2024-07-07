import axiosInstance from "@/axiosInstance";
import { ref } from "vue";
export default function getRelatedUsers() {
    const relatedUsers = ref();
    const asyncCall = async (username) => {
    
        try {
            const response = await axiosInstance.get(`/v1/users/related-users/${username}`);

            relatedUsers.value = response.data

            return {relatedUsers};
            
        } catch (error) {
            console.log(error)
        }
    }

    return {asyncCall}
}