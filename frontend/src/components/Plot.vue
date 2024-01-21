<script>
import { ref, isReactive, isRef, watch, toRefs} from 'vue'
import VueApexCharts from "vue3-apexcharts"

export default {
  props: {
    series: {
      type: Array,
      required: true
    },
    timeLine: {
      type: Array,
      required: true
    }
  },

  components: {
    apexchart: VueApexCharts,
  },

  setup(props, ctx) {
    const {series, timeLine} = toRefs(props)
    const time=ref([])
    time.value=timeLine.value.map(element => new Date(element))

    const chartOptions = ref({
      chart: {
        height: 350,
        type: 'area'
      },

      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      title: {
        text: 'Sensor values from past to current time',
        align: 'center',
        margin: 50,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
            fontSize:  '14px',
            fontWeight:  'bold',
            fontFamily:  undefined,
            color:  '#263238'
        },
      },
      xaxis: {
        type: 'datetime',
        categories: time.value,
        labels: {
            datetimeUTC: false,
            format: 'HH:mm:ss',
        }
      },
      yaxis: [
        {
          title: {
            text: "Temperature"
          },
        },
        {
          title: {
            text: "Humidity"
          }
        },
        {
          opposite: true,
          title: {
            text: "CO2"
          }
        }
      ],
      tooltip: {
        x: {
          format: 'MM/dd HH:mm:ss'
        },
      }
    })

    watch(timeLine, (newTimeLine)=>{
      chartOptions.value.xaxis.categories=newTimeLine
    })



    return {
      series,
      chartOptions,
    }
  }
}
</script>

<template>
  <div id="chart">
    <!-- {{ series }} -->
    <apexchart :key="timeLine" type="area" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<style scoped></style>
