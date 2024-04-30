import Cookies from "js-cookie"
const authHeaders = {
    'Authorization': "Bearer " + Cookies.get('access')
}

export {authHeaders};