<template>
  <v-data-table
    :headers="headers"
    :items="desserts"
    :search="search"
    :sort-by="[{ key: 'timestamp', order: 'asc' }]">
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>รายชื่อสมาชิก</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-btn class="mb-2" color="primary" dark @click="checkIn">
          CheckIn
        </v-btn>
      </v-toolbar>

      <v-text-field
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        hide-details
        single-line>
      </v-text-field>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    search: '',
    headers: [
      { title: 'ID', align: 'start', sortable: false, key: 'id' },
      { title: 'Staff ID', key: 'staffId' },
      { title: 'Name', key: 'name' },
      { title: 'Timestamp', key: 'timestamp' },
    ],
    desserts: [],
  }),

  async created() {
    this.initialize();
    const response = await axios.get("http://localhost:7000/liststds");
    const data = response.data;
    this.desserts = data.students;
    console.log(data);
  },

  methods: {
    initialize() { },

    async checkIn() {
      try {
            const response = await axios.post('http://localhost:7000/Checkin');
            console.log(response.data);
            this.close();
          } catch (error) {
            console.error('Error during POST request:', error);
      }
    }
  }
}
</script>