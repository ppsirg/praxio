<template>
<div class="btn-container">
  <button @click="go_to('cloud')">cloud</button>
  <button @click="go_to('pics')">imagenes</button>
  <button @click="go_to('vids')">videos</button>
</div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: 'DashboardView',
  setup () {
    const router = useRouter()
    function go_to(target) {
      router.push({name: target})
    }
    return {go_to}
  }
}
</script>

<style scoped>
.btn-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  width: 90%;
  margin: auto;
}
</style>