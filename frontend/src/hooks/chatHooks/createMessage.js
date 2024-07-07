import store from "@/store";
import { useToast } from "vue-toastification";


export default function createMessage (chatTitle, message, chatId) {
    const toast = useToast()
    store.dispatch('addMessage', {message: message, chatId: chatId})
    store.commit('updateLastMessage', {chatId: chatId, message: message})
    if (message.user.username != store.getters.getUserName) {
        toast(`Новое сообщение в чате: ${chatTitle}`);
        store.commit('updateNotifications', { chatId: chatId, status: "add" });
    }
}