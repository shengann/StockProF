<template>
    <div class="page-my-account">
        <div class="column is-12">
            <h1 class="title">My account</h1>
        </div>

        <div class="column is-12">
            <button @click="logout()" class="button is-danger">Log out</button>
        </div>

        <div class="box">
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th class="text-center" scope="col">Category</th>
                        <th class="text-center" scope="col">Date Created</th>
                        <th class="text-center" scope="col">remarks</th>
                        <th class="text-center" scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(data,index) in history" :key="data.id">
                        <td scope="row">{{ data.category}}</td>
                        <td scope="row">{{ formatDate(data.date_created)}}</td>
                        <td>idk</td>
                        <td><button @click="navigateToDetails(data.id,index)" type="button" class="btn btn-primary">View Details</button></td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment';

export default {
    name: 'PersonalProfile',
    data() {
        return {
            history:[]
        }
    },
    mounted() {
        document.title = 'My account | StockProF'

        this.getHistory()
    },
    methods: {
        logout() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("userid")
            this.$store.commit('removeToken')
            this.$router.push('/')
        },
        async getHistory() {
            await axios
                .get('api/history')
                .then(response => {
                    this.history = response.data
                })
        },
        formatDate(value) {
            return moment(value, 'YYYY-MM-DDTHH:mm:ss.SSSZZ').local().format('MMM D, YYYY h:mm A');
        },
        navigateToDetails(id,index){
            this.$router.push({
                name: 'PortfolioDetails', 
                params: { id: id },
            });
        }
    }
}
</script>