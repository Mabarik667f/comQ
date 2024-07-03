<script>
import { computed, ref, watch, onMounted } from 'vue';
import changeGroupSettings from "@/hooks/chatHooks/changeGroupSettings"
import isAdmin from "@/hooks/permissionHooks/isAdmin"

import { useStore } from 'vuex';
export default {
    props: {
        groupSettings: {
            require: true
        },
        chatId: {
            type: Number,
            required: true
        }
    },
    setup(props) {
        const showUpload = ref(false)
        const store = useStore();
        
        const chatId = ref(props.chatId);
        const chatData = computed(() => store.getters.getChat(chatId.value));

        const avatarWatch = watch(
            () => chatData.value.groupSettings ? chatData.value.groupSettings.avatar : null,
            (newAvatar) => {
                if (chatData.value.groupSettings) {
                    chatData.value.groupSettings.avatar = newAvatar;
                }
            },
            { immediate: true }
        );
        

        const formData = ref({
            title: '',
            avatar: ''
        })
        const updateImage = async () => {
            const {asyncCall} = changeGroupSettings();
            const {newData} = await asyncCall({avatar: formData.value.avatar,
                                               groupSettings: parseInt(props.groupSettings.id)})
            store.commit('updateGroupAvatar', {chatId: chatId.value, avatar: newData.value.avatar})

        }

        const updateTitle = async () => {
            const {asyncCall} = changeGroupSettings();
            const {newData} = await asyncCall({title: formData.value.title,
                                               groupSettings: parseInt(props.groupSettings.id)})
            store.commit('updateGroupTitle', {chatId: chatId.value, title: newData.value.title})
        }
        
        const handleImageChange = (event) => {
            formData.value.avatar = event.target.files[0]
            updateImage()
        }

        onMounted(() => {
            if (chatData.value.groupSettings) {
                formData.value.title = chatData.value.groupSettings.title || '';
                formData.value.avatar = chatData.value.groupSettings.avatar || '';
            }
        });

        return { chatData, showUpload, formData, store, updateImage, updateTitle, handleImageChange, isAdmin, avatarWatch };
    }
}
</script>

<template>
    <div class="group-settings">
        <h4>Информация о группе</h4>
        <div class="group-settings-wrapper">
        <div class="image-container">
            <img :src="chatData.groupSettings?.avatar || ''" class="image-content">
            <div v-if="isAdmin()" class="wrapper">
                <label :for="'img'" class="plus-icon">+</label>
                <com-input type="file" class="file-input" :id="'img'"
                @change="handleImageChange" accept="image/png, image/jpg, image/jpeg"></com-input>
            </div>
        </div>
        <div>
            <div class="group-name">{{ chatData?.groupSettings?.title }}</div>
            <label :for="'title'">Название: </label>
            <div v-if="isAdmin()" class="input-group">
                <com-input :id="'title'" v-model="formData.title" class="form-control"></com-input>
                <com-button @click="updateTitle()">Изменить</com-button>
            </div>
        </div>
        </div>
    </div>
</template>

<style scoped>
.group-settings {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.group-settings-wrapper {
    display: flex;
    align-items: center;
}
.image-content {
    width: 100px;
    border-radius: 50%;
}

.group-name {
    font-weight: bolder;
    font-size: 22px
}
.file-input {
    display: none;
}

.image-container:hover .upload-button {
    display: block;
}

.image-container{
    position: relative;
} 

.wrapper {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
}

.image-container:hover .wrapper{
    opacity: 1;
}

.plus-icon {
    color: white;
    font-size: 50px;
    cursor: pointer;

}
</style>