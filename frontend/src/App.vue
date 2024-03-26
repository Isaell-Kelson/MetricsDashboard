<template>
  <div id="app">
    <div class="container">
      <h1>Upload de Arquivo e Visualização de Dados</h1>
      <label for="file-upload" class="upload-btn">Selecionar Arquivo</label>
      <input id="file-upload" type="file" @change="handleFileUpload" class="file-input" accept=".xlsx">
      <button @click="uploadFile" class="send-btn">Enviar</button>

      <div v-if="fileName" class="file-name">Arquivo selecionado: {{ fileName }}</div>

      <div v-if="data" class="chart-container">
        <canvas ref="myChart" class="chart"></canvas>
        <div class="data-container">
          <h2>Dados Coletados</h2>
          <ul>
            <li><strong>Quantidade de Cobranças:</strong> {{ data.quantidade_de_cobrancas }}</li>
            <li><strong>Média de Cobrança a Cada Dias:</strong> {{ data.media_de_cobranca_a_cada_dias.toFixed(1) }}</li>
            <li><strong>Status Count:</strong> {{ data.status_count }}</li>
            <li><strong>Data de Início Mínima:</strong> {{ data.data_inicio_min }}</li>
            <li><strong>Data de Início Máxima:</strong> {{ data.data_inicio_max }}</li>
            <li><strong>Data de Cancelamento Mínima:</strong> {{ data.data_cancelamento_min }}</li>
            <li><strong>Data de Cancelamento Máxima:</strong> {{ data.data_cancelamento_max }}</li>
            <li><strong>Intervalo de Tempo Total:</strong> {{ data.intervalo_tempo_total }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  data() {
    return {
      file: null,
      fileName: '', 
      data: null,
      myChart: null
    };
  },
  methods: {
    handleFileUpload(event) {
      const selectedFile = event.target.files[0];
      if (selectedFile && selectedFile.name.endsWith('.xlsx')) {
        this.file = selectedFile;
        this.fileName = this.file.name;
      } else {
        this.file = null;
        this.fileName = '';        
        alert('Por favor, selecione um arquivo no formato .xlsx.');
      }
    },
    uploadFile() {
      if (!this.file) {        
        alert('Por favor, selecione um arquivo para enviar.');
        return;
      }
      
      const formData = new FormData();
      formData.append('file', this.file);

      axios.post('http://127.0.0.1:5001', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.data = response.data;
        this.$nextTick(() => {
          this.renderChart();
        });
      })
      .catch(error => {
        console.error('Erro ao fazer upload do arquivo:', error);
      });
    },
    renderChart() {
      if (this.data && this.$refs.myChart && this.$refs.myChart.getContext) {
        const ctx = this.$refs.myChart.getContext('2d');
        this.myChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho'],
            datasets: [{
              label: 'My Dataset',
              data: [65, 59, 80, 81, 56, 55, 40],
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }
  },
  watch: {
    data() {
      this.renderChart();
    }
  }
};
</script>


<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.file-input {
  display: none;
}

.file-name {
  margin-top: 10px;
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
  
}

#file-upload {
  display: none;
}

.upload-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  margin: 15px;
  font-size: 16px;
  cursor: pointer;
}

.send-btn {
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.chart-container {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 100%;
  max-width: 600px;
}

.data-container {
  margin-top: 20px;
  text-align: left;
}

.data-container h2 {
  font-size: 20px;
}

.data-container ul {
  list-style: none;
  padding: 0;
}

.data-container li {
  margin-bottom: 10px;
}
</style>
