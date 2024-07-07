import axiosInstance from "@/axiosInstance";
export default function changeRole() {
    const asyncCall = async (role, user, group_settings) => {
        try {
            await axiosInstance.patch("/v1/main/group-settings-has-user/", {
                role: role,
                group_settings: group_settings,
                user: user
            })
        } catch (error) {
            console.log(error)
        }
        
        
    }
    return {asyncCall}
}