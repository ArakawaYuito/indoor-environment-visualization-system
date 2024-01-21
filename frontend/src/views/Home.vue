<script>
import { useRouter } from 'vue-router'
import { loadSlim } from "tsparticles-slim";
import gsap from "gsap";
export default {
  name: 'Home',
  setup(props) {
    // ボタンを押したときにシステムページに行けるようにする
    const router = useRouter()
    const getStarted = () => {
      router.push('/system')
    }

    // 背景アニメーションの定義
    const particlesInit = async engine => {
      //await loadFull(engine);
      await loadSlim(engine);
    };
    const particlesLoaded = async container => {
      console.log("Particles container loaded", container);
    };

    // ヘッダーが出てくるアニメーション
    const headerBeforeEnter = (el) => {
      gsap.set(el, {
        y: "-100%",
        opacity: 0
      })
    }
    const headerEnter = (el, done) => {
      gsap.to(el, {
        opacity: 1,
        duration: 0.5,
        delay: 1.2,
        y: "0",
        ease: "Power0.easeOut",
        onComplete: done
      })
    }

    // メニューバーのリンクが出てくるアニメーション
    const linksBeforeEnter = (el) => {
      el.style.opacity = 0
    }
    const linksEnter = (el, done) => {
      gsap.to(el, {
        duration: 0.5,
        opacity: 1,
        delay: 2.5,
        onComplete: done
      })
    }

    // ボタンが出てくるアニメーション
    const panelsBeforeEnter = (el) => {
      gsap.set(el, {
        y: 100,
        opacity: 0
      })
    }
    const panelsEnter = (el, done) => {
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 1.7,
        delay: 1.3,
        onComplete: done
      })
    }

    // テキストが跳ねるようなアニメーション
    const textBeforeEnter = (el) => {
      gsap.set(el, {
        y: "-100%",
        opacity: 0
      })
    }
    const textEnter = (el, done) => {
      gsap.to(el, {
        opacity: 1,
        duration: 1.2,
        y: "0",
        ease: "bounce.out",
        // テキストを0.7秒ずつずらして上から下へ移動
        delay: 0 + 0.7 * (el.dataset.index),
        onComplete: done,
      })
    }

    return {
      getStarted,
      particlesInit,
      particlesLoaded,
      headerBeforeEnter,
      linksBeforeEnter,
      headerEnter,
      linksEnter,
      panelsBeforeEnter,
      panelsEnter,
      textEnter,
      textBeforeEnter
    }

  }
}
</script>


<template>
  <!-- ヘッダーメニューバー -->
  <transition appear @before-enter="headerBeforeEnter" @enter="headerEnter">
    <nav
      class="z-10 mt-6 fixed w-11/12 transform -translate-x-1/2 left-1/2 max-w-[85rem] bg-white border border-gray-200 rounded-[36px] mx-2 py-3 px-4 md:flex md:items-center md:justify-between md:py-0 md:px-6 lg:px-8 xl:mx-auto dark:bg-gray-800 dark:border-gray-700"
      aria-label="Global">
      <div class="navbar bg-base-100">
        <div class="navbar-start">
          <div class="dropdown">
            <label tabindex="0" class="btn btn-ghost lg:hidden">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
            </label>

            <div id="nav">
              <!-- 画面が狭いときはメニューをドロップダウンで表示 -->
              <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                <li><router-link to="/" aria-current="page">Home</router-link> </li>
                <li><router-link to="/system">System</router-link> </li>
                <li><router-link to="/about">About</router-link></li>
              </ul>
            </div>
          </div>
          <a class="btn btn-ghost text-xl p-0">InnerVS</a>
        </div>

        <!-- ヘッダーのメニュー部分のリンク -->
        <transition appear @before-enter="linksBeforeEnter" @enter="linksEnter">
          <div class="navbar-end hidden lg:flex">
            <div
              class="flex flex-col gap-y-4 gap-x-0 mt-5 md:flex-row md:items-center md:justify-end md:gap-y-0 md:gap-x-7 md:mt-0 md:ps-7">
              <div id="nav">
                <router-link to="/" aria-current="page">Home</router-link>
                <router-link to="/system">System</router-link>
                <router-link to="/about">About</router-link>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </nav>
  </transition>

  <!-- 背景アニメーションアニメーションの粒子サイズ等の設定 -->
  <vue-particles id="tsparticles" :particlesInit="particlesInit" :particlesLoaded="particlesLoaded" :options="{
    background: {
      color: {
        value: '#0F172A'
      }
    },
    fullsreen: {
      enable: true,
      zIndex: -1
    },
    fpsLimit: 120,
    interactivity: {
      events: {
        onClick: {
          enable: true,
          mode: 'push'
        },
        onHover: {
          enable: true,
          mode: 'bubble'
        },
        resize: true
      },
      modes: {
        bubble: {
          distance: 100,
          duration: 2,
          opacity: 0.8,
          size: 15
        },
        push: {
          quantity: 4
        },
        repulse: {
          distance: 200,
          duration: 0.4
        }
      }
    },
    particles: {
      color: {
        value: '#713fc8'
      },
      links: {
        color: '#713fc8',
        distance: 250,
        enable: true,
        opacity: 1,
        width: 1
      },
      move: {
        direction: 'none',
        enable: true,
        outMode: 'out',
        random: false,
        speed: 1,
        straight: false
      },
      number: {
        density: {
          enable: true,
          area: 800
        },
        value: 100
      },
      opacity: {
        value: 0.5
      },
      shape: {
        type: 'circle'
      },
      size: {
        random: false,
        value: 5
      }
    },
    detectRetina: true
  }" />
  <div class="h-full">
    <div class="overflow-hidden flex h-full">
      <div class="max-w-[50rem] flex flex-col mx-auto w-full h-full">

        <!-- タイトル部分 -->
        <main id="content" role="main" class="w-2/3 fixed top-1/4 left-1/5 2xl:pl-20">
          <div class="text-center py-10 px-4 sm:px-6 lg:px-8">
            <transition-group tag="div" appear @before-enter="textBeforeEnter" @enter="textEnter" class="text-container">
              <div key="h" data-index=0 class="text-left">
                <h1 class="block text-2xl font-bold text-white sm:text-4xl">Indoor Environment</h1>
                <h2 class="mt-1 sm:mt-3 text-4xl font-bold text-white sm:text-6xl">
                  <span class="bg-clip-text bg-gradient-to-tr from-blue-600 to-purple-400 text-transparent">Visualization
                    System</span>
                </h2>
              </div>
              <div key="p" data-index=1 class="text-left">
                <p class="mt-3 text-lg text-gray-300">
                  This system uses Machine Learning to predict and correct sensor values in a living space, and
                  visualizes the results in real time.
                </p>
              </div>
            </transition-group>
          </div>

          <!-- ボタン部分 -->
          <div class="text-left py-10 px-4 sm:px-6 lg:px-8">
            <transition appear @before-enter="panelsBeforeEnter" @enter="panelsEnter">
              <div class="flex-col justify-center items-center gap-2 sm:flex-row sm:gap-3">
                <a @click.prevent.stop="getStarted"
                  class="w-full sm:w-auto py-3 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-white text-gray-800 hover:bg-gray-200 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600"
                  href="#">
                  <svg class="flex-shrink-0 w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                    viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path d="m15 18-6-6 6-6" />
                  </svg>
                  Get Started
                </a>
              </div>
            </transition>
          </div>
        </main>

      </div>
    </div>
  </div>
</template>


<style scoped>
#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a:hover {
  opacity: 0.5;
}


#nav a.router-link-active {
  color: #42b983;
  font-weight: bold;
}

/* 背景アニメーション部分 */
#tsparticles {
  z-index: -1;
  position: absolute;
  width: 100%;
  background-color: #0F172A;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 50% 50%;
}

#nav>a {
  margin-right: 70px;
}

main{
  left: 8%;
}
</style>