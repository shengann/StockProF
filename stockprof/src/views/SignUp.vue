<template>
    <div class="page-sign-up">
        <section class="h-100 gradient-form" style="background-color:#fcf5e7;">
            <div class="container py-5 h-100">
                <div class="row d-flex justify-content-center align-items-center h-100">
                    <div class="col-xl-10">
                        <div class="card rounded-3 text-black">
                            <div class="row g-0">
                                <div class="col-lg-6">
                                    <div class="card-body p-md-5 mx-md-4">

                                        <div class="text-center">
                                            <img img src="../assets/StockProF.png" alt="StockProF" style="width: 185px;">
                                        </div>

                                        <form @submit.prevent="submitForm">
                                            <p class="title">Sign up</p>


                                            <div class="field">
                                                <label>Username</label>
                                                <div class="control">
                                                    <input type="text" class="input" v-model="username">
                                                </div>
                                            </div>

                                            <div class="field">
                                                <label>Email</label>
                                                <div class="control">
                                                    <input type="email" class="input" v-model="email">
                                                </div>
                                            </div>

                                            <div class="field">
                                                <label>Password</label>
                                                <div class="control">
                                                    <input type="password" class="input" v-model="password">
                                                </div>
                                            </div>

                                            <div class="field">
                                                <label>Confirmed password</label>
                                                <div class="control">
                                                    <input type="password" class="input" v-model="password2">
                                                </div>
                                            </div>

                                            <div class="notification is-danger" v-if="errors.length">
                                                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                                            </div>

                                            <div class="field mb-10">
                                                <div class="control mb-4">
                                                    <button class="button is-black mt-12">Sign up</button>
                                                </div>
                                            </div>

                                            <hr>

                                            Or <router-link to="/login">click here</router-link> to log in!
                                        </form>

                                    </div>
                                </div>
                                <div class="col-lg-6 d-flex align-items-center gradient-custom-2">
                                    <div class="text-white px-3 py-4 p-md-5 mx-md-4">
                                        <h4 class="mb-4">StockProF (Stock Profilling Framework)</h4>
                                        <p class="small mb-0">                                            
                                            StockProF is a stock profiling framework that enables you to quickly build a portfolio from selected sectors in Bursa Malaysia, saving you time in selecting individual stocks. With StockProF, you can profile the stocks and portdolio generated based on the portfolio profile of each portfolio.</p>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name: 'SignUp',
    data() {
        return {
            username: '',
            password: '',
            password2: '',
            email: '',
            errors: []
        }
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.username === '') {
                this.errors.push('Pleaase enter your username')
            }

            if (this.password === '') {
                this.errors.push('The password is too short')
            }

            if (this.password !== this.password2) {
                this.errors.push('The passwords doesn\'t match')
            }

            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password,
                    email: this.email
                }

                axios
                    .post("/api/users/", formData)
                    .then(response => {
                        toast({
                            message: 'Account created, please log in!',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/login')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    }
}
</script>

<style scoped>
.gradient-custom-2 {
    /* fallback for old browsers */
    background: #fccb90;

    /* Chrome 10-25, Safari 5.1-6 */
    background: -webkit-linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);

    /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}

@media (min-width: 768px) {
    .gradient-form {
        height: 120vh !important;
    }
}

@media (min-width: 769px) {
    .gradient-custom-2 {
        border-top-right-radius: .3rem;
        border-bottom-right-radius: .3rem;
    }
}
</style>