<template>
  <div class="btnNavBar">
    <button class="navBtn" @click='prevFile'>prev</button>
    <button class="navBtn" @click='nextFile'>next</button>
  </div>
  <img class="display" :src="imgURL" alt="">
</template>

<script>
export default {
  name: 'PicsView',
  setup() { }
}
</script>