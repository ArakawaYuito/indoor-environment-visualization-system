<script>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

export default {
    setup(props) {
        const router = useRouter()
        const isCollapse = ref(true)
        const handleOpen = (key, keyPath) => {
            console.log(key, keyPath)
        }
        const handleClose = (key, keyPath) => {
            console.log(key, keyPath)
        }
        const onClick =(room)=>{
            router.push({ name: 'RoomInfo', params: { roomName: room} })              
        }
        const goBack = () => {
            console.log('go back')
            }

        return {
            isCollapse,
            handleOpen,
            handleClose,
            onClick,
            ArrowLeft,
            goBack
        }   
    }
}


</script>


<template>
    <div class="flex h-full bg-self_blueWhite overflow-y-auto">
        <el-menu 
        default-active="2" 
        class="sticky top-0 el-menu-vertical-demo" 
        :collapse="isCollapse" 
        @open="handleOpen"
        @close="handleClose"
        >
            <el-radio-group v-model="isCollapse" style="margin: 10px">
                <el-radio-button :label="false" v-if="isCollapse">
                    <el-icon>
                        <Expand />
                    </el-icon>
                </el-radio-button>
                <el-radio-button :label="true" v-else>
                    <el-icon>
                        <CloseBold />
                    </el-icon>
                </el-radio-button>
            </el-radio-group>
            <el-menu-item index="1">
                <router-link to="/">
                    <el-icon>
                        <House />
                    </el-icon>
                </router-link>
                <template #title><router-link to="/">Home</router-link></template>
            </el-menu-item>

            <el-sub-menu index="2">
                <template #title>
                    <router-link to="/system">
                        <el-icon>
                            <Menu />
                        </el-icon>
                    </router-link>
                    <span><router-link to="/system">System</router-link></span>
                </template>
                <el-menu-item-group>
                    <template #title><span>Rooms</span></template>
                    <el-menu-item class="text-slate-900" index="2-1" @click="onClick('House')">House</el-menu-item>
                    <el-menu-item class="text-slate-900" index="2-2" @click="onClick('31A')">31A</el-menu-item>
                    <el-menu-item class="text-slate-900" index="2-3" @click="onClick('31B')">31B</el-menu-item>
                    <el-menu-item class="text-slate-900" index="2-4" @click="onClick('32A')">32A</el-menu-item>
                    <el-menu-item class="text-slate-900" index="2-5" @click="onClick('32B')">32B</el-menu-item>
                </el-menu-item-group>
            </el-sub-menu>
            <el-menu-item index="3">
                <router-link to="/about">
                    <el-icon>
                        <Guide />
                    </el-icon>
                </router-link>
                <template #title><router-link to="/about">About</router-link></template>
            </el-menu-item>
        </el-menu>


        <div class="w-full pt-5 px-4 sm:px-6 md:px-8">
            <div class="flex">
                <el-page-header :icon="ArrowLeft" @back="$router.back" class="back w-24">
                </el-page-header>
                    <span class="text-large font-600 mr-3 ml-3 title"> System </span>
                </div>
            <el-divider />
            <router-view :key="$route.params.roomName"/>
        </div>
    </div>
</template>


<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu-vertical-demo a {
    font-weight: bold;
    color: #2c3e50;
}

.el-menu-vertical-demo a:hover {
    opacity: 0.5;
}

.el-menu-vertical-demo a.router-link-active {
    color: #42b983;
    font-weight: bold;
}

.back:hover{
  opacity: 0.5;
}


</style>