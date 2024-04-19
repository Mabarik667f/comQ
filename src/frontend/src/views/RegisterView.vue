<script>
import { ref } from 'vue';
import register from '@/hooks/register';
import registerValidator from "@/validators/registerValidator";
export default {

    setup() {
        const formData = ref({
                login: '',
                email: '',
                password: '',
                password2: ''
            })

        let errors = ref({
            login: '',
            email: '',
            password: '',
            password2: '',
        })
        
        
        const registerHook = () => {
            const {flag} = registerValidator(formData.value, errors);
            if (!flag.value) {
                register(formData.value);
            }
        }
        return {registerHook, formData, errors}
    }
}
</script>

<template>
    <com-form @submit.prevent="registerHook">
        <template v-slot:header>
            <div class="mb-3">
            <h2>Регистрация</h2>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
                <label for="loginInput" class="form-label">Login</label>
                    <com-input
                    v-model="formData.login"
                    id="loginInput"
                    class="form-control">
                    </com-input>
                <span v-if="errors.login">{{ errors.login }}</span>

            </div>
            <div class="mb-3">
            <label for="emailInput" class="form-label">Email</label>
                <com-input
                v-model="formData.email"
                :type="'email'"
                id="emailInput"
                class="form-control"
                placeholder="name@example.com">
                </com-input>
                <span v-if="errors.email">{{ errors.email }}</span>

            </div>
            <div class="mb-3">
            <label for="passwordInput" class="form-label">Пароль</label>
                
                <com-input
                v-model="formData.password"
                :type="'password'"
                id="passwordInput"
                class="form-control">
                </com-input>
                <span v-if="errors.password">{{ errors.password }}</span>
                <div class="form-text">
                    Ваш пароль должен состоять из 8-20 символов
                </div>
            </div>
            <div class="mb-3">
            <label for="password2Input" class="form-label">Повтор пароля</label>
                <com-input
                v-model="formData.password2"
                :type="'password'"
                id="password2Input"
                class="form-control">
                </com-input>
                <span v-if="errors.password2">{{ errors.password2 }}</span>
            </div>
        </template>
        <template v-slot:button>
            <com-button>Регистрация</com-button>
        </template>
    </com-form>
    
</template>
<style scoped>

</style>