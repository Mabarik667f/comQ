<script>
import baseValidator from '@/validators/baseValidator';
import { ref } from 'vue';
import { useStore } from 'vuex';
export default {
    setup() {
        const formData = ref({
            login: '',
            password: ''
        });

        const errors = ref({
            login: '',
            password: ''
        });

        const store = useStore();

        const handleLogin = async () => {
            
            const {flag} = await baseValidator(formData.value, errors);
            if (flag) {
                try {
                    await store.dispatch('login', {formData: formData.value});
                } catch (error) {
                    formData.value['password'] = '';
                    errors.value['password'] = 'Неправильный логин или пароль';
                }
            }
        }

        return {formData, errors, handleLogin}
    }
    

}
</script>

<template>
    <div class="login-page">
    <com-form @submit.prevent="handleLogin()" class="login">
        <template v-slot:header>
            <div class="mb-3">
            <h2>Войти</h2>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
            <label for="emailInput" class="form-label">Логин или Email</label>
                <com-input
                required
                v-model="formData.login"
                id="emailInput"
                class="form-control"
                placeholder="name@example.com">
                </com-input>
                <span v-if="errors.login" class="form-errors">{{ errors.login }}</span>
            </div>
            <div class="mb-3">
            <label for="passwordInput" class="form-label" >Пароль</label>
                
                <com-input
                required
                v-model="formData.password"
                :type="'password'"
                id="passwordInput"
                class="form-control">
                </com-input>
                <span v-if="errors.password" class="form-errors">{{ errors.password }}</span>
            </div>
        </template>
        <template v-slot:button>
            <div class="buttons">
                <com-button @click="$router.push('/register')" :type="'button'">Регистрация</com-button>
                <com-button class="login-btn">Войти</com-button>
            </div>
        </template>
    </com-form>
    </div>
</template>


<style scoped>

.buttons {
    display: flex;
    flex-direction: row;
}
.buttons {
    margin-top: 10px;
}
.login-btn {
    width: 120px;
    margin-left: 10px;
}

.login {
    background-color: rgba(30, 30, 45);
    color: whitesmoke;
    width: 50%;
    margin: auto;
}

.login-page {
    background-color: rgba(30, 30, 45);
    display: flex;
    align-items: center;
    
}

.form-control:focus {
    border-color: #a3a1a1;
    box-shadow: none;
}

@media screen and (max-width: 768px) {
    .login {
        width: 90%;
        padding: 10px;
    }
}
</style>