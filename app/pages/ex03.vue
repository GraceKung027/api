<template>
    <div>
      <h1> {{ name }}</h1>
      <input type="text" v-model="username"><br>
      <input type="text" v-model="password"><br>
      <button @click="doSave">SAVE</button>
      <button @click="listData">แสดงข้อมูล</button>
    </div>
  </template>
<script>
import axios from 'axios';
export default {
  data() {
    return { 
        name: "กรุณากรอกข้อมูล",
        username: '',
        password: '',
        students: ''
     }
    },
  methods: {
    doSave() {
      console.log(this.username);
      console.log(this.password);
    },
    async listData() {
        let res =  await axios.get('http://localhost:7000/liststds')
        this.students = res.data
        console.log(this.students)
    }
  },
}
</script>