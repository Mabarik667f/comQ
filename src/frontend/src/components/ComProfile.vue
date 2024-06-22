<script>
import { onMounted, ref, watch } from 'vue';
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
        
        const userData = ref({});
        
        const setData = (user) => {
            userData.value = user
            formData.value.img = user.img
            formData.value.name = user.name
            formData.value.status = user.status
        }
        onMounted(() => {
            setData(props.user)
        })

        watch(() => props.user, (user) => {
            setData(user)
        })

        const selectImage = (event) => {
            formData.value.img = event.target.files[0];
            changeImage()
        }
        
        const profileData = ref(null)

        const changeImage = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({img: formData.value.img})
            userData.value.img = profileData.value.profileData.img
        }

        const changeName = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({name: formData.value.name})
            userData.value.name = profileData.value.profileData.name
            
        }

        const changeStatus = async () => {
            const {asyncCall} = changeProfileData(props.user.id)
            profileData.value = await asyncCall({status: formData.value.status})
            userData.value.status = profileData.value.profileData.status
        }

        return {formData, selectImage, changeImage, changeName, changeStatus, userData}
    }
}
</script>

<template>
    <div class="profile">
        <RouterLink to="/" class="main-url">Главная</RouterLink>

        <div class="img-container">
            <img :src="userData.img" class="img-profile">
            <div class="wrapper">
                <label :for="'img'" class="plus-icon">+</label>
                <com-input class="select-image" @change="selectImage"
                :id="'img'" :type="'file'" accept="image/png, image/jpg, image/jpeg"></com-input>
            </div>
        </div>
        
        <div class="user-data">
            <div>
                <label :for="'username'">Уникальное имя пользователя</label>
                <span class="user-name" :id="'username'">{{ userData.username }}</span>
            </div>
            <div>
                <label :for="'name'">Имя</label>
                <span class="" :id="'name'">{{ userData.name }}</span>
            </div>
            <div>
                <label :for="'status'">Статус</label>
                <span class="" :id="'status'">{{ userData.status }}</span>
            </div>

        </div>

        <div class="info-container">
            <div class="form-group mb-3">
                <label class="name" :for="'name'">Имя</label>
                <div class="input-group">
                    <com-input v-model="formData.name" class="form-control profile-input" :id="'name'"></com-input>
                    <com-button @click="changeName()">Изменить</com-button>
                </div>
            </div>

            <div class="form-group mb-3">
                <label class="name" :for="'name'">Статус </label>
                <div class="input-group">
                    <com-input v-model="formData.status" class="form-control profile-input" :id="'status'"></com-input>
                    <com-button @click="changeStatus()">Изменить</com-button> 
                </div>       
            </div>
        </div>

    </div>
</template>

<style scoped>

.main-url {    
    font-weight: bold;
    margin-top: 20px;
    text-decoration: none;
    color: black;
}
.profile {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: auto;
    align-items: center;
    width: 100%;
}

.user-data {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.user-data div {
    display: flex;
    flex-direction: column;
    margin: 5px 0;
    padding: 5px;
}

.user-data div label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
}

.user-data div span {
    display: block;
}
.img-profile {
    border-radius: 50%;
    width: 100%;
    height: 100%;
    object-fit: fill;
}

.img-container {
    position: relative;
    width: 200px;
    height: 200px;
    margin: 30px 0;
}

.profile-input {
    max-width: 400px;
}

.wrapper {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
}

.img-container:hover .wrapper{
    opacity: 1;
}
.select-image {
    display: none;
}

.plus-icon {
    color: white;
    font-size: 50px;
    cursor: pointer;
}

.change-image {
    display: none;
    border-radius: 50%;
    padding: 10px;
}

.info-container {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
}
</style>