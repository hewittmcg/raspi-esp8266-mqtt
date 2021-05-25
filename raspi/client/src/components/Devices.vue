<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';
// eslint-disable-next-line
console.log("in script");
export default {
  name: 'Devices',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      // Flask API serves to port 5000
      const path = `http://${window.location.hostname}:5000/devices`;
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
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
