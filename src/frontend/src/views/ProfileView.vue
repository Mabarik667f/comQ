<script>
import getProfileData from "@/hooks/getProfileData"
import { onMounted, ref } from 'vue';
import changeProfileData from "@/hooks/changeProfileData"
export default {
  setup() {
    const formData = ref({
            img: '',
            status: '',
            name: ''
        })
        
    const user = ref({})
    const setData = async () => {
        const {userData} = await getProfileData();
        user.value = userData.value
        formData.value.img = user.value.img
        formData.value.name = user.value.name
        formData.value.status = user.value.status
    }
    onMounted(async () => {
        await setData()
    })

    const selectImage = (event) => {
            formData.value.img = event.target.files[0];
            changeImage()
        }
        
    const profileData = ref(null)

    const changeImage = async () => {
        const {asyncCall} = changeProfileData(user.value.id)
        profileData.value = await asyncCall({img: formData.value.img})
        user.value.img = profileData.value.profileData.img
    }

    const changeName = async () => {
        const {asyncCall} = changeProfileData(user.value.id)
        profileData.value = await asyncCall({name: formData.value.name})
        user.value.name = profileData.value.profileData.name
        
    }

    const changeStatus = async () => {
        const {asyncCall} = changeProfileData(user.value.id)
        profileData.value = await asyncCall({status: formData.value.status})
        user.value.status = profileData.value.profileData.status
    }

    return {formData, selectImage, changeImage, changeName, changeStatus, user}
  }
}
</script>

<template>
  <div class="profile">
      <RouterLink to="/" class="main-url">Главная</RouterLink>

      <div class="img-container">
          <img :src="user.img" class="img-profile">
          <div class="wrapper">
              <label :for="'img'" class="plus-icon">+</label>
              <com-input class="select-image" @change="selectImage"
              :id="'img'" :type="'file'" accept="image/png, image/jpg, image/jpeg"></com-input>
          </div>
      </div>
      
      <div class="user-data">
          <div>
              <label :for="'username'">Уникальное имя пользователя</label>
              <span class="user-name" :id="'username'">{{ user.username }}</span>
          </div>
          <div>
              <label :for="'name'">Имя</label>
              <span class="" :id="'name'">{{ user.name }}</span>
          </div>
          <div>
              <label :for="'status'">Статус</label>
              <span class="" :id="'status'">{{ user.status }}</span>
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
  color: whitesmoke;
}
.profile {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin: auto;
  align-items: center;
  color: whitesmoke;
  background-color: rgba(30, 30, 45);
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

.form-control:focus {
    border-color: #ccc;
    box-shadow: none;
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
