<script>
import { ref } from 'vue';
import changeGroupSettings from "@/hooks/chatHooks/changeGroupSettings"
export default {
    props: {
        groupSettings: {
            require: true
        },
        img: {
            require: true
        }
    },
    setup(props) {
        const showUpload = ref(false)
        
        const formData = ref({
            title: '',
            avatar: ''
        })
        const updateImage = async () => {
            const {asyncCall} = changeGroupSettings();
            const {newData} = await asyncCall({avatar: formData.value.avatar,
                                               groupSettings: parseInt(props.groupSettings)})
            console.log(newData)
        }

        const updateTitle = async () => {
            const {asyncCall} = changeGroupSettings();
            const {newData} = await asyncCall({title: formData.value.title,
                                               groupSettings: parseInt(props.groupSettings)})
            console.log(newData)
        }
        
        const handleImageChange = (event) => {
            formData.value.avatar = event.target.files[0]
            console.log(formData.value.avatar)
        }

        return {showUpload, formData, updateImage, updateTitle, handleImageChange}
    }
}
</script>

<template>
    <!-- <div class="image-container" @mouseover="showUpload=true" @mouseout="showUpload=false">
        <com-input type="file"  class="file-input"></com-input>
        <com-button v-if="showUpload" class="upload-button">Изменить</com-button>
        <img :src="img" class="image-content">
    </div> -->
    <div class="image-container">
        <com-input type="file" class="file-input" @change="handleImageChange"></com-input>
        <com-button class="upload-button" @click="updateImage()">Изменить</com-button>
        <img :src="img" class="image-content">
    </div>
    <div>
        <label :for="'title'">Название: </label>
        <com-input :id="'title'" v-model="formData.title"></com-input>
        <com-button @click="updateTitle()">Изменить Название</com-button>
    </div>
</template>

<style scoped>
.image-content {
    width: 200px;
    border-radius: 50%;
}
/* .file-input {
    display: none;
} */

.image-container:hover .upload-button {
    display: block;
}

/* .upload-button {
    position: absolute;
}

.image-container{
    position: relative;
    display: inline-block;
} */
</style>