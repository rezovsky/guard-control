new Vue({
    el: '#app',
    data: {
        items: [],
        group: '',
    },
    mounted() {
        const currentUrl = window.location.href;
        const urlParts = currentUrl.split('/');
        const groupIndex = urlParts.indexOf('group');
        if (groupIndex > 0) {
            this.group =  `/${urlParts[groupIndex + 1]}`
        } else {
            this.group = ''
        }
        this.loadData()
        setInterval(this.loadData, 60000);
    },
    methods: {
        loadData() {
            axios.get(`/get_data${this.group}`)
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
