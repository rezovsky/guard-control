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
        getStatus(date, student_events) {
            if (date in student_events) {
                const events = student_events[date];
                if (events.length > 0) {
                    const lastEvent = events[events.length - 1];
                    if (lastEvent.action === 'вход') {
                        // Последнее событие - вход, вернуть зеленый класс
                        return 'square green';
                    } else {
                        // Последнее событие - не вход, вернуть красный класс
                        return 'square red';
                    }
                }
            } else {
                // Нет данных на указанную дату, вернуть серый класс
                return 'square gray';
            }
        },
        getLastEvent(date, student_events) {
            if (date in student_events) {
                const events = student_events[date];
                if (events.length > 0) {
                    return events.map(event => `${event.action} в ${event.time}`).join(' ');
                }
            } else {
                return 'Нет данных';
            }
        }
    }
});
