import Vue from 'vue';
import VueRouter from 'vue-router';

import Navigation from "./Nav.vue";
import Footer from "./Footer.vue";
import Home from "./Home.vue";
import Kanji from "./Kanji.vue";
import Vocabulary from "./Vocabulary.vue";


const routes = [
    { path : "/", component: Home },
    { path : "/kanji", component: Kanji},
    { path : "/vocabulary", component: Vocabulary}
];

const router = new VueRouter({
    routes,
    linkActiveClass: 'is-active'
});

window.Vue = Vue;
Vue.use(VueRouter);

new Vue({
    el: "#wkkp",

    components : {
        'navigation' : Navigation,
        'foot' : Footer
    },

    router
});