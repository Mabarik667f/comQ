<script>
import { mapActions } from 'vuex';
export default {

    data() {
        return {
            formData: {
                email: '',
                password: ''
            }
        }
    },

    methods: {
        ...mapActions({
            login: 'login'
        })
    }

}
</script>

<template>
    <com-form @submit.prevent="login">
        <template v-slot:header>
            <div class="mb-3">
            <h2>Войти</h2>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
            <label for="emailInput" class="form-label">Email</label>
                <com-input
                v-model="formData.login"
                id="emailInput"
                class="form-control"
                placeholder="name@example.com">
                </com-input>
            </div>
            <div class="mb-3">
            <label for="passwordInput" class="form-label">Пароль</label>
                
                <com-input
                v-model="formData.password"
                :type="'password'"
                id="passwordInput"
                class="form-control">
                </com-input>
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