import { createStore } from 'vuex'
import { authModule } from './authModule'
import { userDataModule } from './userDataModule'
import {currentChatModule} from "./currentChatModule"
import { chatsModule } from './chatsModule'

export default createStore({
  modules: {
    auth: authModule,
    userData: userDataModule,
    currentChat: currentChatModule,
    chats: chatsModule
  }
})
