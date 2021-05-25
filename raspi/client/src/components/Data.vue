<template>
  <div>
      <table class='table table-hover'>
          <thead>
              <tr>
                  <th scope="col">Time</th>
                  <th scope="col">Data</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="packet in packets" :key="packet[0]">
                <td>{{packet[0]}}</td>
                <td>{{packet[1]}}</td>
            </tr>
          </tbody>
      </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Data',
  data() {
    return {
      packets: [],
    };
  },
  methods: {
    getMessage() {
      // Flask API serves to port 5000
      const path = `http://${window.location.hostname}:5000/device/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.packets = res.data;
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
