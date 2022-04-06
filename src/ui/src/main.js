import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from 'axios';
import VueAxios from 'vue-axios';

// fontawesome icons
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCirclePlus, faCircleMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faCirclePlus);
library.add(faCircleMinus);

// Vue App
const app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon);  // register font-awesome
app.use(router); // vue router
app.use(VueAxios, axios);
app.mount("#app");
