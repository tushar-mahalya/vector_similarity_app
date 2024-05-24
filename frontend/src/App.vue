<template>
  <main>
    <!-- <header> -->
      <!-- <h1>All files</h1>
      <button class="add-button" @click="triggerFileInput">+</button>
      <input ref="fileInput" type="file" accept=".txt" style="display: none" @change="handleFileUpload" />
    </header>
    <div class="file-cards">
      <div
        v-for="file in files"
        :key="file"
        class="file-card"
        :style="{ backgroundColor: getRandomColor() }"
        @click="showFileContent(file)"
      >
        <span>{{ file }} &nbsp;</span>
        <i class="fas fa-trash-alt delete-icon" @click.stop="deleteFile(file)"></i>
      </div>
    </div>
    <div v-if="showOverlay" class="overlay" @click.self="closeOverlay">
      <div class="overlay-content">
        <span class="close-btn" @click="closeOverlay">&times;</span>
        <pre>{{ fileContent }}</pre>
      </div>
    </div> -->
    <div class="container-fluid">
      <div class="row">
        <div class="container">
          <h1>Uploading CSV file</h1>

          <div class="large-12 medium-12 small-12 cell">
            <label
            >File
          <input
             type="file"
             id="file"
            ref="file"
          />
        </label>
        <button v-on:click="csvTojson()">Submit</button>
          </div>
        </div>
        <div class="table-wrapper">
        <table class="table table-bordered table-hover table-condensed">
          <thead>
            <tr>
              <th title="Field #0">Select</th>
              <th title="Field #1">ID</th>
              <th title="Field #2">A</th>
              <th title="Field #3">B</th>
              <th title="Field #4">C</th>
              <th title="Field #5">D</th>
              <th title="Field #6">E</th>
              <th title="Field #7">F</th>
              <th title="Field #8">G</th>
              <th title="Field #9">H</th>
              <th title="Field #10">I</th>
              <th title="Field #11">J</th>
              <th title="Field #12">K</th>
              <th title="Field #13">L</th>
              <th title="Field #14">M</th>
              <th title="Field #15">N</th>
              <th title="Field #16">O</th>
            </tr>

          </thead>
          <tbody v-for="(data,i) in csvData" :key="i">
            <tr>
              <td><input type="radio" :value="data" v-model="selectedRow"></td>
              <td>{{ data.ID }}</td>
              <td>{{ data.A }}</td>
              <td>{{ data.B }}</td>
              <td>{{ data.C }}</td>
              <td>{{ data.D }}</td>
              <td>{{ data.E }}</td>
              <td>{{ data.F }}</td>
              <td>{{ data.G }}</td>
              <td>{{ data.H }}</td>
              <td>{{ data.I }}</td>
              <td>{{ data.J }}</td>
              <td>{{ data.K }}</td>
              <td>{{ data.L }}</td>
              <td>{{ data.M }}</td>
              <td>{{ data.N }}</td>
              <td>{{ data.O }}</td>
            </tr>
          </tbody>        
        </table>
        </div>
        <button v-on:click="findSimilar">Find Similar</button>
      </div>
      <div v-if="selectedRow">
  <h2>Selected Row Data:</h2>
  <ul>
    <li v-for="(value, key) in selectedRow" :key="key">
      {{ key }}: {{ value }}
    </li>
  </ul>
</div>
    </div>
  </main>
</template>

<script>
// import axios from 'axios';
// import { ref, onMounted } from 'vue';
import papa from 'papaparse';
export default {
  data(){
    return{
      csvData:[],
      selectedRow:null
    }
  },
  methods:{
    csvTojson(){
      let csvFile= this.$refs.file.files[0];

      if( csvFile == undefined){
        alert("Please select a file")
        this.csvData=[];
        return;
      }

      let formData=new FormData();
      formData.append('file', csvFile);

      fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        this.csvData=data;
      })
      .catch((error) => {
        console.error('Error:', error);
      });

      let that=this

      papa.parse(csvFile, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        // preview:100,
        complete(result){
          that.csvData=result.data
        }
      });
    },
  findSimilar() {
    if (this.selectedRow === null) {
      alert('Please select a row first.');
      return;
    }
  }
}
}

// const files = ref([]);
// const showOverlay = ref(false);
// const fileContent = ref('');

// const getRandomColor = () => {
//   const hue = Math.floor(Math.random() * 360);
//   const saturation = 100;
//   const lightness = 75;
//   return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
// };

// const triggerFileInput = () => {
//   const fileInput = document.querySelector('input[type="file"]');
//   fileInput.click();
// };

// const fetchFiles = async () => {
//   try {
//     const response = await axios.get('http://localhost:5000/files');
//     files.value = response.data;
//   } catch (error) {
//     console.error('Error fetching files:', error);
//   }
// };

// const handleFileUpload = async (event) => {
//   const file = event.target.files[0];
//   if (file && file.type === 'text/plain') {
//     const formData = new FormData();
//     formData.append('file', file);

//     try {
//       await axios.post('http://localhost:5000/upload', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });
//       console.log('File uploaded successfully');
//       fetchFiles();
//     } catch (error) {
//       console.error('Error uploading file:', error);
//     }
//   } else {
//     console.error('Please upload a .txt file');
//   }
// };

// const showFileContent = async (fileName) => {
//   try {
//     const response = await axios.get(`http://localhost:5000/files/${fileName}`);
//     fileContent.value = response.data;
//     showOverlay.value = true;
//   } catch (error) {
//     console.error('Error fetching file content:', error);
//   }
// };

// const closeOverlay = () => {
//   showOverlay.value = false;
//   fileContent.value = '';
// };

// const deleteFile = async (fileName) => {
//   try {
//     await axios.delete(`http://localhost:5000/files/${fileName}`);
//     console.log('File deleted successfully');
//     fetchFiles();
//   } catch (error) {
//     console.error('Error deleting file:', error);
//   }
// };

// onMounted(() => {
//   fetchFiles();
// });
</script>

<!-- <style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}
.file-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}
.file-card {
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.delete-icon {
  color: #dc3545;
  cursor: pointer;
}

.add-button {
  font-size: 2rem;
  background-color: #000000;
  color: #fff;
  border: none;
  border-radius: 100%;
  width: 2.5rem;
  height: 2.5rem;
  cursor: pointer;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.overlay-content {
  background-color: #fff;
  padding: 2rem;
  border-radius: 0.5rem;
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
  position: relative;
}
.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style> -->
<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}
.table-wrapper {
  max-height: calc(25 * 1.5em); /* Assuming each row is 1.5em tall */
  overflow-y: auto;
}
.container-fluid {
  margin: 0 auto;
  max-width: 1200px;
  padding: 0 15px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.large-12, .medium-12, .small-12 {
  width: 100%;
}

label {
  display: block;
  margin-bottom: 10px;
}

input[type="file"] {
  margin-bottom: 20px;
}

button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
  color: #333;
}

.table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}
.table tbody tr:hover {
  background-color: #ddd;
  cursor: pointer;
}
</style>