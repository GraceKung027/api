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
import axios from 'axios';

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
            const response = await axios.get("http://localhost:7000/liststds")
            const data = response.data
            this.students = data.students
            comsole.log(data)
        }
    }
</script>