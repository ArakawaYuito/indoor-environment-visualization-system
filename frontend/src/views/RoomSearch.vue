<script>
import RoomCard from '../components/RoomCard.vue'
import SystemMain from '../components/SystemMain.vue'
import gsap from "gsap";

export default{
    components:{
        SystemMain,
        RoomCard
    },
    setup(){
        const rooms = ["House", "31A", "31B", "32A", "32B"]
       
        // パネルのスタート設定
        const panelsBeforeEnter = (el) => {
            gsap.set(el, {
                y: 100,
                opacity: 0
            })
        }
        // パネルのアニメーション設定
        const panelsEnter = (el, done) => {
            gsap.to(el, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                delay: el.dataset.index * 0.2,
                onComplete: done
            })
        }
        return { rooms, panelsBeforeEnter, panelsEnter }
    }
}
</script>

<template>    
    <div>
        <SystemMain/>
        <header>
        <h1 class="block text-2xl font-bold text-gray-800 sm:text-3xl dark:text-white">Rooms</h1>
        </header>

        <!-- Card Section -->
        <div class="panels py-10">
            <!--ここからtransitionコードを開始-->
            <transition-group
            tag="div"
            class="panels-grid"
            appear
            @before-enter="panelsBeforeEnter"
            @enter="panelsEnter"
            >
                <div
                v-for="(room, index) in rooms"
                :key="room" 
                class="panel"
                :data-index="index"
                >
                    <!-- Card -->
                    <RoomCard :room-name="room"/>
                    <!-- End Card -->
                </div>
            </transition-group>
            <!--ここでtransitionをクローズ-->
        </div>
        <!-- End Card Section -->
    </div>
</template>

<style scoped>
.panels{
    margin-top: 5%;
}

.panels-grid {
    display: grid;
    margin: 0 auto;
    grid-gap: 0.75rem;
    max-width: 1200px;
}


@media (min-width: 640px) {
  .panels-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 768px) {
  .panels-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .panels-grid { grid-template-columns: repeat(4, 1fr); }
}

</style>