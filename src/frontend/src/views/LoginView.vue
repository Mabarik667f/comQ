<script>
import baseValidator from '@/validators/baseValidator';
import { ref } from 'vue';
import { useStore } from 'vuex';
import router from '@/router';
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
                    router.push('/');
                    window.location.reload();
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
    <com-form @submit.prevent="handleLogin()">
        <template v-slot:header>
            <div class="mb-3">
            <h2>Войти</h2>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
            <label for="emailInput" class="form-label">Email</label>
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
            <com-button class="login__btn">Войти</com-button>
        </template>
    </com-form>
</template>


<style scoped>
.login__btn {
    width: 120px;
}

</style>