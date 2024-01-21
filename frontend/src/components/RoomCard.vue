<script>
import {ref} from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
    props:{
        roomName:{
            type: String,
            required: true
        }
    },

    setup(props){
        const router = useRouter()
        const temp = ref("--")
        const humid = ref("--")
        const co2 = ref("--")

        const onClick =()=>{
            router.push({ name: 'RoomInfo', params: { roomName: props.roomName } })              

        }
        const update_timeSeries = async (roomName) => {
            const url = "/api/ondotori/" + roomName
            const params = { method: "GET" };
            try {
                let response = await fetch(url, params)
                // レスポンスが正常かどうかをチェック
                if (!response.ok) {
                    throw new Error("Network response was not OK")
                }

                const res = await response.json()
                temp.value=res.temp.pop()
                humid.value=res.humid.pop()
                co2.value=res.Co2.pop()

            } catch (e) {
                console.error("There has been a problem with your fetch operation:", e);
            }
        }
        //////////////////////////////////////////////////////
        //バックエンドからセンサ値を取得する
        update_timeSeries(props.roomName)

        return{
            temp,
            humid,
            co2,
            onClick
        }
    }
}
</script>

<template>    
<!-- Card -->
<div class="group flex flex-col bg-white border shadow-sm rounded-xl hover:shadow-md transition dark:bg-slate-900 dark:border-gray-800 dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600" v-on:click="onClick">
<div class="p-4 md:p-5">
    <div class="flex justify-between items-center">
    <div>
        <h3 class="group-hover:text-blue-600 font-semibold text-gray-800 dark:group-hover:text-gray-400 dark:text-gray-200">
        {{ roomName }}
        </h3>
        <p class="text-sm text-gray-500">Temperature：{{ temp }} ℃</p>
        <p class="text-sm text-gray-500">Humidity：{{ humid }} %</p>
        <p class="text-sm text-gray-500">CO2：{{ co2 }} ppm</p>
    </div>
    <div class="ps-3">
        <svg class="flex-shrink-0 w-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </div>
    </div>
</div>
</div>
<!-- End Card -->

</template>

<style scoped>

</style>
