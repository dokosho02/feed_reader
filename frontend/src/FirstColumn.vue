<template>
    <div class="column" :class="{ 'full-width': !isSmallScreen }" id="first-column">
      
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
            :class="[charClasses(char),
                { 'currently-selected': selectedFeed === feed }]"
            >{{ char }}</span>
                <hr v-if="feedIndex !==  group.feeds.length - 1">
            </div>
        </div>
        </span>
    </div>

    <!-- </div> -->
  </template>
  
  <script>
  export default {
    props: {
      isSmallScreen: Boolean
    }
  };
  </script>
  
  <style scoped>
  /* 样式 */
  </style>
  