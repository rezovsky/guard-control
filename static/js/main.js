new Vue({
    el: '#app',
    data: {
        data: {},
        groupVisible: {},
        personVisible: {},
        personDateVisible: {},
    },
    mounted() {
        this.loadData();
    },
    methods: {
        loadData() {
            axios.get('/get_data')
                .then(response => {
                    this.data = response.data;
                    // Инициализация видимости групп
                    for (const groupName in this.data) {
                        this.$set(this.groupVisible, groupName, false);
                    }
                    // Инициализация видимости персон
                    for (const groupName in this.data) {
                        for (const personName in this.data[groupName]) {
                            this.$set(this.personVisible, personName, false);
                        }
                    }
                })
                .catch(error => {
                    console.error('Ошибка при загрузке данных:', error);
                });
        },
        toggleGroup(groupName) {
            this.$set(this.groupVisible, groupName, !this.groupVisible[groupName]);
        },
        togglePerson(personName) {
            this.$set(this.personVisible, personName, !this.personVisible[personName]);
        },
        togglePersonDate(personName, date) {
            const personDate = personName + date
            this.$set(this.personDateVisible, personDate, !this.personDateVisible[personDate]);
        }
    }
});
