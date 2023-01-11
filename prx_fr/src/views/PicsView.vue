<template>
  <div class="btnNavBar">
    <button class="navBtn" @click='prevFile'>prev</button>
    <button class="navBtn" @click='nextFile'>next</button>
  </div>
  <div class="btnNavBar">
    <input type="text" v-model="folder_dir">
    <button @click="search_data">go</button>
  </div>
  <img class="img-display" :src="actual_img" alt="">
</template>

<script setup>
import { ref } from 'vue';

let folder_dir = ref('')
let resource_list = ref([])
const back = 'http://localhost:8000'
let actual_img = ref('')
let actual_indx = ref(0)

function prevFile() {
  actual_indx.value = actual_indx.value - 1
  if (actual_indx.value < 0) {
    actual_indx.value = resource_list.value.length -1
  }
  actual_img.value = resource_list.value[actual_indx.value]
}

function nextFile() {
  actual_indx.value = actual_indx.value + 1
  if (actual_indx.value == resource_list.value.length) {
    actual_indx.value = 0
  }
  actual_img.value = resource_list.value[actual_indx.value]
}

function search_data() {
  fetch(`${back}/gallery/${folder_dir.value}/`)
  .then(rsp => rsp.json())
  .then(rs => {
    resource_list.value = rs.map(itm => `${back}/${itm}`)
    actual_indx.value = 0
    actual_img.value = resource_list.value[0] ? resource_list.value[0]:''
    return resource_list.value
  })
}

</script>

<style>
.img-display {
  width: 95%;
}
</style>