<template>
  <div class="control-container">
    <label for="savingfiles">Files to save</label>
    <input type="file" multiple name="savingfiles" id="savingfiles" v-on:change='listFiles'>
    <button v-on:click="uploadFiles">upload</button>
    <div>{{ to_upload_files }}</div>
  </div>
  <div class="load-container">
    <div class="load-progress" v-for='bt in batch' :key='bt.k'>{{ bt.k }}</div>
  </div>
</template>

<script>
import { ref } from 'vue'

const BACK_URL = 'http://localhost:9000'


export default {
  name: 'CloudView',
  setup() {
    let to_upload_files = ref('')
    let batch = ref([])

    async function uploadFiles() {
      to_upload_files.value = 'uploading in progress'
      let fileObj = document.getElementById('savingfiles')
      let rr = []
      let count = 0
      for (let index = 0; index < fileObj.files.length; index++) {
        let itm = fileObj.files[index]
        let ff = new FormData()
        ff.append('files', itm, itm.name)
        const bdy = { method: 'POST', body: ff }
        rr.push(fetch(`${BACK_URL}/upload/`, bdy))
        if ((index % 3 == 0 && index != 0) || index == (fileObj.files.length - 1)) {
          await Promise.all(rr)
          rr = []
          batch.value.push({ k: index })
          to_upload_files.value = `uploaded ${index + 1} files`
        }
        count = index + 1
      }
      to_upload_files.value = `uploaded ${count} files`
      fileObj.value = null
      batch.value = []
    }

    function listFiles() {
      let fileObj = document.getElementById('savingfiles')
      console.log({ fileObj });
    }

    return { uploadFiles, listFiles, to_upload_files, batch }
  }
}
</script>

<style scoped>
.load-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 10px;
  padding: 10px;
}

.load-progress {
  min-width: 3em;
  padding: 3px;
  margin: 2px;
  background-color: darkcyan;
  color: white;
  border: 2px solid darkblue;
  border-radius: 5px;
}

button {
  margin-top: 20px;
  margin-bottom: 20px;
}

.control-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
}
</style>