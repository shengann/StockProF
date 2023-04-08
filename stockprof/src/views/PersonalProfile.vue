<template>
    <div class="page-my-account">
        <div class="column is-12">
            <h1 class="title">My account</h1>
        </div>

        <div class="box">
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th class="text-center" scope="col"></th>
                        <th class="text-center" scope="col">Category</th>
                        <th class="text-center" scope="col">Date Created</th>
                        <th class="text-center" scope="col">remarks</th>
                        <th class="text-center" scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(data,index) in history" :key="data.id">
                        <td><button class="delete button is-danger" aria-label="close"  @click="showModal = true; this.deleteId=data.id"></button></td>
                        <td scope="row">{{ data.category}}</td>
                        <td scope="row">{{ formatDate(data.date_created)}}</td>
                        <td>{{data.remarks}}</td>
                        <td><button @click="navigateToDetails(data.id,index)" type="button" class="btn btn-primary">View Details</button></td>
                    </tr>
                </tbody>
            </table>
            <div class="modal"  :class="{ 'is-active': showModal }">
                    <div class="modal-background" @click="showModal = false"></div>
                    <div class="modal-card">
                        <header class="modal-card-head">
                            <p class="modal-card-title">Are You  Sure?</p>
                            <button class="delete" aria-label="close" @click="showModal = false"></button>
                        </header>
                        <section class="modal-card-body">
                            <label>Do you want to delete the selected portfolio.This procees cannot be undone</label>
                        </section>
                        <footer class="modal-card-foot">
                            <button class="button is-danger" @click="deleteHistory(this.deleteId); showModal = false">Save Results</button>
                            <button class="button" @click="showModal = false">Cancel</button>
                        </footer>
                    </div>
                </div>
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
            history:[],
            showModal: false,
            deleteId: '',
        }
    },
    mounted() {
        document.title = 'My account | StockProF'

        this.getHistory()
    },
    methods: {
        async getHistory() {
            await axios
                .get('api/history')
                .then(response => {
                    this.history = response.data
                })
        },
        async deleteHistory(id) {
            await axios
                .delete(`api/history/${this.deleteId}`)
                .then(response => {
                    this.getHistory()
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