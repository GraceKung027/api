<template>
    <h2>รายชื่่อสมาชิก</h2>
    <div>
    <ul>
        <li v-for="st in students" :key="st.id">
            <span>{{ st.id }}</span>
            <span>{{ st.username }}</span>
            <span>{{ st.password }}</span>
        </li>
    </ul>
    </div>
</template>
<script>
    export default{
        data: () => ({
            title : 'สมาชิก',
            students:[
                {id: 123,username: 'kruoak',password: 1},
                {id: 124,username: 'kruoak1',password: 2},
                {id: 125,username: 'kruoak2',password: 3},
            ],
            test: '',
        }),
        async created() {
            const response = await fetch("http://localhost:7000/liststds")
            const data = await response.json()
            this.students = data.students
            comsole.log(data.students)
        }
    }
</script>