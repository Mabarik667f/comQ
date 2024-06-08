import { createStore } from 'vuex'
import { authModule } from './authModule'
import { userDataModule } from './userDataModule'
import {currentChatModule} from "./currentChatModule"

export default createStore({
  modules: {
    auth: authModule,
    userData: userDataModule,
    currentChat: currentChatModule
  }
})
