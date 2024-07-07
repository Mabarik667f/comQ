import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode";
import axiosInstance from "@/axiosInstance";
import { ref } from 'vue';

export default async function getProfileData() {
    const userData = ref({});
    const payload = jwtDecode(Cookies.get('access'));

    try {
        const response = await axiosInstance.get(`/v1/users/profile/${payload['user_id']}/`, {
        });
        userData.value = response.data;
    } catch (error) {
        console.error(error);
    }

    return { userData };
}
