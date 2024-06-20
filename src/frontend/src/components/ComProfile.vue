<script>
import { ref } from 'vue';
import changeProfileData from "@/hooks/changeProfileData"
export default {
    props: {
        user: {
            require: true
        }
    },
    setup(props) {
        const formData = ref({
            img: '',
            status: '',
            name: ''
        })

        const selectImage = (event) => {
            formData.value.img = event.target.files[0];
        }
        
        const profileData = ref(null)

        const changeImage = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({img: formData.value.img})
        }

        const changeName = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({name: formData.value.name})
        }

        const changeStatus = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({status: formData.value.status})
        }

        return {formData, selectImage, changeImage, changeName, changeStatus}
    }
}
</script>

<template>
    <div class="profile">
        <img :src="user.img" class="img-profile">
        <com-input class="form-control" @change="selectImage"
        :id="'img'" :type="'file'" accept="image/png, image/jpg, image/jpeg"></com-input>
        <com-button @click="changeImage()">Изменить</com-button>

        <span class="name">{{ user.name }}</span>
        <com-input v-model="formData.name" class="form-control" :id="'name'"></com-input>
        <com-button @click="changeName()">Изменить</com-button>

        <span class="status">{{ status }}</span>

        <div class="user-status-block">
            <label>&#9432;</label>
            <span class="user-status">{{ user.status }}</span>
            <com-input v-model="formData.status" class="form-control" :id="'status'"></com-input>
            <com-button @click="changeStatus()">Изменить</com-button>

        </div>
        <div class="user-name-block">
            <label>Username: </label>
            <span class="user-name">{{ user.username }}</span>
        </div>
    </div>
</template>

<style scoped>

.profile {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: auto;
    align-items: center;
}

.img-profile {
    border-radius: 50%;
    width: 200px;
}
</style>