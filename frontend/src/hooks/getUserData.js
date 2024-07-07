import Cookies from "js-cookie"
import { jwtDecode } from "jwt-decode"
import axiosInstance from "@/axiosInstance";

import {ref} from "vue";

export default function getUserData() {
    const userData = ref({});
    const payload = jwtDecode(Cookies.get('access'))
    const asyncCall = async () => {
        const response = await axiosInstance.get(`/v1/users/userData/${payload['user_id']}/`, {

            })
        userData.value = response.data;
        return {userData}
    }
    return {asyncCall}


}