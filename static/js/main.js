new Vue({
    el: '#app',
    data: {
        items: [],
    },
    mounted() {
        const currentUrl = window.location.href;
        const urlParts = currentUrl.split('/');
        const groupIndex = urlParts.indexOf('group');
        if (groupIndex > 0) {
            group =  `/${urlParts[groupIndex + 1]}`
        } else {
            group = ''
        }
        console.log(group)
        this.loadData(group);
    },
    methods: {
        loadData(group) {
            axios.get(`/get_data${group}`)
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
