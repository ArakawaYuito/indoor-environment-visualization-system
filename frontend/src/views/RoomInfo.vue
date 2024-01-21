<script>
///仮のデータを作る用の関数//////////////////////
function generateData(count, yrange) {
    var i = 0;
    var series = [];
    while (i < count) {
        var x = (i + 1).toString();
        var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

        series.push({
            x: x,
            y: y
        });
        i++;
    }
    return series;
}

// 折れ線グラフ用のデータを作る関数
function generateLineData(yrange) {
    var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    return y;
}
//////////////////////////////////////////////////


import { computed, ref, watch, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Loading from '../components/Loading.vue'
import RoomTemp from '../components/RoomTemp.vue'
import RoomHumid from '../components/RoomHumid.vue'
import RoomPpm from '../components/RoomPpm.vue'
import PlotLine from '../components/Plot.vue'
import { useStore } from '../store/store.js'
import moment from 'moment'

//アイコン
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiTemperatureCelsius, mdiPercentOutline, mdiShoeBallet } from '@mdi/js';
import { ElNotification } from 'element-plus'

// 各部屋の間取りのSVGコンポーネントをインポート/////
import RoomSample from '../assets/roomSample.svg'
import RoomHome from '../assets/roomHome.svg'
/////////////////////////////////////////////////

import anime from 'animejs/lib/anime.es.js';

export default {
    props: {
        roomName: {
            type: String,
            required: true
        }
    },
    components: {
        RoomSample,
        RoomHome,
        Loading,
        RoomTemp,
        RoomHumid,
        RoomPpm,
        SvgIcon,
        PlotLine
    },
    setup(props) {
        const process =ref(true)
        const centerDialogVisible = ref(false)
        const selectedDate = ref('')
        const optionTimeValue = ref('')
        const selectedTime = ref('')
        const timeOptions = ref('')
        const defaultTime = new Date()
        const selectedCellTempValue = ref("--")
        const selectedCellHumidValue = ref("--")
        const selectedCellPpmValue = ref("--")
        const show = ref("temp")

        // 折れ線グラフ用の変数
        const plot_data_series = ref([]);
        const timeLine = ref([]);


        let roomComponent = ""
        switch (props.roomName) {
            case "House":
                roomComponent = RoomHome
                break
            case "31A":
                roomComponent = RoomSample
                break
            case "31B":
                roomComponent = RoomSample
                break
            case "32A":
                roomComponent = RoomSample
                break
            case "32B":
                roomComponent = RoomSample
                break
        }

        // 部屋の温度分布と湿度分布のデータを子コンポーネントと共有する
        const store = useStore()
        provide('store', store);

        // バックエンドから温度分布と湿度分布を取得・更新する/////////
        let seriesTemp = []
        let scaled_seriesTemp = []
        let seriesHumid = []
        let scaled_seriesHumid = []
        let seriesPpm = []
        let scaled_seriesPpm = []

        const UpdateDistribution = async () => {
            process.value=true
            const seriesTempHumidPpm=await fetch('/api/db/distribution/'+props.roomName, {
                method: "GET", 
            }).then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not OK");
                }
                return response.json()
            })
            .catch((error) => {
                console.error("There has been a problem with your fetch operation:", error);
            }); //-> array shape: [[[], []],  [[], []]]

            seriesTemp = seriesTempHumidPpm[0][0]
            scaled_seriesTemp = seriesTempHumidPpm[0][1]

            seriesHumid = seriesTempHumidPpm[1][0]
            scaled_seriesHumid = seriesTempHumidPpm[1][1]

            seriesPpm = seriesTempHumidPpm[2][0]
            scaled_seriesPpm = seriesTempHumidPpm[2][1]

            process.value=false

            // 取得した温度分布をstoreに保存
            store.actions.update_seriesTemp(seriesTemp)
            store.actions.update_scaled_seriesTemp(scaled_seriesTemp)
            // 取得した湿度分布をstoreに保存
            store.actions.update_seriesHumid(seriesHumid)
            store.actions.update_scaled_seriesHumid(scaled_seriesHumid)
            // 取得した二酸化炭素濃度分布をstoreに保存
            store.actions.update_seriesPpm(seriesPpm)
            store.actions.update_scaled_seriesPpm(scaled_seriesPpm)

            // 更新した温湿度の分布をそれぞれデータベースに保存
            PostDb(seriesTempHumidPpm, selectedTime.value)
        };
        // バックエンドから温度分布と湿度分布を取得する//////////
        UpdateDistribution()

        //////////////////////////////////////////////////////
        //バックエンドからセンサ値の時系列データを取得・更新する
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
                // console.log(res.data)
                // console.log(res.time)

                plot_data_series.value = [{
                    name: 'Temperature',
                    data: res.temp
                }, {
                    name: 'Humidity',
                    data: res.humid
                }, {
                    name: 'CO2',
                    data: res.Co2
                }]
                timeLine.value = res.time

            } catch (e) {
                console.error("There has been a problem with your fetch operation:", e);
            }
        }
        //////////////////////////////////////////////////////
        //バックエンドからセンサ値を取得する
        update_timeSeries(props.roomName)

        // 日本時間を取得しisoフォーマットに変換
        selectedTime.value = moment().format('YYYY-MM-DD_HH:mm:ss')

        // 温湿度分布をデータベースに保存する関数
        const PostDb = async (array_temp_humid_ppm, datetime) => {
            await fetch('/api/db/post/distribution/' + datetime, {
                method: "POST",
                // レスポンスをキャッシュする方法を指定
                cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
                headers: {
                    // リクエストの本文がJSON文字列であることを示す
                    "Content-Type": "application/json",
                },
                // リクエストの本文データを指定// 型は "Content-Type" ヘッダーと一致させる
                body: JSON.stringify(array_temp_humid_ppm), //JSON文字列に変換
            }).then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not OK");
                }
            })
                .catch((error) => {
                    console.error("There has been a problem with your fetch operation:", error);
                });
        };
        // 分布が保存されている日時リストをデータベースから取得する関数
        const GetDbDate = async (date) => {
            if (date != null) {
                let list_datetime = await fetch('/api/db/distribution/date/' + date, {
                    method: "GET",
                }).then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not OK");
                    }
                    return response.json()
                }).catch((error) => {
                    console.error("There has been a problem with your fetch operation:", error);
                });

                let count = 0
                timeOptions.value = list_datetime.map((el) => {
                    const date = new Date(el.replace('_', 'T'));
                    //時、分、秒を取得
                    const hours = date.getHours();
                    const minutes = date.getMinutes();
                    const seconds = date.getSeconds();

                    // フォーマットした日付文字列を生成
                    const formattedDate = `${hours}：${minutes}：${seconds}`;

                    count++
                    return { id: count, value: el, label: formattedDate };


                })

                if (timeOptions.value.length > 0) {
                    // Data existsを表示
                    ElNotification({
                        title: 'Data exists',
                        message: 'There is more than one data',
                        type: 'success',
                    })
                } else {
                    // 'no Data' を表示
                    ElNotification({
                        title: 'No data',
                        message: 'There is no data available',
                        type: 'warning',
                    })
                }
            }
        };

        // 日付を変更した際のイベント
        const onChangedDate = () => {
            if (selectedDate.value == '') {
                ElNotification({
                    title: 'Error',
                    message: 'Please make sure to select one date',
                    type: 'error',
                })
            } else {
                GetDbDate(selectedDate.value)
            }
        }

        const onSelectTime = async () => {
            if (optionTimeValue.value == '') {
                ElNotification({
                    title: 'Error',
                    message: 'Please make sure to select one of the suggested times',
                    type: 'error',
                })
            } else {
                selectedTime.value = optionTimeValue.value

                // 文字列型が返ってくる
                const json_seriesTempHumidPpm = await fetch('/api/db/get/distribution/' + selectedTime.value, {
                    method: "GET",
                }).then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not OK");
                    }
                    return response.json()
                })
                    .catch((error) => {
                        console.error("There has been a problem with your fetch operation:", error);
                    });

                // 文字列型をjavascriptオブジェクトに変換
                const seriesTempHumidPpm = JSON.parse(json_seriesTempHumidPpm) //-> array shape: [[[], []],  [[], []]]

                seriesTemp = seriesTempHumidPpm[0][0]
                scaled_seriesTemp = seriesTempHumidPpm[0][1]

                seriesHumid = seriesTempHumidPpm[1][0]
                scaled_seriesHumid = seriesTempHumidPpm[1][1]
                
                seriesPpm = seriesTempHumidPpm[2][0]
                scaled_seriesPpm = seriesTempHumidPpm[2][1]

                // 取得した温度分布をstoreに保存
                store.actions.update_seriesTemp(seriesTemp)
                store.actions.update_scaled_seriesTemp(scaled_seriesTemp)
                // 取得した湿度分布をstoreに保存
                store.actions.update_seriesHumid(seriesHumid)
                store.actions.update_scaled_seriesHumid(scaled_seriesHumid)
                // 取得した二酸化炭素濃度分布をstoreに保存
                store.actions.update_seriesPpm(seriesPpm)
                store.actions.update_scaled_seriesPpm(scaled_seriesPpm)
            }

        }


        // クリックされたセルの座標を引数として、その座標の値を取得
        const cellClicked = (e) => {
            selectedCellTempValue.value = store.getters.getTempValue(e)
            selectedCellHumidValue.value = store.getters.getHumidValue(e)
            selectedCellPpmValue.value = store.getters.getPpmValue(e)
        }

        // 折れ線グラフに表示するデータを更新する
        const update_Dist_TimeSeries = async (roomName) => {
            // 日本時間を取得
            selectedTime.value = moment().format('YYYY-MM-DD_HH:mm:ss')

            //////////////////////////////////////////////////////
            //バックエンドからセンサ値の時系列データを更新する
            update_timeSeries(props.roomName)
            ///////////////////////////////////////////////////////

            ////////////////////////////////////////////////
            ///温湿度分布を更新する
            UpdateDistribution()
            ////////////////////////////////////////////////
        }


        // 温度/湿度/二酸化炭素濃度タブの切り替え
        const changeShow = (value) => {
            show.value = value
        }

        // 温度と湿度の数値をドラムロールのアニメーションで変化させる
        const animationChangeTemp = () => {
            var selectedCellTemp = document.querySelector('#selectedCellTemp');
            var selectedCellHumid = document.querySelector('#selectedCellHumid');
            var selectedCellPpm = document.querySelector('#selectedCellPpm');

            var selectedCellValues = {
                temperature: '',
                humidity: '',
                ppm: ''
            };

            anime({
                targets: selectedCellValues,
                temperature: selectedCellTempValue.value,
                humidity: selectedCellHumidValue.value,
                ppm: selectedCellPpmValue.value,
                round: 10,
                easing: 'linear',
                duration: 200,
                update: function () {
                    selectedCellTemp.innerHTML = selectedCellValues.temperature
                    selectedCellHumid.innerHTML = selectedCellValues.humidity
                    selectedCellPpm.innerHTML = selectedCellValues.ppm
                }
            });
        }

        watch(selectedCellTempValue, (newX) => {
            animationChangeTemp()
        })

        return {
            process,
            centerDialogVisible,
            optionTimeValue,
            selectedDate,
            defaultTime,
            onChangedDate,
            onSelectTime,
            selectedTime,
            timeOptions,
            show,
            roomComponent,
            pathTemp: mdiTemperatureCelsius,
            pathPercent: mdiPercentOutline,
            selectedCellTempValue,
            selectedCellHumidValue,
            selectedCellPpmValue,
            cellClicked,
            update_Dist_TimeSeries,
            changeShow,
            plot_data_series,
            timeLine
        }
    }
}
</script>

<template>
    <!-- Card Section -->
    <div class="max-w-[85rem] px-4 pb-10 sm:px-6 lg:px-8 lg:pb-14 mx-auto">
        <!-- Grid -->
        <div class="grid lg:grid-cols-[minmax(450px,_2fr)_1fr] gap-3 sm:gap-6">
            <div>
                <div class="tabs tabs-bordered  mr-5">
                    <a class="tab text-gray-500"
                        :class="{ 'tab-active border-b-2 border-self_blue text-self_blue': show === 'temp' }"
                        @click="changeShow('temp')">Temperature</a>
                    <a class="tab text-gray-500"
                        :class="{ 'tab-active border-b-2 border-self_blue text-self_blue': show === 'humid' }"
                        @click="changeShow('humid')">Humidity</a>
                    <a class="tab text-gray-500"
                        :class="{ 'tab-active border-b-2 border-self_blue text-self_blue': show === 'ppm' }"
                        @click="changeShow('ppm')">CO2</a>
                </div>
            </div>


            <div class="flex justify-between mx-5">
                <!-- Card -->
                <el-descriptions class="margin-top" :column="2" size="large" border>
                    <el-descriptions-item>
                        <template #label>
                            <div class="cell-item">
                                <el-icon>
                                    <location />
                                </el-icon>
                                Place
                            </div>
                        </template>
                        {{ roomName }}
                    </el-descriptions-item>

                    <el-descriptions-item>
                        <template #label>
                            <div class="cell-item">
                                <el-icon>
                                    <Calendar />
                                </el-icon>
                                Datetime
                            </div>
                        </template>
                        {{ selectedTime }}
                    </el-descriptions-item>
                </el-descriptions>
                <div>
                    <el-tooltip content="Update Data" placement="top">
                        <el-button class="w-10 ml-5 mt-1" type="primary" @click="update_Dist_TimeSeries">
                            <el-icon>
                                <Refresh />
                            </el-icon>
                        </el-button>
                    </el-tooltip>
                    <el-tooltip content="Date Time Selection Form" placement="bottom">
                        <el-button type="info" class="w-10 ml-5 mt-1" @click="centerDialogVisible = true">
                            <el-icon>
                                <MoreFilled />
                            </el-icon>
                        </el-button>
                    </el-tooltip>
                </div>
            </div>
            <div
                class="mr-5 p-8 group flex flex-col items-center lg:row-start-2 lg:row-span-2 bg-self_darkPurple border border-gray-200 shadow-sm rounded-xl dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7] ">
                <div class="h-[400px] w-[350px] flex justify-center items-center">
                    <div class="relative h-[370px] w-[350px] ">
                        <component :is="roomComponent" class="absolute inset-x-0 m-auto  pointer-events-none" />
                        <Loading v-if="process" />
                        <RoomTemp v-show="!process" v-if='show === "temp"' @cellClicked="cellClicked" class="absolute" :height="230"
                            :width="350" style="top: 7rem; left:0rem;" />
                        <RoomHumid v-show="!process" v-else-if='show === "humid"' @cellClicked="cellClicked" class="absolute" :height="230" :width="350"
                            style="top: 7rem; left:0rem;" />
                        <RoomPpm v-show="!process" v-else @cellClicked="cellClicked" class="absolute" :height="230" :width="350"
                            style="top: 7rem; left:0rem;" />
                    </div>
                </div>

            </div>
            <!-- End Card -->

            <el-dialog v-model="centerDialogVisible" title="Select the date time to visualize"
                class="lg:w-2/5 md:w-3/5 sm:w-4/5 w-11/12 " align-center>
                <el-form label-position="left" label-width="100px">
                    <el-space fill>
                        <el-alert type="info" show-icon :closable="false">
                            <p>First, please select a date</p>
                            <p>
                                <el-icon>
                                    <WarnTriangleFilled />
                                </el-icon>
                                You must select a date to present a candidate time
                            </p>
                        </el-alert>
                        <el-form-item label="Date" class="px-10">
                            <div class="block w-3/5">
                                <el-date-picker v-model="selectedDate" type="date" placeholder="Pick a date"
                                    :default-value="defaultTime" format="YYYY/MM/DD" value-format="YYYY-MM-DD"
                                    @change="onChangedDate" class="w-full" />
                            </div>
                        </el-form-item>
                    </el-space>
                    <el-space fill>
                        <el-alert type="info" show-icon :closable="false">
                            <p>
                                The data stored in the database on the date you choose are the options
                            </p>
                        </el-alert>
                        <el-form-item label="Time" class="px-10">
                            <div class="block w-3/5">
                                <el-select v-model="optionTimeValue" class="w-full" placeholder="Select a time">
                                    <el-option v-for="item in timeOptions" :key="item.id" :label="item.label"
                                        :value="item.value" />
                                </el-select>
                            </div>
                        </el-form-item>
                    </el-space>
                </el-form>
                <template #footer>
                    <span class="dialog-footer">
                        <el-button @click="centerDialogVisible = false">Cancel</el-button>
                        <el-button type="primary" @click="centerDialogVisible = false; onSelectTime()">
                            Confirm
                        </el-button>
                    </span>
                </template>
            </el-dialog>
            <!-- Card -->
            <div class="grid lg:h-[500px] lg:grid-cols-1 grid-cols-3 gap-4 mr-5">
                <div
                    class="group lg:mt-1 grid-item bg-white border border-gray-200 shadow-sm rounded-xl dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
                    <div class="h-full flex items-end justify-start">
                        <div class="flex flex-col">
                            <div class="mt-2 lg:ml-8 lg:mb-5 ml-4 mb-4 font-bold sm:text-xl md:text-2xl text-gray-500">Temperature</div>
                            <div class="flex items-center justify-center lg:ml-8 lg:mb-2 lg:mt-2">
                                <p id="selectedCellTemp" class="text-self_darkPurple font-bold sm:text-2xl md:text-5xl ml-8 mb-8">
                                    {{ selectedCellTempValue }}
                                </p>
                                <svg-icon class="text-gray-500" type="mdi" :path="pathTemp"></svg-icon>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- End Card -->
                <!-- Card -->
                <div
                    class="group grid-item bg-white border border-gray-200 shadow-sm rounded-xl dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
                    <div class="h-full flex items-end justify-start">
                        <div class="flex flex-col">
                            <div class="mt-2 lg:ml-8 lg:mb-5 ml-4 mb-4 font-bold sm:text-xl md:text-2xl text-gray-500">Humidity</div>
                            <div class="flex items-center justify-center lg:ml-8 lg:mb-2 lg:mt-2">
                                <p id="selectedCellHumid" class="text-self_darkPurple font-bold sm:text-2xl md:text-5xl ml-8 mb-8">
                                    {{ selectedCellHumidValue }}
                                </p>
                                <svg-icon class="text-gray-500" type="mdi" :path="pathPercent"></svg-icon>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Card -->
                <div
                    class="group grid-item bg-white border border-gray-200 shadow-sm rounded-xl dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
                    <div class="h-full flex items-end justify-start">
                        <div class="flex flex-col">
                            <div class="mt-2 lg:ml-8 lg:mb-5 ml-4 mb-4 font-bold sm:text-xl md:text-2xl text-gray-500">CO2</div>
                            <div class="flex items-center justify-center lg:ml-8 lg:mb-2 lg:mt-2">
                                <p id="selectedCellPpm" class="text-self_darkPurple font-bold sm:text-2xl md:text-5xl ml-8 mb-8">
                                    {{ selectedCellPpmValue }}
                                </p>
                                <span class="font-bold text-gray-500">ppm</span>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- End Card -->
            </div>
            <!-- Card -->
            <div
                class="lg:col-span-2 mt-5 mr-5 bg-white border border-gray-200 shadow-sm rounded-xl dark:bg-slate-900 dark:border-gray-700 dark:shadow-slate-700/[.7]">
                <div class=" h-[380px] w-full">
                    <!-- {{ plot_data_series }} -->
                    <PlotLine :series="plot_data_series" :timeLine="timeLine"/>
                </div>
            </div>
            <!-- End Card -->
        </div>
        <!-- End Grid -->


    </div>
</template>

<style scoped>
.dialog-footer button:first-child {
    margin-right: 10px;
}

.block {
    border-right: solid 1px var(--el-border-color);
}

.block:last-child {
    border-right: none;
}

.demonstration {
    display: block;
    color: var(--el-text-color-secondary);
    font-size: 14px;
    margin-bottom: 20px;
}

.el-button:hover {
    opacity: 0.5;
}
</style>
