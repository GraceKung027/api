<template>
    <div>
      <h1>Hello {{ name }}</h1>
      <div>{{ age }}</div>
      <input type="text" :value="name"><br>
      <input type="text" v-model="name"><br>
      <ui>
        <li v-for="st in students">
            <span>{{ st.name }}</span>
            <span>{{ st.age }}</span>
        </li>
      </ui>
    </div>
  </template>
  <script>
  export default {
    data() {
      return  {
      name: "World ctc",
      age:30,
      students : [
       { id: 1 ,'name':'kitsada','age':50},
       { id: 2 ,'name':'toa1121','age':20},
       { id: 3 ,'name':'tao658','age':30}
      ]
      }
    }
  
  }
  </script>