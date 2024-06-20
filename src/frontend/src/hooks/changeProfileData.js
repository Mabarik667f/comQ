import axiosInstance from "@/axiosInstance";
import { ref } from 'vue';

export default function changeProfileData(userId) {
    const profileData = ref(null);

    const asyncCall = async (params) => {
        console.log(params)
        try {
        const response = await axiosInstance.patch(`/v1/users/profile/${userId}/`,
        {...params},
        {headers: {"Content-Type": "multipart/form-data"}})

            profileData.value = response.data
            return {profileData}
        } catch (error) {
            console.log(error)
        }
    }

    return {asyncCall}
}