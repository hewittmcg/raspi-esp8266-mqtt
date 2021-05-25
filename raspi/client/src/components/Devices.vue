<template>
  <div>
      <table class='table table-hover'>
          <thead>
              <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Name</th>
                  <th scope="col">Date Registered</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="device in devices" :key="device[0]">
                <td><router-link :to="{
                    name: 'Data', params: { id: device[0] } }">{{device[0]}}</router-link></td>
                <td>{{device[1]}}</td>
                <td>{{device[2]}}</td>
            </tr>
          </tbody>
      </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Devices',
  data() {
    return {
      devices: [],
    };
  },
  methods: {
    getMessage() {
      // Flask API serves to port 5000
      const path = `http://${window.location.hostname}:5000/devices`;
      axios.get(path)
        .then((res) => {
          this.devices = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
                console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
