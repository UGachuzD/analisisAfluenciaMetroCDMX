<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="1000px">
      <v-row>
        <v-col>
          <h1 class="text-center">AFLUENCIA METRO CDMX</h1>
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <p>Seleccione alguna opción de los siguientes campos:</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="8">
          <v-select
            clearable
            label="Mes"
            :items="meses"
            variant="outlined"
            v-model="selectedMes"
          ></v-select>
        </v-col>
        <v-col cols="4">
          <v-select
            clearable
            label="Año"
            :items="anios"
            variant="outlined"
            v-model="selectedAnio"
          ></v-select>
        </v-col>
        <v-col>
          <v-card min-height="600px">
            <v-card-title>Mapa interactivo</v-card-title>
            <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
            <v-card-text>
              Haga clic en la estacion de metro para ver la afluencia
              <iframe
                v-if="iframeSrc"
                ref="iframe"
                :src="iframeSrc"
                width="100%"
                height="400px"
                frameborder="0"
              ></iframe>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" @click="limpiarCampos">Limpiar campos</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from "vue";

// Definir los datos para los selectores
const meses = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];

const anios = [
  "2010",
  "2011",
  "2012",
  "2013",
  "2014",
  "2015",
  "2016",
  "2017",
  "2018",
  "2019",
  "2020",
  "2021",
  "2022",
  "2023",
  "2024",
];

const selectedMes = ref("");
const selectedAnio = ref("");
const iframeSrc = ref("");

// Computed property para el subtítulo
const subtitle = computed(() => {
  if (selectedMes.value && selectedAnio.value) {
    return `${selectedMes.value} ${selectedAnio.value}`;
  } else {
    return "Seleccione un mes y un año";
  }
});

const limpiarCampos = () => {
  selectedMes.value = "";
  selectedAnio.value = "";
  iframeSrc.value = "";
};

// Watcher para actualizar el iframeSrc cuando se cambien los valores seleccionados
watch([selectedMes, selectedAnio], () => {
  if (selectedMes.value && selectedAnio.value) {
    iframeSrc.value = `http://127.0.0.1:5000/map?mes=${selectedMes.value}&anio=${selectedAnio.value}`;
  } else {
    iframeSrc.value = "";
  }
});

</script>
