import axiosInstance from "@/axiosInstance";
import { ref } from "vue";

export default function changeGroupSettings () {
    const asyncCall = async (params) => {
        const data = {}
        const newData = ref({})
        console.log(params)
        if (params.avatar) {
            data.avatar = params.avatar
        }
        if (params.title) {
            data.title = params.title
        }
        try {
            const response = await axiosInstance.patch(`/v1/main/group-settings/${params.groupSettings}/`,
                {...data},
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            )

            newData.value = response.data 
            return {newData}
        } catch (error) {
            console.log(error)
        }
    }

    return {asyncCall}
}