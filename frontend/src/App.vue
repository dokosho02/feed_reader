<template>

  <div id="app">
    <!-- 加载动画 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading">
        <div class="loader"></div>
        <div>Loading...</div>
        <div>{{ loadingTime }}</div> <!-- 加载时间 -->
      </div>
    </div>
    
      <div class="column" id="first-column">

          <div class="icons-container">
              <!-- 预留一个位置给app 图标 -->

              <span>&#x2026;</span>
              <!-- <span>&#x25C9;</span>
              <span>&#x2605;</span>
              <span>&#x1F4D6;</span> -->

          </div>



          <!-- Display groups -->
          <span v-for="(group, index) in feedGroups" :key="index">
            <hr>
            <span>
                  <span v-if="expanededFeedGroups.includes(index)" class="toggle-icon" @click="toggleGroup(index)">&#x25BE;</span>
                  <!-- test for the 1 st group -->
                  <!-- <span v-else-if="index !== 0" class="toggle-icon"  @click="toggleGroup(index)">&#x25B8;</span> -->
                  <span v-else class="toggle-icon"  @click="toggleGroup(index)">&#x25B8;</span>

                  <span v-for="(char, charIndex) in group.name" :key="charIndex" :class="charClasses(char)" @click="showGroupFeeds(group)">{{ char }}</span>
              </span>
              <!-- Feeds -->
              <div v-show="expanededFeedGroups.includes(index)" class="group-content">
                  <hr>
                  <div v-for="(feed, feedIndex) in group.feeds" :key="feedIndex" @click="selectFeed(feed)">
                      <!-- <span v-for="(char, charIndex) in feed.name" :key="charIndex" @click="selectItem(feed)" :class="charClasses(char)">{{ char }}</span> -->
                      <span v-for="(char, charIndex) in feed.name"
                    :key="charIndex"
                    @click="selectItem(feed)"
                    :class="[charClasses(char), { 'currently_selected': selectedFeed === feed }]"
                  >{{ char }}</span>
                      <hr v-if="feedIndex !==  group.feeds.length - 1">
                  </div>
              </div>
          </span>
      </div>

      <!-- items -->
      <div class="column" id="second-column">
          <div v-if="selectedFeed">
              <div class="icons-container">
              <!-- 预留一个位置给app 图标 -->

              <span>&#x2026;</span>
              <span>&#x25C9;</span>
              <span>&#x2605;</span>
              <span>&#x1F4D6;</span>

              </div>
              <div v-for="(item, itemIndex) in selectedFeed.items" :key="itemIndex">
                  <hr>
                  <span v-for="(char, charIndex) in item.name"
                    :key="charIndex"
                    @click="selectItem(item)"
                    :class="[charClasses(char), { 'currently_selected': selectedItem === item }]"
                  >{{ char }}</span>
              </div>
          </div>
      </div>

      <!-- contents -->
      <div class="column" id="third-column">
          <div v-if="selectedItem">
              <div class="icons-container">
              <!-- 预留一个位置给app 图标 -->

              <span>&#x25CB;</span>
              <span>&#x25C9;</span>
              <span>&#x2606;</span>
              <!-- <span>&#x1F56E;</span> -->
              <span>&#x1F4D6;</span>

              <span @click="openLink(selectedItem.link)">&#x1F310;</span>

              </div>
              <hr>
              <!-- <img src="https://img.huxiucdn.com/article/cover/202403/18/212915139133.jpg" style="width: auto;"> -->
              <!-- <h2>{{ selectedItem.name }}</h2> -->
              <!-- <a :href="selectedItem.link" target="_blank" class="link-style">Web</a> -->
              <h2><span
                v-for="(char, charIndex) in selectedItem.name"
                :key="charIndex"
                :class="charClasses(char)"
                >{{ char }}</span>
              </h2>
              
              <!-- time -->
              <p v-if="selectedItem.time && Array.isArray(selectedItem.time)">
                {{ convertUTCToLocalTime(selectedItem.time) }}
              </p>


              <hr>



              <!-- <template v-for="segment in splitContent(selectedItem.content)">
                <div v-if="segment.type === 'text'">{{ segment.text }}</div>
                <span v-else>{{ segment.text }}</span> -->
              <!-- </template> -->
              <div v-html="sanitizeContent(selectedItem.content)"></div>
              <!-- <div v-html="selectedItem.content"></div> -->
              <!-- <p><span v-for="(char, charIndex) in selectedItem.content" :key="charIndex" :class="charClasses(char)">{{ char }}</span></p> -->
              <hr>
          </div>
      </div>
  </div>
</template>


<script>
import axios from 'axios';
import { DateTime } from 'luxon';

export default {
  data() {
    return {
      feeds: [], // 从后端获取的数据将赋值给这里
      feedGroups: [],
      expanededFeedGroups: [],
      selectedFeed: null,
      selectedItem: null,
      loading: false, // 初始时加载动画不显示
      loadingStartTime: null, // 加载开始时间
      loadingTime: null // 定时器对象
    };
  },
  mounted() {
    this.loadingStartTime = new Date(); // 记录加载开始时间
    this.loading = true; // 显示加载动画
    this.startLoadingTimer(); // 启动加载计时器
    this.getFeeds().then(() => {
      this.stopLoadingTimer(); // 停止加载计时器
      this.loading = false; // 隐藏加载动画
    });
  },
  methods: {
    // 移除原有的生成数据的方法，由后端提供数据
    toggleGroup(index) {
      if (this.expanededFeedGroups.includes(index)) {
        this.expanededFeedGroups = this.expanededFeedGroups.filter(item => item !== index); // 从 expanededFeedGroups 中移除 index
      } else {
        this.expanededFeedGroups.push(index); // 将 index 添加到 expanededFeedGroups
      }
    },
    showGroupFeeds(group) {
        this.selectedFeed = null;
        this.selectedItem = null;
        this.selectedFeed = {
          items: []
        };
        Object.values(group.feeds).forEach(feed => {
          this.selectedFeed.items.push(...feed.items);
        });
    },
    selectFeed(feed) {
      this.selectedFeed = feed;
      this.selectedItem = null; // 重置选中的条目
      this.scrollToTopOfColumn("second-column");

    },
    selectItem(item) {
      this.selectedItem = item;
      // 将第三栏的滚动位置设置为顶部
      this.scrollToTopOfColumn("third-column");
    },
    // 滚动第三栏到顶部
    scrollToTopOfColumn(column_id) {
      const column = document.getElementById(column_id);
      if (column) {
        column.scrollTop = 0; // 将滚动位置设置为顶部
      }
    },
    openLink(link) {
      // 使用 window.open() 打开新的窗口以导航到链接
      window.open(link, '_blank');
    },
    isEnglish(text) {
      return /[a-zA-Z]/.test(text);
    },
    isChinese(text) {
      const reg = new RegExp('[\\u4E00-\\u9FFF]+', 'g');
      return reg.test(text);
    },
    charClasses(char) {
      return ['font-style', { 'english': this.isEnglish(char), 'chinese': this.isChinese(char) }];
    },
    sanitizeContent(content) {
      // 将斜杠转义字符进行处理
      if (!(typeof content !== 'string' || content === '')) {
        content = content.replace(/(<img[^>]*>)\s*(\S)/g, '$1<br>$2');
        console.log("fig");
      }
      // 使用 DOMParser 将 HTML 字符串转换为 DOM 对象
      const parser = new DOMParser();
      const doc = parser.parseFromString(content, 'text/html');
      
      // 遍历所有图片元素，添加样式以限制宽度
      const images = doc.querySelectorAll('img');
      images.forEach(image => {
          image.style.maxWidth = '100%'; // 将图片宽度限制为父元素宽度的 100%
          image.style.height = 'auto'; // 自适应高度
      });
      // 遍历所有ビデオ要素、スタイルを適用して幅を制限
      const videos = doc.querySelectorAll('video');
      videos.forEach(video => {
        video.style.maxWidth = '100%'; // 親要素の幅の100%に制限
        video.style.height = 'auto'; // 高さを自動調整
      });
      // 返回处理后的 HTML 字符串
      return doc.body.innerHTML;
    },
    removeSubstringBetween(str, startChar, endChar) {
      const regex = new RegExp(`${startChar}[^${endChar}]*${endChar}`, 'g');
      return str.replace(regex, '');
    },

  convertUTCToLocalTime(utcTimeList) {
    // 使用 Date 对象将 UTC 时间转换为当地时间
    const utcTime = new Date(Date.UTC(...utcTimeList));

    // 使用 luxon 库将时间转换为包含时区名称的本地时间字符串
    const localTime = DateTime.fromJSDate(utcTime).setZone('local').toFormat('yyyy-MM-dd HH:mm:ss ZZZZ');

    return localTime;
},

    // 启动加载计时器
    startLoadingTimer() {
      this.loadingTimer = setInterval(() => {
        this.loadingTime = this.calculateLoadingTime(); // 更新加载时间
      }, 1000); // 每秒更新一次加载时间
    },
    calculateLoadingTime() {
      if (this.loadingStartTime) {
        const currentTime = new Date();
        const milliseconds = currentTime - this.loadingStartTime;
        const seconds = Math.floor(milliseconds / 1000);
        return `Time: ${seconds}s`;
      } else {
        return '';
      }
    },
    // 停止加载计时器
    stopLoadingTimer() {
      clearInterval(this.loadingTimer);
    },
    async getFeeds() {
      await axios.get('http://localhost:10000/data')
        .then(response => {
            // this.feeds = response.data; // 将获取到的数据赋值给 feeds
            // 将获取到的数据结构调整为与之前生成的数据结构相匹配
            this.feeds = response.data.map(feed => ({
            name: feed.feed.title,
            group: `Test`, // 根据后端返回的数据设置组名
            items: feed.entries.map(entry => ({
              name: entry.title,
              link: entry.link,
              time: entry.published_parsed? entry.published_parsed : "", // 添加安全访问
              content: entry.content && entry.content.length > 0 ? entry.content[0].value : entry.summary,
            }))
          }));

        // 初始化 feedGroups
        this.feedGroups = [{
          name: "Test", // 根据后端返回的数据设置组名
          feeds: this.feeds
        }];

        // 默认展开第一个组
        this.expanededFeedGroups.push(0);
            console.log("get");
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>


<style>

/* font */
/* Bold 字体 */
@font-face {
  font-family: 'LXGWWenKai-Bold';
  src: url('@/assets/fonts/lxgw-wenkai/LXGWWenKai-Bold.ttf');
  font-weight: bold;
  font-style: normal;
}

/* Light 字体 */
@font-face {
  font-family: 'LXGWWenKai-Light';
  src: url('@/assets/fonts/lxgw-wenkai/LXGWWenKai-Light.ttf');
  font-weight: lighter;
  font-style: normal;
}

/* Regular 字体 */
@font-face {
  font-family: 'LXGWWenKai-Regular';
  src: url('@/assets/fonts/lxgw-wenkai/LXGWWenKai-Regular.ttf');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Noto Sans SC', sans-serif;
  src: url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@100..900&display=swap') format('woff2');
  font-weight: normal;
  font-style: normal;
}

/* .font-style {
  font-family: "Cambria", serif;
} */
.font-style.english {
  font-family: 'Cambria', serif;
}

.font-style.chinese {
  font-family: 'Noto Sans SC', sans-serif;
}


div {
  font-family: "Cambria", serif;
}

div:lang(zh) {
  font-family: '仿宋', serif;
}


html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  overflow-y: auto;
  height: 100%;
  width: 100%;
}

/* #first-column,
#second-column {
  width: calc(50% - 1px);
}

#third-column {
  width: calc(75% - 2px);
} */

/* layout */
#first-column {
  width: calc(30% - 1px);
}

#second-column {
  width: calc(50% - 1px);
}

#third-column {
  width: calc(75% - 2px);
}

.column {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  height: 100%;
}
/* function */
.toggle-icon {
  margin-left: auto;
}

.group-content {
  padding-left: 20px;
}

.feed-item:hover {
  background-color: #f0f0f0;
}

.currently_selected {
  font-weight: bold;
}

/* loading */

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 1); /* 不透明白色背景 */
  z-index: 999; /* 确保加载动画在最上层 */
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.loader {
  border: 4px solid #f3f3f3; /* Light grey */
  border-top: 4px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
