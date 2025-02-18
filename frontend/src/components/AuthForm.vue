<script setup>
import { ref } from 'vue';
import BubbleButton from './BubbleButton.vue';
import store from '@/store';
import { generate_reset_code } from '@/api';

var isLogin = ref(true);
var snackbar = ref(false);
var timeout = 2000;
var text = ref("");
var reset_email = ref("");


const data = ref({
        first_name: "",
        last_name: "",
        email: "",
        phone_number: "",
        password: "",
        specialization: "",
        isDoctor: false
    }),
    emit = defineEmits(['submit']);

    function resetFields(){
        data.value = {
            first_name: "",
            last_name: "",
            email: "",
            phone_number: "",
            password: "",
            specialization: "",
            isDoctor: false
        }
    }

    function submit() {
        //if (data.city.length === 0 && data.specialization === 0) return;
        emit('submit', data.value);
    }

    function runChecks(){
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        const phonePattern = /^\d+$/;
        if(data.value.password.length < 3 || data.value.password.length > 22) {
            text.value = 'Password must have more than 3 and less than 22 characters'
            return false;
        }
        else if(!emailPattern.test(data.value.email)) {
            text.value = 'Provide a valid email address'
            return false;
        }
        else if(data.value.last_name.length < 3 || data.value.last_name.length > 26) {
            text.value = 'Last name must have more than 3 and less than 22 characters'
            return false;
        }
        else if(data.value.first_name.length < 3 || data.value.first_name.length > 26) {
            text.value = 'First name must have more than 3 and less than 22 characters'
            return false;
        }
        else if(data.value.phone_number.length != 10) {
            text.value = 'Phone number must have 10 characters'
            return false;
        }
        else if(!phonePattern.test(data.value.phone_number)) {
            text.value = 'Phone number must contain only digits'
            return false;
        }
        return true;
    }

    function register() {
        if (runChecks()){
            store.dispatch('register', {email: data.value.email, password: data.value.password, nume: data.value.last_name, prenume: data.value.first_name, phone_number: data.value.phone_number, isDoctor: data.value.isDoctor}).then((response) => {
            })
            resetFields()
            text.value = 'Please check your email to confirm your account!'
            snackbar.value = true;
        }
    }

    async function login() {
        console.log(data.value.email + ' ' + data.value.password)
        await store.dispatch('login', {email: data.value.email, password: data.value.password}).then((response) => {
            text.value = response
        })
        snackbar.value = true;
        resetFields()
    }

    async function submitReset(){
        if(reset_email.value.length == 0){
            text.value = 'Please fill in empty field'
            snackbar.value = true;
            return;
        }

        text.value = 'You will receive an email with the reset link!'
        snackbar.value = true;
        await generate_reset_code({'email': reset_email.value});
        reset_email.value = '';
    }
</script>

<template>
    <div>
        <div class="inputs" v-if="isLogin">
            <input type="text" v-model="data.email" placeholder="email" />
            <input type="password" v-model="data.password" placeholder="password" />
            <a @click="isLogin = !isLogin">New user? Register</a>
            <v-dialog max-width="500">
                <template v-slot:activator="{ props: activatorProps }">
                <a v-bind="activatorProps">Forgot password? Reset</a>
                </template>

                <template v-slot:default="{ isActive }">
                <v-card prepend-icon="mdi-grease-pencil" title="Submit reset password request" color="rgba(6, 125, 100, 1)">
                    <div class="test">
                    <v-spacer></v-spacer>
                    <v-text-field label="Email" v-model="reset_email"></v-text-field>
                    </div>
                    <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        text="Close"
                        @click="isActive.value = false"
                    ></v-btn>
                    <v-btn
                        text="Submit"
                        @click="submitReset(); isActive.value = false;"
                    ></v-btn>
                    </v-card-actions>
                </v-card>
                </template>
            </v-dialog>
            <BubbleButton label="Login" @click="login" />
        </div>
        <div class="inputs" v-else>
            <input type="text" v-model="data.first_name" placeholder="first name" />
            <input type="text" v-model="data.last_name" placeholder="last name" />
            <input type="text" v-model="data.email" placeholder="email" />
            <input type="text" v-model="data.phone_number" placeholder="phone number" />
            <input type="password" v-model="data.password" placeholder="password" />
            <v-checkbox label="Register as a doctor" color="green" v-model="data.isDoctor"></v-checkbox>
            <a @click="isLogin = !isLogin">Already a user? Login</a>
            <v-dialog max-width="500">
                <template v-slot:activator="{ props: activatorProps }">
                <a v-bind="activatorProps">Forgot password? Reset</a>
                </template>

                <template v-slot:default="{ isActive }">
                <v-card prepend-icon="mdi-grease-pencil" title="Submit reset password request" color="rgba(6, 125, 100, 1)">
                    <div class="test">
                    <v-spacer></v-spacer>
                    <v-text-field label="Email" v-model="reset_email"></v-text-field>
                    </div>
                    <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        text="Close"
                        @click="isActive.value = false"
                    ></v-btn>
                    <v-btn
                        text="Submit"
                        @click="submitReset(); isActive.value = false;"
                    ></v-btn>
                    </v-card-actions>
                </v-card>
                </template>
            </v-dialog>
            <BubbleButton label="Register" @click="register" />
        </div>
        <v-layout>
            <v-snackbar v-model="snackbar" :timeout="timeout">
                {{ text }}
                <template v-slot:action="{ attrs }">
                <v-btn text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
                </template>
            </v-snackbar>
        </v-layout>
    </div>
</template>

<style scoped>
.inputs:not(.teste) {
    width: auto;
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.teste{
    color: rgb(187, 187, 187);
    width: auto;
    height: auto;
}

.inputs input {
    padding: 1em;
    border: 1px solid white;
    border-radius: 4px;
    background-color: transparent;
    color: white;
}

.inputs a {
    color: white;
    text-decoration: none;
    cursor: pointer;
}

</style>