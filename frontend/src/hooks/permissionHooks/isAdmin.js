import store from "@/store";
export default function isOwner() {
    return store.getters.getUserRole === 'O' || store.getters.getUserRole === 'A'
}