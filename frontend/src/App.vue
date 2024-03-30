<template>

  <div id="app" :class="{ 'dark-mode': darkMode }" @keydown.left="goBack">
    <!-- loading animation -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading">
        <div class="loader"></div>
        <div>Loading...</div>
        <div>{{ loadingTime }}</div>
      </div>
    </div>
    <!-- <component :is="isSmallScreen ? 'full' : 'first-column'"
               :isSmallScreen="isSmallScreen">
    </component> -->
      <div class="column" id="first-column">
        <!-- <div :class="getColumnClass('first-column')" id="first-column"> -->

          <div class="icons-container">

              <span>&#x2026;</span>
              <span @click="toggleDarkMode">&#x25D0;</span>
              <!-- <span>&#x2605;</span>
              <span>&#x1F4D6;</span> -->

          </div>

          <!-- Display groups -->
          <span v-for="(group, index) in feedGroups" :key="index">
            <hr>
            <span>
              <div class="card-wrapper">
                    <div class="text-wrapper">
                  <span v-if="expanededFeedGroups.includes(index)" class="toggle-icon" @click="toggleGroup(index)">&#x25BE;</span>
                  <!-- test for the 1 st group -->
                  <!-- <span v-else-if="index !== 0" class="toggle-icon"  @click="toggleGroup(index)">&#x25B8;</span> -->
                  <span v-else class="toggle-icon"  @click="toggleGroup(index)">&#x25B8;</span>

                  <span v-for="(char, charIndex) in group.name" :key="charIndex" :class="charClasses(char)" @click="showGroupFeeds(group)">{{ char }}</span>
                </div>
                <div class="number-wrapper">
      <span v-if="unreadItemCountGroup(group) > 0" class="number-after-text">{{ unreadItemCountGroup(group) }}</span>
    </div>
  </div>
              </span>
              <!-- Feeds -->
              <div v-show="expanededFeedGroups.includes(index)" class="group-content">
                  <hr>

                  
                  <div v-for="(feed, feedIndex) in group.feeds" :key="feedIndex" @click="selectFeed(feed)">
                      <!-- <span v-for="(char, charIndex) in feed.name" :key="charIndex" @click="selectItem(feed)" :class="charClasses(char)">{{ char }}</span> -->
                      <div class="card-wrapper">
                        <div class="text-wrapper">
                      <span v-for="(char, charIndex) in feed.name"
                    :key="charIndex"
                    @click="selectItem(feed)"
                    :class="[charClasses(char),
                      { 'currently-selected': selectedFeed === feed }]"
                  >{{ char }}</span>
                </div>
                <div class="number-wrapper">
                  <span class="number-after-text" v-if="unreadItemCount(feed) > 0">{{ unreadItemCount(feed) }}</span>
                </div>
                </div>
                      <hr v-if="feedIndex !==  group.feeds.length - 1">
                  </div>
              </div>
          </span>
      </div>

      <!-- items -->
      <!-- <div :class="getColumnClass('second-column')" id="second-column"> -->
        <div v-if="!isSmallScreen || (isSmallScreen && currentColumn === 'second-column')" class="column" id="second-column">
          <div v-if="selectedFeed">
              <div class="icons-container">
              <span v-if="isSmallScreen && currentColumn !== 'first-column'" @click="goBack">&#x2190;</span>
              <span>&#x2026;</span>
              <span>&#x25C9;</span>
              <span>&#x2605;</span>
              <span>&#x1F4D6;</span>

              </div>
              <div v-for="(item, itemIndex) in selectedFeed.items" :key="itemIndex">
                  <hr>
                  <div class="card-wrapper">
                    <div class="text-wrapper">
                      <span v-for="(char, charIndex) in item.name"
                            :key="charIndex"
                            @click="selectItem(item)"
                            :class="[charClasses(char), 
                            { 'currently-selected': selectedItem === item },
                            { 'is-read': selectedItem !== item && item.isRead }
                            ]">
                            {{ char }}
                      </span>
                    </div>
                    <div class="number-wrapper">
                      <span class="number-after-text">{{ getRelativeTime(item.time) }}</span>
                    </div>
                  </div>
              </div>
          </div>
      </div>

      <!-- contents -->
      <!-- <div class="column" id="third-column"> -->
        <div v-if="!isSmallScreen || (isSmallScreen && currentColumn === 'third-column')" class="column" id="third-column">

          <div v-if="selectedItem">
              <div class="icons-container">
              <span v-if="isSmallScreen && currentColumn !== 'first-column'" @click="goBack">&#x2190;</span>
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
              <div
              @dblclick="scrollContent('third-column','up')"
              @click.exact="scrollContent('third-column', 'down')"
              @click.shift="scrollContent('third-column','up')"
              v-html="sanitizeContent(selectedItem.content)"></div>
              <!-- <div v-html="selectedItem.content"></div> -->
              <!-- <p><span v-for="(char, charIndex) in selectedItem.content" :key="charIndex" :class="charClasses(char)">{{ char }}</span></p> -->
              <hr>
          </div>
      </div>
  </div>
</template>


<script>
// import axios from 'axios';
import ky from 'ky';
import { DateTime } from 'luxon';

// import FirstColumn from './FirstColumn.vue';

export default {
  // components: {
  //   'first-column': FirstColumn,
  //   // 'first-column-small': FirstColumnSmall
  // },
  data() {
    return {
      feeds: [], // data obtained from the backend
      feedGroups: [],
      expanededFeedGroups: [],
      selectedFeed: null,
      selectedItem: null,
      loading: false,
      loadingStartTime: null,
      loadingTime: null,
      darkMode: false,
      isSmallScreen: false,
      currentColumn: 'first-column',
    };
  },
  created() {
    this.checkDeviceType();
    window.addEventListener('resize', this.checkDeviceType);
  },
  unmounted() {
    window.removeEventListener('resize', this.checkDeviceType);
  },
  mounted() {
    this.loadingStartTime = new Date();
    this.loading = true;
    this.startLoadingTimer();
    this.getFeeds().then(() => {
      this.stopLoadingTimer();
      this.loading = false;
      this.darkMode =  true;
    });
  },
  methods: {
    checkDeviceType() {
      this.isSmallScreen = window.innerWidth < 1000;
    },
    getColumnClass(columnName) {
      // 根据条件动态设置 class
      const classes = {};
      if (this.isSmallScreen && this.currentColumn === columnName) {
        classes['full-width'] = true; // 在 isSmallScreen 为 true 且 currentColumn 为指定列名时添加 full-width 类
      } else {
        classes[columnName] = true; // 在其他情况下添加 column 类
      }
      return classes;
    },
    goBack() {
      if (this.currentColumn === 'third-column') {
        this.currentColumn = 'second-column'; // 返回第二列
      } else if (this.currentColumn === 'second-column') {
        this.currentColumn = 'first-column'; // 返回第一列
      }
    },
    // Remove the existing method for generating data and let the backend provide the data instead
    toggleGroup(index) {
      if (this.expanededFeedGroups.includes(index)) {
        this.expanededFeedGroups = this.expanededFeedGroups.filter(item => item !== index);
      } else {
        this.expanededFeedGroups.push(index);
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
      this.selectedItem = null; // reset the selected item
      this.currentColumn = "second-column"
      this.scrollToTopOfColumn("second-column");

    },
    selectItem(item) {
      this.selectedItem = item;
      this.selectedItem.isRead = true; // update isRead property to true
      this.currentColumn = "third-column"
      this.scrollToTopOfColumn("third-column");
    },
    scrollToTopOfColumn(column_id) {
      const column = document.getElementById(column_id);
      if (column) {
        column.scrollTop = 0; // Set the scroll position to the top
      }
    },
    unreadItemCount(feed) {
      return feed.items.filter(item => !item.isRead).length;
    },
    unreadItemCountGroup(group) {
      let count = 0;
      group.feeds.forEach(feed => {
        count += feed.items.filter(item => !item.isRead).length;
      });
      return count;
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode; // 切换暗黑模式的状态
    },
    openLink(link) {
      // open a new window and navigate to a link
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
      if (!(typeof content !== 'string' || content === '')) {
        content = content.replace(/(<img[^>]*>)\s*(\S)/g, '$1<br>$2');
        console.log("fig");
      }
      const parser = new DOMParser();
      const doc = parser.parseFromString(content, 'text/html');
      
      const images = doc.querySelectorAll('img');
      images.forEach(image => {
          image.style.maxWidth = '100%'; // Limit the image width to 100% of the parent element width
          image.style.height = 'auto'; //
      });
      // ビデオ要素、スタイルを適用して幅を制限
      const videos = doc.querySelectorAll('video');
      videos.forEach(video => {
        video.style.maxWidth = '100%'; // 親要素の幅の100%に制限
        video.style.height = 'auto'; // 高さを自動調整
      });
      return doc.body.innerHTML;
    },
    removeSubstringBetween(str, startChar, endChar) {
      const regex = new RegExp(`${startChar}[^${endChar}]*${endChar}`, 'g');
      return str.replace(regex, '');
    },

    startLoadingTimer() {
      this.loadingTimer = setInterval(() => {
        this.loadingTime = this.calculateLoadingTime();
      }, 1000);
    },
    calculateLoadingTime() {
      if (this.loadingStartTime) {
        const currentTime = new Date();
        const milliseconds = currentTime - this.loadingStartTime;
        const seconds = Math.floor(milliseconds / 1000);
        return `${seconds}s`;
      } else {
        return '';
      }
    },
    stopLoadingTimer() {
      clearInterval(this.loadingTimer);
    },
    
    convertUTCToLocalTime(utcTimeList) {
      // console.log(utcTimeList);
      const [year, month, day, hours, minutes, seconds] = utcTimeList;
      const timestamp = Date.UTC(year, month - 1, day, hours, minutes, seconds);
      const localTime = DateTime.fromMillis(timestamp, { zone: 'local' });
      const formattedLocalTime = localTime.toFormat('yyyy-MM-dd HH:mm:ss ZZZZ');
      return formattedLocalTime;
    },
    getRelativeTime(utcTimeList) {
      const [year, month, day, hours, minutes, seconds] = utcTimeList;
      const timestamp = Date.UTC(year, month - 1, day, hours, minutes, seconds);
      const secondsDifference = Math.floor((new Date().getTime() - timestamp) / 1000);

      const intervals = [
        { label: 'Y', value: 365 * 24 * 60 * 60 },
        { label: 'M', value: 30 * 24 * 60 * 60 },
        { label: 'w', value: 7 * 24 * 60 * 60 },
        { label: 'd', value: 24 * 60 * 60 },
        { label: 'h', value: 60 * 60 },
        { label: 'm', value: 60 },
        { label: 's', value: 1 }
      ];

      for (const interval of intervals) {
        const amount = Math.floor(secondsDifference / interval.value);
        if (amount >= 1) {
          return `${amount}${interval.label}`;
        }
      }

      return '0s';

    },
    scrollContent(columnID, direction) {
      const scrollHeight = window.innerHeight*0.9;
      const thirdColumn = document.getElementById(columnID);
      if (thirdColumn) {
        if (direction === 'up') {
          thirdColumn.scrollTop -= scrollHeight;
        } else if (direction === 'down') {
          thirdColumn.scrollTop += scrollHeight;
        }
      }
    },
    async getFeeds() {

      // await axios.get('http://localhost:10000/data')
      // // await ky.get('http://localhost:10000/data')
      //   .then(response => {
      //     // console.log(response.status);
      //     // console.log(response.json);
      //       // this.feeds = response.data;
      //       // Adjust the structure of the retrieved data to match the previously generated data structure
      //       this.feeds = response.data.map(feed => ({
      //       name: feed.feed.title,
      //       group: `Test`, // Set group names based on the data returned by the backend
      //       items: feed.entries.map(entry => ({
      //         name: entry.title,
      //         link: entry.link,
      //         time: entry.published_parsed? entry.published_parsed : "", // Add safe access
      //         content: entry.content && entry.content.length > 0 ? entry.content[0].value : entry.summary,
      //       }))
      //     }));
      const response = await ky.get('http://localhost:10000/data').json();
      this.feeds = response.map(feed => ({
        name: feed.feed.title,
        group: `Test`, // Set group names based on the data returned by the backend
        items: feed.entries.map(entry => ({
          name: entry.title,
          link: entry.link,
          time: entry.published_parsed ? entry.published_parsed : "", // Add safe access
          content: entry.content && entry.content.length > 0 ? entry.content[0].value : entry.summary,
          isRead: false,
          isStarred: false,
        }))
      }));
        this.feedGroups = [{
          name: "Test", // Set group names based on the data returned by the backend
          feeds: this.feeds
        }];

        // Expand the first group by default
        this.expanededFeedGroups.push(0);
            console.log("get");
        // })
        // .catch(error => {
        //   console.error(error);
        // });
    }
  }
};
</script>


<style>

/* font */
/* Bold  */
@font-face {
  font-family: 'LXGWWenKai-Bold';
  src: url('@/assets/fonts/lxgw-wenkai/LXGWWenKai-Bold.ttf');
  font-weight: bold;
  font-style: normal;
}

/* Light  */
@font-face {
  font-family: 'LXGWWenKai-Light';
  src: url('@/assets/fonts/lxgw-wenkai/LXGWWenKai-Light.ttf');
  font-weight: lighter;
  font-style: normal;
}

/* Regular  */
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

/* div:lang(zh) {
  font-family: '仿宋', serif;
} */


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

.full-width {
  width: 100%;
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

.currently-selected {
  font-weight: bold;
}

.is-read {
  color: #888; /* set color for read items */
}


.card-wrapper {
  display: flex;
  justify-content: space-between;
}

.text-wrapper {
  text-align: left; /* 左对齐 */
}

.number-wrapper {
  padding-left: 10px;
  text-align: right; /* 右对齐 */
}


.number-after-text {
  color: #888; /* 设置相对时间的颜色 */
  font-size: 14px; /* 设置相对时间的字体大小 */
  font-style: italic; /* 设置相对时间的斜体样式 */
  text-align: right; /* 将相对时间右对齐 */
}

/* .icons-container {
  position: fixed;
  top: 10px; 
  right: 10px; 
  z-index: 999; 
} */




.dark-mode {
  background-color: #333; /* 设置暗黑背景色 */
  color: #ccc; /* 设置暗黑文本颜色 */
}


/* loading */

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 1);
  z-index: 999; /* Ensure that the loading animation is on top layer */
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
