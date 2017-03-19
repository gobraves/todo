(function(Vue) {

   var vue = new Vue({
        el: '#app',

        created: function() {
            this.$http.get('/users/'++'/tasks').then(function(res) {
                this.tasks = res.data.tasks ? res.data.tasks : [];
            });
        },

        methods: {
            createTask: function() {
                if (!$.trim(this.newTask.title)) {
                    this.newTask = {
                        title: '',
                        description: ''
                    };
                    return;
                };

                this.newTask.done = false;

                this.$http.post('/tasks/', this.newTask).then(function(res) {
                    this.newTask.id = res.data.tasks.length;
                    this.tasks.push(this.newTask);

                    this.newTask = {
                        title: '',
                        description: ''
                    };
                }, function(err) {
                    console.log(err);
                });
            },

            deleteTask: function(index) {
                this.$http.delete('/tasks/' + index).then(function(res) {
                    this.$http.get('/tasks').then(function(res) {
                        this.tasks = res.data.tasks ? res.data.tasks : [];
                    });
                },function(err) {
                    console.log(err);
                });
            },

            updateTask: function(task, completed) {
                if (completed) {
                    task.done = true;
                }

                this.$http.put('/tasks/' + task.id, task).then(function(res) {
                    this.$http.get('/tasks').then(function(res) {
                        this.tasks = res.data.tasks ? res.data.tasks : [];
                    });
                }, function(err) {
                    console.log(err);
                });
            }
        }
    });
})(Vue);
