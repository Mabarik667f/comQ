<script>
import { ref } from 'vue';
import register from '@/hooks/register';
import baseValidator from "@/validators/baseValidator";
export default {

    setup() {
        const formData = ref({
                username: '',
                email: '',
                password: '',
                password2: ''
            })

        let errors = ref({
            username: '',
            email: '',
            password: '',
            password2: '',
        })

        
        const registerHook = async () => {
            const {flag} = await baseValidator(formData.value, errors);
            if (!flag.value) {
                const updatedErrors = await register(formData.value, errors.value);

                for (const key in updatedErrors.value) {
                    const errorMessage = updatedErrors.value[key].join(' '); 
                    errors.value[key] = errorMessage;
                }

                if (updatedErrors) {
                    formData.value['password'] = '';
                    formData.value['password2'] = '';
                }

            }
        }
        return {registerHook, formData, errors}
    }
}
</script>

<template>
    <div class="register-page">
    <com-form @submit.prevent="registerHook" class="register">
        <template v-slot:header>
            <div class="mb-3">
            <h2>Регистрация</h2>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
                <label for="usernameInput" class="form-label">Login</label>
                    <com-input
                    required
                    v-model="formData.username"
                    id="usernameInput"
                    class="form-control">
                    </com-input>
                <span v-if="errors.username" class="form-errors">{{ errors.username }}</span>

            </div>
            <div class="mb-3">
            <label for="emailInput" class="form-label">Email</label>
                <com-input
                required
                v-model="formData.email"
                :type="'email'"
                id="emailInput"
                class="form-control"
                placeholder="name@example.com">
                </com-input>
                <span v-if="errors.email" class="form-errors">{{ errors.email }}</span>

            </div>
            <div class="mb-3">
            <label for="passwordInput" class="form-label">Пароль</label>
                
                <com-input
                required
                v-model="formData.password"
                :type="'password'"
                id="passwordInput"
                class="form-control">
                </com-input>
                <span v-if="errors.password" class="form-errors">{{ errors.password }}</span>
                <div class="form-text">
                    Ваш пароль должен состоять из 8-20 символов
                </div>
            </div>
            <div class="mb-3">
            <label for="password2Input" class="form-label">Повтор пароля</label>
                <com-input
                required
                v-model="formData.password2"
                :type="'password'"
                id="password2Input"
                class="form-control">
                </com-input>
                <span v-if="errors.password2" class="form-errors">{{ errors.password2 }}</span>
            </div>
        </template>
        <template v-slot:button>
            <div class="buttons">
                <com-button >Регистрация</com-button>
                <com-button @click="$router.push('/login')" class="login-button" :type="'button'">Войти</com-button>
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

.login-button {
    margin-left: 20px;
    width: 100px;
}

.register {
    background-color: rgba(30, 30, 45);
    color: whitesmoke;
    width: 50%;
    margin: auto;
}

.register-page {
    background-color: rgba(30, 30, 45);
    display: flex;
    align-items: center;
}

.form-control:focus {
    border-color: #a3a1a1;
    box-shadow: none;
}

.form-text {
    color: whitesmoke;
}

@media screen and (max-width: 768px) {
    .register {
        width: 90%;
        padding: 10px;
    }
}
</style>