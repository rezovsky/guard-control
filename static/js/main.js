new Vue({
    el: '#app',
    data: {
        items: [],
    },
    mounted() {
        this.loadData();
    },
    methods: {
        loadData() {
            axios.get('/get_data')
                .then(response => {
                    this.items = response.data;
                })
                .catch(error => {
                    console.error('Ошибка при загрузке данных:', error);
                });
        },

    }
});
