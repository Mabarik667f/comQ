import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import components from './components/UI/index'
import 'bootstrap/dist/css/bootstrap.css'; 
import "vue-toastification/dist/index.css"
import Toast from 'vue-toastification'


const app = createApp(App);

components.forEach(component => {
    app.component(component.name, component);
})

app
    .use(Toast, {maxToasts: 3})
    .use(store)
    .use(router)
    .mount('#app')
