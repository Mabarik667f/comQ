import router from '@/router';
import axios from 'axios';

export default function register(formData) {
    axios.post('/v1/users/register/', {
        email: formData.email,
        username: formData.login,
        password: formData.password,
        password2: formData.password2
    },
    {
        headers: {
            'Content-Type': 'application/json',
            "Accept": 'application/json'
        }
    })
    .then(response => {
        console.log(response);
        if (response.status === 201 && response.statusText === 'Created'){
            router.push('/login');
        }
    })
    .catch(error => {
        console.log(error);
    })

    
}