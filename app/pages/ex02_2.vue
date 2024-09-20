<template>
    <h1>{{ name }} {{ age }}</h1>
    <h1>{{ upperCase }}</h1>
    <input type="text" :value="name">
    <input type="text" v-model="name">
</template>
<script>
    export default{
        data: () => ({
            name:'Chaiyaphum',
            age: 51
        }),
        computed: {
            upperCase(){
            return this.name.toUpperCase()
            }
        }
    }
</script>
