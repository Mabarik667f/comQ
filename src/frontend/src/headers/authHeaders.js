import Cookies from "js-cookie"
const access = Cookies.get('access');
const authHeaders = {
    'Authorization': `Bearer ${access}`
}

export {authHeaders};