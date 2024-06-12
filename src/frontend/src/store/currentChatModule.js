import Cookies from "js-cookie";

export const currentChatModule = {
    state: () => ({
        title: '',
        imagePath: '',
    }),
    getters: {
        title: state => state.title,
        imagePath: state => state.imagePath
    },

    mutations: {
        setChatData(state, {title, imagePath}) {
            state.imagePath = imagePath;
            state.title = title;
        }
    },
    actions: {
        setChatDataCookies({dispatch}, {title, imagePath}) {
            Cookies.set('title', title, { sameSite: 'None', secure: true });
            Cookies.set('imagePath', imagePath.value, { sameSite: 'None', secure: true })
            dispatch('getChatDataCookies');
        },

        getChatDataCookies({commit}) {
            commit('setChatData', {title: Cookies.get('title'),
             imagePath: Cookies.get('imagePath')})
        },
        clear() {
            Cookies.remove('title');
            Cookies.remove('imagePath');
        },
    }
}