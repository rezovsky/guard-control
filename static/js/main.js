new Vue({
    el: '#app',
    data: {
        data: {}, // Ваши данные JSON здесь
        groupVisible: {}, // Для отслеживания видимости групп
        personVisible: {} // Для отслеживания видимости персон
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
            // Переключение видимости группы
            this.$set(this.groupVisible, groupName, !this.groupVisible[groupName]);
        },
        togglePerson(personName) {
            // Переключение видимости персоны
            this.$set(this.personVisible, personName, !this.personVisible[personName]);
        }
    }
});
