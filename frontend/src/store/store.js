import { ref, computed, readonly } from 'vue'
export function useStore() {
    //state
    const seriesTemp = ref([])
    const scaled_seriesTemp = ref([])
    const seriesHumid = ref([])
    const scaled_seriesHumid = ref([])
    const seriesPpm = ref([])
    const scaled_seriesPpm = ref([])

    // 折れ線グラフに使用するデータ点の数
    const maxsize=10
    const tempLine = ref([])
    const humidLine = ref([])
    const timeLine = ref([])

    //getter
    const getters = {
        // index: [seriesIndex, dataPointIndex]
        getTempValue: (index) =>{
            return seriesTemp.value[index[0]].data[index[1]].y
        },     
        getHumidValue: (index) =>{
            return seriesHumid.value[index[0]].data[index[1]].y
        }, 
        getPpmValue: (index) =>{
            return seriesPpm.value[index[0]].data[index[1]].y
        }
    }

    //action
    const actions = {
        update_seriesTemp: (payload)=>{
            seriesTemp.value = payload
        },
        update_scaled_seriesTemp: (payload)=>{
            scaled_seriesTemp.value = payload
        },

        update_seriesHumid: (payload)=>{
            seriesHumid.value = payload
        },                
        update_scaled_seriesHumid: (payload)=>{
            scaled_seriesHumid.value = payload
        },   
        update_seriesPpm: (payload)=>{
            seriesPpm.value = payload
        },
        update_scaled_seriesPpm: (payload)=>{
            scaled_seriesPpm.value = payload
        },
             
    }

    return{
        seriesTemp,
        scaled_seriesTemp,
        seriesHumid,
        scaled_seriesHumid,
        seriesPpm,
        scaled_seriesPpm,
        tempLine,
        humidLine,
        timeLine,
        getters,
        actions
    }

  }