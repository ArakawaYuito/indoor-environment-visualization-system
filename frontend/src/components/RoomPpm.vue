<script>
import { inject } from 'vue'
import VueApexCharts from "vue3-apexcharts"

export default{
    emits: ['cellClicked'],
    components: {
        VueApexCharts,
    },
    props:{
        height:{
        type:Number,
        required:true
        },
        width:{
        type:Number,
        required:true
        }
    },

    setup(props, ctx){
        const store = inject('store');
        const series = store.seriesPpm
        const scaled_series = store.scaled_seriesPpm
    
        const chartOptions = {
                chart: {
                    type: 'heatmap',
                    toolbar: {
                        show: false,

                    },
                },
                plotOptions:{
                    heatmap:{
                        //ヒートマップのセルの角のradius
                        radius: 3
                    }
                    
                },
                //　ヒートマップのセルの枠の色と幅
                stroke:{
                    colors: ['#1D1D3F'],
                    width: 2,
                },
                // セルの色
                colors: ["#66FFB2"],
                // 軸ラベルなどのいらないものを非表示
                grid:{
                    show: false
                },
                tooltip: {
                    y:{
                        formatter:function(value, { series, seriesIndex, dataPointIndex, w }){
                            const selected2DIndex = [seriesIndex, dataPointIndex]
                            return store.getters.getPpmValue(selected2DIndex)
                        }
                    }
                },
                xaxis: {
                        labels:{
                            show:false
                        },
                        tooltip:{
                        enabled:false
                        },
                        axisBorder:{
                        show:false
                        },
                        axisTicks:{
                        show:false
                        }
                        
                },
                yaxis: {
                        labels:{
                            show:false
                        },
                        tooltip:{
                        enabled:false
                        },
                        axisBorder:{
                        show:false
                        },
                        axisTicks:{
                        show:false
                        },
                        crosshairs: {
                            show: false,
                        },
                },
                dataLabels: {
                enabled: false
                },
        }

        // クリックしたセルのインデックスを取得
        // この方法はドキュメントに記載がなかったため issue参考：https://github.com/apexcharts/vue3-apexcharts/issues/20
        const cellClicked = (event, chartContext, config)=>{
            const seriesIndex = config.seriesIndex
            const dataPointIndex = config.dataPointIndex
            const selected2DIndex = [seriesIndex, dataPointIndex]
            // const selectedCellValue = series[seriesIndex].data[dataPointIndex].y
            // console.log("selected data:", `[${seriesIndex}][${dataPointIndex}]`)
            // console.log(selectedCellValue )
            ctx.emit("cellClicked", selected2DIndex)

        }

        return {
            series,
            scaled_series,
            chartOptions,
            cellClicked

        }
    }
}
</script>

<template>
<div id="chart">
    <VueApexCharts :height="height" :width="width" :options="chartOptions" :series="scaled_series" @dataPointSelection="cellClicked" :key="series"/>
</div>
</template>

<style scoped>

</style>
